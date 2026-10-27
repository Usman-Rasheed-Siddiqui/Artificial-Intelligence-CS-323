% === Facts ===
weather(karachi, hot).
weather(lahore, moderate).
weather(peshawar, moderate).
weather(islamabad, cold).

% === Rules ===
comfortable(X) :- weather(X, moderate).