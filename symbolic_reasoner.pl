/*
Student Name: Tshering Sherpa
Student FAN: sher0304
File: symbolic_reasoner.pl
Date: 19-11-2025
Description: Symbolic AI subsystem for crime hotspot reasoning and classification
*/

:- dynamic historical_average/5.
:- consult('crime_averages.pl').

% Rule Base for Hotspot Classification
% Using historical_average(Suburb, CrimeType, Year, Quarter, AverageIncidents) as facts

% Rule 1: Low Risk Area (most specific - check small numbers first)
classify_hotspot(_, _, PredictedCount, 'Low Risk', Justification) :-
    PredictedCount < 5,
    format(atom(Justification), 
           'Predicted incidents (~w) are below absolute risk threshold of 5', 
           [PredictedCount]).

% Rule 2: Significant Hotspot Classification (check 3x before 2x)
classify_hotspot(Suburb, CrimeType, PredictedCount, 'Significant Hotspot', Justification) :-
    historical_average(Suburb, CrimeType, Year, Quarter, HistoricalAvg),
    PredictedCount >= 3 * HistoricalAvg,
    PredictedCount >= 10,
    format(atom(Justification), 
           'Predicted incidents (~w) are more than 3x the historical average (~w) and exceed absolute threshold of 10', 
           [PredictedCount, HistoricalAvg]).

% Rule 3: Emerging Hotspot Classification (check 2x before critical)
classify_hotspot(Suburb, CrimeType, PredictedCount, 'Emerging Hotspot', Justification) :-
    historical_average(Suburb, CrimeType, Year, Quarter, HistoricalAvg),
    PredictedCount >= 2 * HistoricalAvg,
    PredictedCount >= 5,
    format(atom(Justification), 
           'Predicted incidents (~w) are 2-3x the historical average (~w) indicating emerging concern', 
           [PredictedCount, HistoricalAvg]).

% Rule 4: Critical Hotspot (moved down - least specific)
classify_hotspot(Suburb, CrimeType, PredictedCount, 'Critical Hotspot', Justification) :-
    PredictedCount >= 50,
    format(atom(Justification), 
           'Predicted incidents (~w) exceed critical threshold of 50 requiring immediate attention', 
           [PredictedCount]).

% Rule 5: Stable Area Classification
classify_hotspot(Suburb, CrimeType, PredictedCount, 'Stable', Justification) :-
    historical_average(Suburb, CrimeType, Year, Quarter, HistoricalAvg),
    PredictedCount < 2 * HistoricalAvg,
    format(atom(Justification), 
           'Predicted incidents (~w) are within normal range compared to historical average (~w)', 
           [PredictedCount, HistoricalAvg]).

% Default rule if no specific conditions met or historical average not present
classify_hotspot(Suburb, CrimeType, PredictedCount, 'Needs Review', Justification) :-
    \+ historical_average(Suburb, CrimeType, _, _, _),
    format(atom(Justification), 
           'Prediction of ~w incidents for ~w, ~w requires manual review or historical average not available', 
           [PredictedCount, Suburb, CrimeType]).
           
% Main reasoning predicate with Year and Quarter parameters
reason_about_prediction(Suburb, CrimeType, Year, Quarter, PredictedCount, Classification, Justification) :-
    (   classify_hotspot(Suburb, CrimeType, PredictedCount, Classification, Justification)
    ).

% Demo predicate for automated testing
demo :-
    write('=== Crime Hotspot Reasoning System Demo ==='), nl, nl,
    % Test case 1: Significant/Critical hotspot
    write('Test Case 1: Significant or Critical Hotspot'), nl,
    reason_about_prediction('ADELAIDE', 'THEFT AND RELATED OFFENCES', 2025, 3, 150, Classification1, Justification1),
    write('Classification: '), write(Classification1), nl,
    write('Justification: '), write(Justification1), nl, nl,
    % Test case 2: Emerging hotspot
    write('Test Case 2: Emerging Hotspot'), nl,
    reason_about_prediction('PORT AUGUSTA', 'ACTS INTENDED TO CAUSE INJURY', 2025, 3, 45, Classification2, Justification2),
    write('Classification: '), write(Classification2), nl,
    write('Justification: '), write(Justification2), nl, nl,
    % Test case 3: Stable area
    write('Test Case 3: Stable Area'), nl,
    reason_about_prediction('MOUNT GAMBIER', 'PROPERTY DAMAGE AND ENVIRONMENTAL', 2025, 3, 8, Classification3, Justification3),
    write('Classification: '), write(Classification3), nl,
    write('Justification: '), write(Justification3), nl, nl,
    % Test case 4: Low risk
    write('Test Case 4: Low Risk'), nl,
    reason_about_prediction('ADELAIDE', 'FRAUD DECEPTION AND RELATED OFFENCES', 2025, 3, 3, Classification4, Justification4),
    write('Classification: '), write(Classification4), nl,
    write('Justification: '), write(Justification4), nl, nl.

