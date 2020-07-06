temperatureHeigerThen38(Temperature, true) :- Temperature > 38, !.
temperatureHeigerThen38(_, false).
 
patientWasSickForAtLeast2Days(Num_days, true) :- Num_days > 2, !.
patientWasSickForAtLeast2Days(_, false).
 
hasCough(yes, true).
hasCough(no, false).

updateLwithTemperatureHeigerThen38(true, L, NL) :- append(L, [[th]], NL), !.
updateLwithTemperatureHeigerThen38(_, L, L).

updateLwithPatientWasSickForAtLeast2Days(true, L, NL) :- append(L, [[sr]], NL), !.
updateLwithPatientWasSickForAtLeast2Days(_, L, L).

updateLwithHasCough(true, L, NL) :- append(L, [[c]], NL), !.
updateLwithHasCough(_, L, L).

checkAllNegativeClause([]).
checkAllNegativeClause([n(_)|T]) :- checkAllNegativeClause(T).

singleNegativeClause(R, L) :- member(R, L), 
    						  delete(L, R, NL),
                              checkAllNegativeClause(NL), !.

negateList([], []).
negateList([n(U)|T], [U|R]) :- negateList(T, R).

backwardChaining([], _, _) :- !.
backwardChaining([H|T], KB, [KBH|_]) :- singleNegativeClause(H, KBH),
                                        delete(KBH, H, Aux),
                                        negateList(Aux, Aux2),
                                        append(Aux2, T, Aux3),
                                        backwardChaining(Aux3, KB, KB), !.
backwardChaining([H|T], KB, [_|KBT]) :- backwardChaining([H|T], KB, KBT), !.




checkAllOfTheGoalsAreSolved([], _).
checkAllOfTheGoalsAreSolved([H|T], L) :- member((H, solved), L), 
                                         checkAllOfTheGoalsAreSolved(T, L), !.
numNegativeLiterals([], 0) :- !.
numNegativeLiterals([n(_)|T], R) :- numNegativeLiterals(T, S), R is S + 1, !.
numNegativeLiterals([_|T], R) :- numNegativeLiterals(T, R), !.

checkOnePositiveAndAllNegative(C) :- C \= [], 
                                     numNegativeLiterals(C, Neg),
                                     length(C, Len),
    								 A is Len - 1,
                                     Neg == A.

getPositiveLiteral([n(_)|T], Res) :- getPositiveLiteral(T, Res), !.
getPositiveLiteral([H|_], H) :- !.

getAllLiteralsAux([], []) :- !.
getAllLiteralsAux([n(H)|T], [H|Res]) :- getAllLiteralsAux(T, Res), !.
getAllLiteralsAux([H|T], [H|Res]) :- getAllLiteralsAux(T, Res), !.

getAllLiterals(L, Res) :- getAllLiteralsAux(L, Aux), 
                          sort(Aux, Res).

getAllLiteralsFromAllClausesAux([], []) :- !.
getAllLiteralsFromAllClausesAux([H|T], Res) :- getAllLiterals(H, A),
                                               getAllLiteralsFromAllClausesAux(T, R), 
                                               append(A, R, Res), !.

getAllLiteralsFromAllClauses(L, Res) :- getAllLiteralsFromAllClausesAux(L, Aux), 
                                        sort(Aux, Res).

checkAllNegativeAreSolved([], _) :- !.
checkAllNegativeAreSolved([H|T], M) :- member((H, solved), M),
                                        checkAllNegativeAreSolved(T, M), !.

findInKBonePositiveAndAllNegative([], _, []).
findInKBonePositiveAndAllNegative([H|_], M, H) :- checkOnePositiveAndAllNegative(H),
                                                  getPositiveLiteral(H, Res),
                                                  member((Res, unsolved), M),
                                                  getAllLiterals(H, All),
                                                  delete(All, Res, Neg),
                                                  checkAllNegativeAreSolved(Neg, M),
                                                  !.
findInKBonePositiveAndAllNegative([_|T], M, Res) :- findInKBonePositiveAndAllNegative(T, M, Res), !.

forwardChaining(G, M, _) :- checkAllOfTheGoalsAreSolved(G, M), !.
forwardChaining(G, M, KB) :- findInKBonePositiveAndAllNegative(KB, M, Res), 
                             Res \= [],
                             getPositiveLiteral(Res, Lit),
                             delete(M, (Lit, unsolved), Aux1),
                             append(Aux1, [(Lit, solved)], Aux2),
                             forwardChaining(G, Aux2, KB).

markAllLiteralsAsUnsolved([], []) :- !.
markAllLiteralsAsUnsolved([H|T], [(H, unsolved)|Res]) :- markAllLiteralsAsUnsolved(T, Res), !.
 




hasPneumoniaBackwardChaining(LC) :- backwardChaining([p], LC, LC),
 								    write('Backward Chaining: '), nl, 
    				                write('The patient has pneumonia'), nl, !.
hasPneumoniaBackwardChaining(_) :- write('Backward Chaining: '), nl, 
                                   write('patient is ok'), nl.

hasPneumoniaForwardChaining(LC) :- append(LC, [[p]], AllC),
                                   getAllLiteralsFromAllClauses(AllC, Literals),
                                   markAllLiteralsAsUnsolved(Literals, A),
                                   forwardChaining([p], A, LC),
 								   write('Forward Chaining: '), nl, 
    				               write('The patient has pneumonia'), nl, !.
hasPneumoniaForwardChaining(_) :- write('Forward Chaining: '), nl, 
                                  write('patient is ok'), nl.

read :-
    write('What is patient temperature? (answer is a number)'),
    prompt(_, 'Type a temperature'),
    read(Temperature),
   
    write('For how many days has the patient been sick? (answer is a number)'),
    prompt(_, 'Type the number of days'),
    read(Num_days),
   
    write('Has patient cough? (answer is yes/no)'),
    prompt(_, 'Type yes/no'),
    read(Has_cough),
   
    temperatureHeigerThen38(Temperature, Th),
    patientWasSickForAtLeast2Days(Num_days, Sr),
    hasCough(Has_cough, Ch),

    see('C:\\Users\\Marian Lupascu\\Documents\\Documente\\FMI\\MI\\Sem I\\KnowRepr&Reason\\Lab\\KB.txt'),
    read(L),
    seen,
    write(L),
    nl,
    
    updateLwithTemperatureHeigerThen38(Th, L, LT),
    updateLwithPatientWasSickForAtLeast2Days(Sr, LT, LS),
    updateLwithHasCough(Ch, LS, LC),
    
    write(LC), nl,
    
    hasPneumoniaBackwardChaining(LC),
    hasPneumoniaForwardChaining(LC),
 
    nl,
    write('Do you want to continue? (the answer for no is stop)'),
    prompt(_, 'Type stop for no'),
    read(Continue),
    (   Continue == stop
    ->  true
    ;  
        read
    ).

main :- read.