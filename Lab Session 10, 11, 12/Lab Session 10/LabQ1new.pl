% === Facts: City Populations ===
population(karachi, 15000000).
population(lahore, 11000000).
population(islamabad, 2000000).
population(quetta, 1000000).
population(peshawar, 2500000).

% Conditions
large_city(X) :- population(X, P), P > 5000000.
small_city(X) :- population(X, P), P < 3000000.

% New rule: population greater than 2,000,000
population_greater_than_2m(X) :- population(X, P), P > 2000000.



