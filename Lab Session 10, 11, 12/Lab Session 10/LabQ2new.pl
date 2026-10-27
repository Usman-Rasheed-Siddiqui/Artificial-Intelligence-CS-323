% === Facts ===
weather(karachi, hot).
weather(lahore, moderate).
weather(peshawar, moderate).
weather(islamabad, cold).

% === Helper Rules ===
hot_area(X) :- weather(X, hot).
chilly(X) :- weather(X, cold).
comfortable(X) :- weather(X, moderate).

% === Travel Advisory Rules ===
% A city is good for travel if it is comfortable and NOT a hot area
good_for_travel(X) :- comfortable(X), \+ hot_area(X).

% Avoid travel if it is chilly OR a hot area
avoid_travel(X) :- chilly(X).
avoid_travel(X) :- hot_area(X).

% Moderate advice if it is neither good_for_travel nor avoid_travel
moderate_advice(X) :- weather(X, _), \+ good_for_travel(X), \+ avoid_travel(X).



