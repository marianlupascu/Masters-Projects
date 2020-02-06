
get_all_literals_from_a_clause_aux([], Aux, Res) :- sort(Aux, Res), !.
get_all_literals_from_a_clause_aux([n(H)|T], Aux, Res):- get_all_literals_from_a_clause_aux(T, [H|Aux], Res), !.
get_all_literals_from_a_clause_aux([H|T], Aux, Res):- get_all_literals_from_a_clause_aux(T, [H|Aux], Res).

get_all_literals_from_a_clause([], []) :- !.
get_all_literals_from_a_clause(Clause, Res) :- get_all_literals_from_a_clause_aux(Clause, [], Res).


get_all_literals_from_a_set_of_clauses_aux([], Aux, Res) :- sort(Aux, Res), !.
get_all_literals_from_a_set_of_clauses_aux([H|T], Aux, Res) :- get_all_literals_from_a_clause(H, Literals),
                                                               append(Literals, Aux, Aux2),
                                                               get_all_literals_from_a_set_of_clauses_aux(T, Aux2, Res).

get_all_literals_from_a_set_of_clauses([], []) :- !.
get_all_literals_from_a_set_of_clauses(Set, Res) :- get_all_literals_from_a_set_of_clauses_aux(Set, [], Res).

get_clause_with_a_positive_literal([], _, []).
get_clause_with_a_positive_literal([H|_], Lit, H) :- member(Lit, H), !.
get_clause_with_a_positive_literal([_|T], Lit, Res) :- get_clause_with_a_positive_literal(T, Lit, Res).

get_clause_with_a_negative_literal([], _, []).
get_clause_with_a_negative_literal([H|_], Lit, H) :- member(n(Lit), H), !.
get_clause_with_a_negative_literal([_|T], Lit, Res) :- get_clause_with_a_negative_literal(T, Lit, Res).

is_trivial_clause([], 'No').
is_trivial_clause(C, 'Yes') :- member(A, C),
                               member(n(A), C).
is_trivial_clause(_, 'No').

remove_trivial_clauses([], []).
remove_trivial_clauses([H|T], Res) :- is_trivial_clause(H, 'Yes'),
                                      remove_trivial_clauses(T, Res).
remove_trivial_clauses([H|T], [H|Res]) :- is_trivial_clause(H, 'No'),
                                          remove_trivial_clauses(T, Res).

find_possible_resolvent(_, [], [], [], _).
find_possible_resolvent(Clauses, [Lit|_], Cplus, Cminus, Lit) :- get_clause_with_a_positive_literal(Clauses, Lit, Cplus),
                                                                 get_clause_with_a_negative_literal(Clauses, Lit, Cminus),
                                                                 Cplus \= [],
                                                                 Cminus \= [], !.
find_possible_resolvent(Clauses, [_|T], Cplus, Cminus, Lit) :- find_possible_resolvent(Clauses, T, Cplus, Cminus, Lit).
                                         
resolution_aux([], 'Satisfiable') :- !.
resolution_aux(Set, 'Unsatisfiable') :- member([], Set), !.
resolution_aux(Set, 'Satisfiable') :- remove_trivial_clauses(Set, Set2),
                        get_all_literals_from_a_set_of_clauses(Set2, Literals),
                        find_possible_resolvent(Set2, Literals, Cplus, _, _),
                        Cplus = [], write('aici1').
resolution_aux(Set, 'Satisfiable') :- remove_trivial_clauses(Set, Set2),
                        get_all_literals_from_a_set_of_clauses(Set2, Literals),
                        find_possible_resolvent(Set2, Literals, _, Cminus, _), 
                        Cminus = [], write('aici2').
resolution_aux(Set, Ans) :- remove_trivial_clauses(Set, Set2),
                        get_all_literals_from_a_set_of_clauses(Set2, Literals),
                        find_possible_resolvent(Set2, Literals, Cplus, Cminus, Lit),
                        Cplus \= [],
                        Cminus \= [],
                        delete(Cplus, Lit, R1),
                        delete(Cminus, n(Lit), R2),
                        union(R1, R2, Resolvent),
                        delete(Set2, Cplus, Aux1),
                        delete(Aux1, Cminus, Aux2),
                        union(Aux2, [Resolvent], NewSet),
                        write(Set2),
                        nl,
                        write(Cplus),
                        write(Cminus),
                        write(Resolvent),
                        nl,
                        resolution_aux(NewSet, Ans).

resolution(Set, 'Unsatisfiable') :- resolution_aux(Set, 'Unsatisfiable'), !.
resolution(Set, 'Satisfiable') :- resolution_aux(Set, 'Satisfiable'), !.

main_aux_res(T) :- 
see('C:\\Users\\Marian Lupascu\\Documents\\Documente\\FMI\\MI\\Sem I\\KnowRepr&Reason\\data2.txt'),
    read(C),
    (   C == end_of_file
    ->  seen,
        resolution(T, Ans),
        tell('C:\\Users\\Marian Lupascu\\Documents\\Documente\\FMI\\MI\\Sem I\\KnowRepr&Reason\\out.txt'),
        write(Ans),
        told
    ;   A = [C|T],
    	main_aux_res(A)
    ).
main_res :- main_aux_res([]).


dot_positive([], _, []).
dot_positive([H|T], Literal, [H|Res]) :- not(member(Literal, H)), 
                                         not(member(n(Literal), H)),
                                         dot_positive(T, Literal, Res), !.
dot_positive([H|T], Literal, [A|Res]) :- member(n(Literal), H), 
                                         delete(H, n(Literal), A),
                                         dot_positive(T, Literal, Res), !.
dot_positive([H|T], Literal, Res) :- member(Literal, H), 
                                     dot_positive(T, Literal, Res), !.

dot_negative([], _, []).
dot_negative([H|T], Literal, [H|Res]) :- not(member(Literal, H)), 
                                         not(member(n(Literal), H)),
                                         dot_negative(T, Literal, Res), !.
dot_negative([H|T], Literal, [A|Res]) :- member(Literal, H), 
                                         delete(H, Literal, A),
                                         dot_negative(T, Literal, Res), !.
dot_negative([H|T], Literal, Res) :- member(n(Literal), H), 
                                     dot_negative(T, Literal, Res), !.

dp_aux([], _, 'Yes', []) :- !.
dp_aux(Set, _ , 'No', _) :- member([], Set).
dp_aux(Set, [Lit|T], Ans, [(Lit, 'true')|L]) :- remove_trivial_clauses(Set, Set2),
                             dot_positive(Set2, Lit, R),
                             dp_aux(R, T, Ans, L), write(R), nl.
dp_aux(Set, [Lit|T], Ans, [(Lit, 'false')|L]) :- remove_trivial_clauses(Set, Set2),
                             dot_negative(Set2, Lit, R),
                             dp_aux(R, T, Ans, L), write(R), nl.

dp([], 'Yes', []) :- !.
dp(Set, 'No', []) :- member([], Set), !.
dp(Set, 'Yes', L) :- remove_trivial_clauses(Set, Set2),
                get_all_literals_from_a_set_of_clauses(Set2, Literals),
                dp_aux(Set2, Literals, 'Yes', L), !.
dp(Set, 'No', []) :- remove_trivial_clauses(Set, Set2),
                get_all_literals_from_a_set_of_clauses(Set2, Literals),
                dp_aux(Set2, Literals, 'No', _), !.
                
%?- dp([[n(a), n(e), b], [n(d), e, n(b)], [n(e), f, n(b)], [f, n(a), e], [e, f, n(b)]] ,R)
%?- dp([[n(a), n(b)], [a, b], [n(a), b], [a, n(b)]] ,R)


get_frequences_for_one_literal([], _, R, R) :- !.
get_frequences_for_one_literal([H|T], Lit, Now, Res) :- member(Lit, H),
                                                        A is Now + 1,
                                                        get_frequences_for_one_literal(T, Lit, A, Res), !.
get_frequences_for_one_literal([H|T], Lit, Now, Res) :- not(member(Lit, H)),
                                                        get_frequences_for_one_literal(T, Lit, Now, Res), !.

get_frequences(_, [], []) :- !.
get_frequences(C, [H|T], [(H, A)|Res]) :- get_frequences_for_one_literal(C, H, 0, A1),
                                          get_frequences_for_one_literal(C, n(H), 0, A2),
                                          A is A1 + A2,
                                          get_frequences(C, T, Res).

get_max_pair([], M, L, M, L) :- !.
get_max_pair([(Lit, Freq)|T], M, _, R, L) :- M < Freq, get_max_pair(T, Freq, Lit, R, L), !.
get_max_pair([(_, Freq)|T], M, Lit, R, L) :- not(M < Freq), get_max_pair(T, M, Lit, R, L), !.

get_literal_that_appears_in_most_clauses(C, Res) :- remove_trivial_clauses(C, C1),
                                                    get_all_literals_from_a_set_of_clauses(C1, Literals),
                                                    get_frequences(C1, Literals, Freq),
                                                    get_max_pair(Freq, 0, 0, _, Res).

dp_aux1([], 'Yes', []) :- !.
dp_aux1(Set, 'No', _) :- member([], Set).
dp_aux1(Set, Ans, [(Lit, 'true')|L]) :- remove_trivial_clauses(Set, Set2),
                             get_literal_that_appears_in_most_clauses(Set2, Lit),
    						 Lit \= 0,
                             dot_positive(Set2, Lit, R),
                             dp_aux1(R, Ans, L), write(R), nl.
dp_aux1(Set, Ans, [(Lit, 'false')|L]) :- remove_trivial_clauses(Set, Set2),
                             get_literal_that_appears_in_most_clauses(Set2, Lit),
                             Lit \= 0,
                             dot_negative(Set2, Lit, R),
                             dp_aux1(R, Ans, L), write(R), nl.

dp1([], 'Yes', []) :- !.
dp1(Set, 'No', []) :- member([], Set), !.
dp1(Set, 'Yes', L) :- remove_trivial_clauses(Set, Set2),
                dp_aux1(Set2, 'Yes', L), !.
dp1(Set, 'No', []) :- remove_trivial_clauses(Set, Set2),
                dp_aux1(Set2, 'No', _), !.



shortest_clause_aux([], RL, RC, RL, RC) :- !.
shortest_clause_aux([H|T], L, _, RL, RC) :- length(H, A), A < L, shortest_clause_aux(T, A, H, RL, RC), !.
shortest_clause_aux([H|T], L, C, RL, RC) :- length(H, A), not(A < L), shortest_clause_aux(T, L, C, RL, RC), !.


shortest_clause(C, R) :- get_all_literals_from_a_set_of_clauses(C, Literals),
                         length(Literals, A),
                         B is A + A + 1,
                         shortest_clause_aux(C, B, 0, _, R).

get_literal_that_appears_in_shortest_clause(C, Res) :- remove_trivial_clauses(C, C1),
                                                    shortest_clause(C1, [n(Res)|_]), !.
get_literal_that_appears_in_shortest_clause(C, Res) :- remove_trivial_clauses(C, C1),
                                                    shortest_clause(C1, [Res|_]), !.

dp_aux2([], 'Yes', []) :- !.
dp_aux2(Set, 'No', _) :- member([], Set).
dp_aux2(Set, Ans, [(Lit, 'true')|L]) :- remove_trivial_clauses(Set, Set2),
    get_literal_that_appears_in_shortest_clause(Set2, Lit),
                             dot_positive(Set2, Lit, R),
                             dp_aux2(R, Ans, L), write(R), nl.
dp_aux2(Set, Ans, [(Lit, 'false')|L]) :- remove_trivial_clauses(Set, Set2),
    get_literal_that_appears_in_shortest_clause(Set2, Lit),
                             dot_negative(Set2, Lit, R),
                             dp_aux2(R, Ans, L), write(R), nl.

dp2([], 'Yes', []) :- !.
dp2(Set, 'No', []) :- member([], Set), !.
dp2(Set, 'Yes', L) :- remove_trivial_clauses(Set, Set2),
                dp_aux2(Set2, 'Yes', L), !.
dp2(Set, 'No', []) :- remove_trivial_clauses(Set, Set2),
                dp_aux2(Set2, 'No', _), !.
    
main_aux(T) :- 
see('C:\\Users\\Marian Lupascu\\Documents\\Documente\\FMI\\MI\\Sem I\\KnowRepr&Reason\\sat1.txt'),
    read(C),
    (   C == end_of_file
    ->  seen,
        dp2(T, Ans, L),
        tell('C:\\Users\\Marian Lupascu\\Documents\\Documente\\FMI\\MI\\Sem I\\KnowRepr&Reason\\out.txt'),
        write(Ans),
        nl,
        write(L),
        told
    ;   A = [C|T],
    	main_aux(A)
    ).
main :- main_aux([]).

