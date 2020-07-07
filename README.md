# sharedVocGroup
Measures of shared vocabulary for multi-party groups


1. Build the corpus : 

    For each conversation and for each locuteur in the conversation 
        build files focusing on one specific locutor 
            L vs X, where X is the rest of the locutors of the group
            
            For example in a conversation with 4 participants (A, B, C, D), we build 4 files : 
                - A vs X : the first one with A's speech turn, the other participants' speech turns (B, C, D) will be noted X
                - B vs X : the second one with B's speech turn, the other participants' speech turns (A, C, D) will be noted X
                - C vs X : the third one with C's speech turn, the other participants' speech turns (A, B, D) will be noted X
                - D vs X : the fourth one with D's speech turn, the other participants' speech turns (A, B, C) will be noted X 
                

2. Run Dialign on the corpus

output obtained : 
- dial-synthesis.csv : results for the measures applied on all the files of the corpus
- for each file : 
    -> the lexicon of the repeated expressions
    -> the annotated dialogue

For more detailled about the output, see Dialign documentation


3. From the results of dialign : 

--> Build the shared lexicon of the group: 

By processing conversations L vs X, 
