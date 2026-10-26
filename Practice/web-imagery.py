import re, io, math, time, hashlib, requests
from PIL import Image
from datetime import date

CONFIG_URL = "https://s3-us-west-2.amazonaws.com/config.maptiles.arcgis.com/waybackconfig.json"
HEADERS = {"User-Agent": "student-srs-project"}

# Reusable session injected here
SESSION = requests.Session()
SESSION.headers.update(HEADERS)

def load_releases(since="2016-01-01"):
    cfg = SESSION.get(CONFIG_URL, timeout=30).json()
    rels = []
    for num, item in cfg.items():
        m = re.search(r"\d{4}-\d{2}-\d{2}", item["itemTitle"])
        if m and m.group() >= since:                 # only the last ~10 years
            rels.append({"num": int(num), "date": m.group(), "url": item["itemURL"]})
    return sorted(rels, key=lambda r: r["date"])

def lonlat_to_tile(lon, lat, z):
    n = 2 ** z
    # Fixed missing multiplication/subtraction operators from original snippet
    x = (lon + 180) / 360 * n
    y = (1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * n
    return x, y

def get_tile(rel, z, x, y):
    try:
        r = SESSION.get(rel["url"].format(level=z, row=y, col=x), timeout=15)
        return r.content if r.status_code == 200 else None
    except requests.RequestException:
        return None

def get_image(rel, west, south, east, north, z=18, max_tiles=150):
    x0f, y0f = lonlat_to_tile(west, north, z)
    x1f, y1f = lonlat_to_tile(east, south, z)
    x0, x1, y0, y1 = int(x0f), int(x1f), int(y0f), int(y1f)
    n = (x1 - x0 + 1) * (y1 - y0 + 1)
    
    # New validation logic
    if n > max_tiles:
        raise ValueError(f"{n} tiles needed - use a smaller box or a lower zoom")
    
    # Rest of the original get_image function stays the same
    mosaic = Image.new("RGB", ((x1 - x0 + 1) * 256, (y1 - y0 + 1) * 256))
    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            data = get_tile(rel, z, x, y)
            if data:
                tile = Image.open(io.BytesIO(data)).convert("RGB")
                mosaic.paste(tile, ((x - x0) * 256, (y - y0) * 256))
            time.sleep(0.05)                      # be polite to the server
    box = [int((x0f - x0) * 256), int((y0f - y0) * 256),
           int((x1f - x0) * 256), int((y1f - y0) * 256)]
    return mosaic.crop(box)

def metres_per_pixel(lat, z):
    # Fixed missing multiplication operator from original snippet
    return 156543.03392 * math.cos(math.radians(lat)) / 2 ** z

def releases_with_changes(rels, lon, lat, z=17):
    x, y = (int(v) for v in lonlat_to_tile(lon, lat, z))
    kept, last = [], None
    for i, rel in enumerate(rels, 1):
        # Progress tracking added here
        print(f"checking {i}/{len(rels)}  {rel['date']}", flush=True)
        data = get_tile(rel, z, x, y)
        h = hashlib.md5(data).hexdigest() if data else None
        if h and h != last:
            kept.append(rel)
            last = h
    return kept

def pick_release(rels, target):
    """Release whose date is closest to target ('YYYY-MM-DD')."""
    t = date.fromisoformat(target)
    return min(rels, key=lambda r: abs((date.fromisoformat(r["date"]) - t).days))

def box_around(lon, lat, half_m):
    """Bounding box (west, south, east, north) around a point."""
    dlat = half_m / 111320
    dlon = half_m / (111320 * math.cos(math.radians(lat)))
    return lon - dlon, lat - dlat, lon + dlon, lat + dlat

def tile_fingerprint(rel, lon, lat, z=17):
    x, y = (int(v) for v in lonlat_to_tile(lon, lat, z))
    data = get_tile(rel, z, x, y)
    return hashlib.md5(data).hexdigest() if data else None

# ---- one place, 10-year backtrack ----
if __name__ == "__main__":
    lon, lat = 67.11281430823749, 24.93046370276989
    west, south, east, north = box_around(lon, lat, half_m=500)   # ~1 km box
    rels = load_releases()

    seen = {}
    for year in range(2016, 2027):
        rel = pick_release(rels, f"{year}-06-30")
        fp = tile_fingerprint(rel, lon, lat)
        if fp is None:
            print(year, "no tile returned")
            continue
        if fp in seen:
            print(year, rel["date"], "same imagery as", seen[fp])
            continue
        seen[fp] = rel["date"]
        get_image(rel, west, south, east, north).save(f"site_{rel['date']}.png")
        print("saved", rel["date"])
    print(round(metres_per_pixel(lat, 18), 3), "m/px at zoom 18")