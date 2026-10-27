% Exercise 2 (decision table). 
walk(sunny, free,  go_for_a_walk).
walk(sunny, busy,  stay_in).
walk(rainy, _,     stay_in).

start :-
    write('Weather? (sunny/rainy)'), nl,
    read(Weather),
    write('Are you free? (free/busy)'), nl,
    read(Time),
    walk(Weather, Time, Action),
    write('Decision: '), write(Action), nl.
