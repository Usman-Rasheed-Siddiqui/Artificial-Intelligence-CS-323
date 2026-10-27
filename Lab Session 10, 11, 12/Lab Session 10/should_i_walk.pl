% Exercise 2 (decision table). 
walk(hot, dry, _, _, _, dont_go).
walk(hot, windy, yes, _, _, dont_go).
walk(hot, windy, no, yes, high, go_for_a_walk).
walk(hot, windy, no, yes, moderate, walk_15_20_min).
walk(hot, windy, no, yes, low, gentle_stroll).
walk(hot, windy, no, no, _, dont_go).
walk(cold, wet, yes, _, _, dont_go).
walk(cold, wet, no, yes, high, go_for_a_walk).
walk(cold, wet, no, yes, moderate, walk_15_20_min).
walk(cold, wet, no, yes, low, gentle_stroll).
walk(cold, wet, no, no, _, dont_go).

start:-
    write('Weather1? (hot, cold)'), nl,
    read(Weather1),
    write('Weather2? (dry, windy, wet)'), nl,
    read(Weather2),
    write('Physical Limitations? (yes, no)'), nl,
    read(Physical_limitation),
    write('Safe Time? (yes, no)'), nl,
    read(Safe_time),
    write('Energy Level? (high, moderate, low)'), nl,
    read(Energy_level),
    walk(Weather1, Weather2, Physical_limitation, Safe_time, Energy_level, Action),
    write('Decision: '), write(Action), nl.
    
    
    
    