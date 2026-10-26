import re
import io
import math
import time
from datetime import date
from pathlib import Path

import requests
from PIL import Image

# ============================================================
# KARACHI CONSTRUCTION SITE - ARCGIS WAYBACK IMAGE EXPORT
# ============================================================

LON = 67.11281430823749
LAT = 24.93046370276989
HALF_WIDTH_METRES = 250
ZOOM = 20

TARGET_DATES = [
    "2026-10-24",
    "2025-11-24",
    "2025-12-24",
    "2026-01-24",
    "2026-02-24",
]

CONFIG_URL = (
    "https://s3-us-west-2.amazonaws.com/"
    "config.maptiles.arcgis.com/waybackconfig.json"
)

OUTPUT_DIR = Path("karachi_wayback_results")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "student-srs-project/1.0"})

TILE_SIZE = 256
REQUEST_DELAY_SECONDS = 0.05


def lonlat_to_tile(lon, lat, zoom):
    """Convert longitude/latitude to fractional XYZ Web Mercator tile coordinates."""
    lat = max(min(lat, 85.05112878), -85.05112878)
    n = 2 ** zoom
    x = (lon + 180.0) / 360.0 * n
    lat_rad = math.radians(lat)
    y = (1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n
    return x, y


def box_around(lon, lat, half_metres):
    """Return west, south, east, north for a square ground-distance bounding box."""
    dlat = half_metres / 111320.0
    cos_lat = math.cos(math.radians(lat))
    if abs(cos_lat) < 1e-8:
        raise ValueError("Latitude too close to a pole.")
    dlon = half_metres / (111320.0 * cos_lat)
    return lon - dlon, lat - dlat, lon + dlon, lat + dlat


def load_releases():
    """Load ArcGIS Wayback basemap releases."""
    print("Loading ArcGIS Wayback release catalogue...")
    response = SESSION.get(CONFIG_URL, timeout=45)
    response.raise_for_status()
    config = response.json()

    releases = []
    for key, item in config.items():
        title = item.get("itemTitle", "")
        match = re.search(r"(\d{4}-\d{2}-\d{2})", title)
        if not match or not item.get("itemURL"):
            continue

        releases.append({
            "release_num": int(key),
            "release_date": match.group(1),
            "title": title,
            "tile_url": item["itemURL"],
        })

    releases.sort(key=lambda r: r["release_date"])
    if not releases:
        raise RuntimeError("No releases found in the Wayback catalogue.")

    print(
        f"Loaded {len(releases)} releases: "
        f"{releases[0]['release_date']} to {releases[-1]['release_date']}"
    )
    return releases


def make_tile_url(release, zoom, x, y):
    """Fill common ArcGIS tile-template placeholders."""
    template = release["tile_url"]
    replacements = {
        "{level}": str(zoom),
        "{z}": str(zoom),
        "{row}": str(y),
        "{y}": str(y),
        "{col}": str(x),
        "{column}": str(x),
        "{x}": str(x),
    }
    for placeholder, value in replacements.items():
        template = template.replace(placeholder, value)
    return template


def download_tile(release, zoom, x, y):
    """Download and validate one tile from a selected Wayback release."""
    url = make_tile_url(release, zoom, x, y)
    try:
        response = SESSION.get(url, timeout=30)
        if response.status_code != 200:
            return None
        content = response.content
        with Image.open(io.BytesIO(content)) as img:
            img.verify()
        return content
    except (requests.RequestException, OSError, ValueError):
        return None


def download_area(release, bounds, zoom=ZOOM):
    """
    Download all tiles covering the requested bounds and crop to the exact
    fractional-tile bounds. There is intentionally no arbitrary 100-tile cap.
    """
    west, south, east, north = bounds
    x0f, y0f = lonlat_to_tile(west, north, zoom)
    x1f, y1f = lonlat_to_tile(east, south, zoom)

    x0, x1 = math.floor(x0f), math.ceil(x1f) - 1
    y0, y1 = math.floor(y0f), math.ceil(y1f) - 1

    cols = x1 - x0 + 1
    rows = y1 - y0 + 1
    tile_count = cols * rows
    print(f"Tiles required: {cols} columns x {rows} rows = {tile_count}")

    mosaic = Image.new("RGB", (cols * TILE_SIZE, rows * TILE_SIZE), (35, 35, 35))
    successful = 0
    failed = 0

    for row_index, y in enumerate(range(y0, y1 + 1), start=1):
        print(f"  Downloading tile row {row_index}/{rows}...")
        for x in range(x0, x1 + 1):
            data = download_tile(release, zoom, x, y)
            if data:
                try:
                    with Image.open(io.BytesIO(data)) as tile_img:
                        tile = tile_img.convert("RGB")
                    if tile.size != (TILE_SIZE, TILE_SIZE):
                        tile = tile.resize((TILE_SIZE, TILE_SIZE))
                    mosaic.paste(
                        tile,
                        ((x - x0) * TILE_SIZE, (y - y0) * TILE_SIZE),
                    )
                    successful += 1
                except OSError:
                    failed += 1
            else:
                failed += 1
            time.sleep(REQUEST_DELAY_SECONDS)

    print(f"Valid tiles: {successful}/{tile_count}; failed/missing: {failed}")
    if successful == 0:
        return None

    # Crop using fractional XYZ tile coordinates.
    crop_box = (
        round((x0f - x0) * TILE_SIZE),
        round((y0f - y0) * TILE_SIZE),
        round((x1f - x0) * TILE_SIZE),
        round((y1f - y0) * TILE_SIZE),
    )
    crop_box = (
        max(0, min(crop_box[0], mosaic.width)),
        max(0, min(crop_box[1], mosaic.height)),
        max(0, min(crop_box[2], mosaic.width)),
        max(0, min(crop_box[3], mosaic.height)),
    )
    result = mosaic.crop(crop_box)
    return result if result.width > 0 and result.height > 0 else None


def main():
    bounds = box_around(LON, LAT, HALF_WIDTH_METRES)
    west, south, east, north = bounds

    print("\nKarachi construction site")
    print(f"Centre: {LON:.8f}, {LAT:.8f}")
    print("Requested area: 500 m x 500 m")
    print(f"West:  {west:.8f}")
    print(f"South: {south:.8f}")
    print(f"East:  {east:.8f}")
    print(f"North: {north:.8f}")
    print(f"Tile zoom: {ZOOM}")
    print("\nNote: Wayback release dates are publication dates, not necessarily")
    print("the actual image capture dates for this location.\n")

    releases = load_releases()

    for target_text in TARGET_DATES:
        target = date.fromisoformat(target_text)
        selected = min(
            releases,
            key=lambda release: abs(
                (date.fromisoformat(release["release_date"]) - target).days
            ),
        )

        release_date = selected["release_date"]
        day_difference = abs((date.fromisoformat(release_date) - target).days)

        print("-" * 60)
        print(f"Target date: {target_text}")
        print(f"Selected Wayback release: {release_date}")
        print(f"Release-date difference: {day_difference} days")

        filename = OUTPUT_DIR / f"target_{target_text}_release_{release_date}.png"

        try:
            image = download_area(selected, bounds, zoom=ZOOM)
            if image is None:
                print("No valid image tiles returned; no file saved.")
                continue

            image.save(filename)
            print(f"Saved image: {filename.resolve()}")
        except (requests.RequestException, ValueError, OSError) as exc:
            print(f"Failed to download this image: {exc}")

    print("\nFinished. Check the karachi_wayback_results folder.")


if __name__ == "__main__":
    main()
