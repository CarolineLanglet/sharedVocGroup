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
                

2. Run Dialign on the corpus for offline and speaker-centered measures : 

output obtained (for more details about output see the dialign documetation)
- dial-synthesis.csv : results for the measures applied on all the files of the corpus. The speaker-centered measures in the file are relevant for an analysis of the shared vocabulary between speaker S and the rest of the group (Offline and )
- for each file : 
    -> the lexicon of the repeated expressions (shared vocabulary between the speaker S and the rest of the group)
    -> the annotated dialogue
 

3. Building the shared lexicon of the group from the results of dialign : 
   - Script : getSharedLexiconGroup.py
   - Input : output directory of dialign (file-dialogue.txt and file-lexicon.txt)
   - Output : directory (shLexiconGlobal) containing 1 file of the shared vocabulary for each conversation. 

4. Applying offline and group-centered measures
   - Script : offlineGpMeasures.py
   - Input : shLexiconGlobal (directory obtained at stage 3. Building the shared lexicon of the group)
   - Output : synthesisGlobalAllConv.csv contained the results of the offline group-centered measures for all the conversations. 

5. Applying online measures : 
    - Script : onlineMeasures.py
    - Input : output directory of dialign (file-dialogue.txt and file-lexicon.txt) AND shLexiconGlobal directory obtained at stage 3. 
    - Output : resultsOnLine.csv containing the results of the online measures. 
