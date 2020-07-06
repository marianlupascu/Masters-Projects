temperatureHeigerThen38(Temperature, true) :- Temperature > 38, !.
temperatureHeigerThen38(_, false).
 
patientWasSickForAtLeast2Days(Num_days, true) :- Num_days > 2, !.
patientWasSickForAtLeast2Days(_, false).
 
hasMusclePain(yes, true).
hasMusclePain(no, false).

hasCough(yes, true).
hasCough(no, false).

updateLwithTemperatureHeigerThen38(true, L, NL) :- append(L, [[[], [th]]], NL), !.
updateLwithTemperatureHeigerThen38(_, L, L).

updateLwithPatientWasSickForAtLeast2Days(true, L, NL) :- append(L, [[[], [sr]]], NL), !.
updateLwithPatientWasSickForAtLeast2Days(_, L, L).

updateLwithMusclePain(true, L, NL) :- append(L, [[[], [mp]]], NL), !.
updateLwithMusclePain(_, L, L).

updateLwithHasCough(true, L, NL) :- append(L, [[[], [c]]], NL), !.
updateLwithHasCough(_, L, L).





checkAllOfTheGoalsAreSolved([], _).
checkAllOfTheGoalsAreSolved([H|T], L) :- member((H, solved), L), 
                                         checkAllOfTheGoalsAreSolved(T, L), !.
numNegativeLiterals([], 0) :- !.
numNegativeLiterals([n(_)|T], R) :- numNegativeLiterals(T, S), R is S + 1, !.
numNegativeLiterals([_|T], R) :- numNegativeLiterals(T, R), !.

getPositiveLiteral([n(_)|T], Res) :- getPositiveLiteral(T, Res), !.
getPositiveLiteral([H|_], H) :- !.

getAllLiteralsAux([], []) :- !.
getAllLiteralsAux([n(H)|T], [H|Res]) :- getAllLiteralsAux(T, Res), !.
getAllLiteralsAux([H|T], [H|Res]) :- getAllLiteralsAux(T, Res), !.

getAllLiterals(L, Res) :- getAllLiteralsAux(L, Aux), 
                          sort(Aux, Res).

getAllLiteralsFromAllClausesAux([], []) :- !.
getAllLiteralsFromAllClausesAux([[Ip|[Cl]]|T], Res2) :- getAllLiterals(Ip, A),
                                                      getAllLiterals(Cl, B),
                                                      getAllLiteralsFromAllClausesAux(T, R), 
                                                      append(A, R, Res1),
                                                      append(B, Res1, Res2), !.

getAllLiteralsFromAllClauses(L, Res) :- getAllLiteralsFromAllClausesAux(L, Aux), 
                                        sort(Aux, Res).

checkAllNegativeAreSolved([], _) :- !.
checkAllNegativeAreSolved([H|T], M) :- member((H, solved), M),
                                       checkAllNegativeAreSolved(T, M), !.

findInKBonePositiveAndAllNegative([[Ip|[Cl]]|_], M, [Ip|[Cl]]) :- length(Cl, 1),
                                            			          [Res] = Cl,
                                                                  member((Res, unsolved), M),
                                                                  getAllLiterals(Ip, All),
                                                                  checkAllNegativeAreSolved(All, M),
                                                                  !.
findInKBonePositiveAndAllNegative([_|T], M, Res) :- findInKBonePositiveAndAllNegative(T, M, Res), !.

resetFile :- tell('C:\\Users\\Marian Lupascu\\Documents\\Documente\\FMI\\MI\\Sem I\\KnowRepr&Reason\\Lab\\WM.txt'),
             told.

writeWM(WM) :- write(WM), 
               nl.

forwardChaining(G, M, _) :- checkAllOfTheGoalsAreSolved(G, M), writeWM(M),!.
forwardChaining(G, M, KB) :- findInKBonePositiveAndAllNegative(KB, M, Res), 
                             Res \= [],
                             [_|[[Cl]]] = Res,
                             delete(M, (Cl, unsolved), Aux1),
                             append(Aux1, [(Cl, solved)], Aux2),
    						 writeWM(Aux2),
                             forwardChaining(G, Aux2, KB).

markAllLiteralsAsUnsolved([], []) :- !.
markAllLiteralsAsUnsolved([H|T], [(H, unsolved)|Res]) :- markAllLiteralsAsUnsolved(T, Res), !.
 




hasPneumoniaForwardChaining(LC, Stream_console, Stream_file) :- append(LC, [[[], [p]]], AllC),
                                                                getAllLiteralsFromAllClauses(AllC, Literals),
                                                                markAllLiteralsAsUnsolved(Literals, A),
                                                                set_output(Stream_file),
                                                                writeWM(A),
                                                                forwardChaining([p], A, LC),
                                                                close(Stream_file),
                                                                set_output(Stream_console),
 								                                write('Forward Chaining: '), nl, 
    				                                            write('The patient has pneumonia'), nl, !.
hasPneumoniaForwardChaining(_, Stream_console, Stream_file) :- close(Stream_file),
                                                               set_output(Stream_console),
                                                               write('Forward Chaining: '), nl, 
                                                               write('The patient is ok (pneumonia)'), nl.

hasFluForwardChaining(LC) :- append(LC, [[[], [flu]]], AllC),
                             getAllLiteralsFromAllClauses(AllC, Literals),
                             markAllLiteralsAsUnsolved(Literals, A),
                             writeWM(A),
                             forwardChaining([flu], A, LC),
 			                 write('Forward Chaining: '), nl, 
    				         write('The patient has flu'), nl, !.
hasFluForwardChaining(_) :- write('Forward Chaining: '), nl, 
                            write('The patient is ok (flu)'), nl.

read :-
    write('What is patient temperature? (answer is a number)'),
    prompt(_, 'Type a temperature'),
    read(Temperature),
   
    write('For how many days has the patient been sick? (answer is a number)'),
    prompt(_, 'Type the number of days'),
    read(Num_days),
    
    write('Has patient muscle pain? (answer is yes/no)'),
    prompt(_, 'Type yes/no'),
    read(Muscle_pain),
   
    write('Has patient cough? (answer is yes/no)'),
    prompt(_, 'Type yes/no'),
    read(Has_cough),
   
    temperatureHeigerThen38(Temperature, Th),
    patientWasSickForAtLeast2Days(Num_days, Sr),
    hasMusclePain(Muscle_pain, Mp),
    hasCough(Has_cough, Ch),

    resetFile,
    current_output(Stream_console),
    open('C:\\Users\\Marian Lupascu\\Documents\\Documente\\FMI\\MI\\Sem I\\KnowRepr&Reason\\Lab\\WM.txt', 'update', Stream_file),

    see('C:\\Users\\Marian Lupascu\\Documents\\Documente\\FMI\\MI\\Sem I\\KnowRepr&Reason\\Lab\\KB2.txt'),
    read(L),
    read(_),
    seen,
    write(L),
    nl,
    
    updateLwithTemperatureHeigerThen38(Th, L, LT),
    updateLwithPatientWasSickForAtLeast2Days(Sr, LT, LS),
    updateLwithMusclePain(Mp, LS, LM),
    updateLwithHasCough(Ch, LM, LC),
    
    write(LC), nl,
    
    hasPneumoniaForwardChaining(LC, Stream_console, Stream_file),
    %hasFluForwardChaining(LC),
 
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