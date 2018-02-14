# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 10:27:53 2018

@author: Saketh
"""
import tbaUtils
import pandas as pd
import numpy as np
from pprint import pprint

def makeMatchList(event, year = 2018):
    '''
    Get match list from the Blue Alliance website depending on what event we're 
    going to. Format it and write it to a file. Have that read by the Scouting 
    Program and have formatted so that other scouting software can use it.
    '''
    RawMatches = tbaUtils.get_event_matches(event, year) 

    pprint(RawMatches[0:2])
    
    print()
    MatchList = []
    for Match in RawMatches:
        
        ShortMatch = []
        #Some of these matches are not quals, need to filter out non qm eventually
        MatchNum = Match['match_number']
        ShortMatch.append(MatchNum)
        
        for team in Match['alliances']['blue']['teams']:
        
            ShortMatch.append(int(team[3:]))
        
        for team in Match['alliances']['red']['teams']:
            
            ShortMatch.append(int(team[3:])) 
            
        comp_level = Match['comp_level']
        if comp_level == 'qm':
            MatchList.append(ShortMatch)
      
    print()
    MatchList.sort()
    pprint(MatchList)    


    with open('MatchList.csv', 'w') as File:
        for Match in MatchList : 
            Outstr = str(Match).replace('[', '').replace(']', '').replace(' ', '')+'\n'
            File.write(Outstr)

def readMatchList():
    
    '''
    Read the Match List file created by makeMatchList. 
    
    '''
    
    with open('MatchList.csv', 'r') as Matchlist:
       data = Matchlist.readlines()
   
   
    result = []
    for line in data:
        line = line.replace('\n' , '')
        dataresult = line.split(',')
        for idx in range(len(dataresult)):
            dataresult[idx] = int(dataresult[idx])
            
        result.append(dataresult)
        
    return result

'''
def readTeamMatches(TeamNumber):
    data = FindPartners(readMatchList(), TeamNumber)
    output = []
    for i in range(0, len(data)):
        matchData = data[i]
        print(matchData, type(matchData))
        match = matchData['3']
        output.append(match)
    return output
'''
def readScout():
    '''
    Read Scouting Data from a file, fix formatting to numeric where neccessary,
    clean the data, report any implausibile data.  
    '''
    with open('fake-data-6-team.csv', 'r') as ScoutFile:
        ScoutData = pd.read_csv(ScoutFile, sep = '|') 
    Result = ScoutData.fillna(value = 0)
    return Result
    

def FindPartners(Matchlist, team = 1939):
    
    '''
    Takes the Match List from the entire competition and finds the matches we're
    in and finds the teams that are with us.
    '''
    result = []
    for match in Matchlist:
        thisMatch = {}
        if team in match[1:]:
         #   print(match)
            if team in match[1:4]:
                thisMatch['alliance'] = 'blue'
                thisMatch['opposing'] = 'red'
                allies = match[1:4]
                thisMatch['opponents'] = match[4:7]
                allies.remove(team)
                thisMatch['allies'] = allies
            
                
            else:
                thisMatch['alliance'] = 'red'
                thisMatch['opposing'] = 'blue'
                allies = match[4:7]
                thisMatch['opponents'] = match[1:4]
                allies.remove(team)
                thisMatch['allies'] = allies
            
            thisMatch['match'] = match[0] 
            result.append(thisMatch)
            
    return result
            
def MatchReport(MatchList, PivotDf, Scoutdf, TeamNumber):
    ''' (dataframe)->dataframe
    (Scouting Data)->PivotTable with upcoming match partners
    Take the scouting data, trim down to only partners and opponents.
    Create a report by match showing partners and opponents.
    '''
    #if MatchList in readScout()
     #   print(MatchList['allies'])
    #index = pd.Index([MatchList])
    #if 'allies' in index:
    print(MatchList)
    print(MatchList[0]['allies'])
    LastScouted = max(Scoutdf['match'])
    
    for match in MatchList:
        if match['match'] > LastScouted:
            print('match', match['match'])
            print('\nallies')
            for ally in match['allies']:
                SearchTeam(Scoutdf, PivotDf, ally)
                print()
            return
    
    
    

    
    
def Day1Report(Scoutdf):
    '''(dataframe)->None
    Take Scouting data and analyze it by creating a report that will be presented
    at the Day 1 Scouting meeting
    '''
    pass

def SearchTeam(Scoutdf, PivotDf, TeamNumber):
    '''
    A Search function where we can find a team and their specific stats.
    '''
   # print(PivotDf['totalmatches'])
    print('Team:', TeamNumber)
    PivotDf.reset_index(inplace = True)
    PivotDf.set_index('team', inplace = True)
    print('Matches Played =', PivotDf.loc[TeamNumber]['totalmatches'])
    
    print('\nMatch Summary')
    print(PivotDf.loc[TeamNumber])
    print('\nMatch Details')
    
   #print(PivotDf[PivotDf.team == TeamNumber]['PositiveComments'])
    print(Scoutdf[Scoutdf.team == TeamNumber])
    
    
    
    
    
def TeamStats(TeamDf):
    '''
    Takes full dataframe, and creates per match calculated values. Creates a pivot
    dataframe with overall team statistics
    '''
    
    TeamDf['avgtelecubes'] = TeamDf['teleBoxToSwitchCount'] + TeamDf['teleBoxToScaleCount'] 
    TeamDf['avgtelecubes'] += TeamDf['teleBoxToExchangeCount'] 
    TeamDf['avgtelecubes'] += TeamDf['teleBoxToOpponentSwitchCount']
  
    TeamDf['avgautocubes'] = TeamDf['autoBoxToSwitchCount'] + TeamDf['autoBoxToWrongSwitchCount']
    TeamDf['avgautocubes'] += TeamDf['autoBoxToScaleCount']
    TeamDf['avgautocubes'] += TeamDf['autoBoxToWrongScaleCount']
    
    TeamDf['totalclimbs'] = TeamDf['endClimbedCenter'] + TeamDf['endClimbedSide']
    TeamDf['totalclimbs'] = TeamDf['endClimbedRamp'] + TeamDf['endDeployRamp']
    
    #TeamDf['PostiveComments'] = TeamDf['postCommentsPro'] 
    
    TeamDf['totalmatches'] = TeamDf['team'] 
    
    AvgTeamPivot = pd.pivot_table(TeamDf, values = ['avgtelecubes', 'avgautocubes'], index = 'team', aggfunc = np.average)
    MatchCount = pd.pivot_table(TeamDf, values = ['totalmatches', 'totalclimbs'], index = 'team', aggfunc = np.count_nonzero)
    #Comments = pd.pivot_table(TeamDf, values = ['PositiveComments'], index = 'team', aggfunc = lambda x: ' '.join(x))
    
    AvgTeamPivot.reset_index(inplace = True)
    MatchCount.reset_index(inplace = True)
    #Comments.reset_index(inplace = True)

    TeamPivot = pd.merge(AvgTeamPivot, MatchCount, on = 'team')
    
   

    
    return TeamDf, TeamPivot

def PickList():
    '''
    List of teams organized by the order we should pick them. Then catagories 
    that rank robotics based on that catagory. Do not pick catagory.
    '''
    pass

def enterTeam():
     Team = input('enter team number: ')
     if Team.isdigit():
        Team = int(Team)
        return Team
     else:
        print('input error')
        return
    
def Main():
    print('press 1 to acquire a Match List')
    print('press 2 to get a prematch Scouting Report')
    print('press 3 to get a single team report')
    selection = input('enter number: ')
    
    if selection == '1':
        event = input('enter event code: ')
        makeMatchList(event, 2017)
    elif selection == '2':
        Team = enterTeam()       
        ReadData = readScout()
        MatchList = readMatchList()
        TeamDf, PivotDf = TeamStats(ReadData)
        Partners = FindPartners(MatchList, Team)
        #matchNum = FindPartners(MatchList, Team)
        MatchReport(Partners, PivotDf, TeamDf, Team)
        
    elif selection == '3':
        Team = int(enterTeam())       
        ReadData = readScout()
        MatchList = readMatchList()
        TeamDf, PivotDf = TeamStats(ReadData)
        SearchTeam(TeamDf, PivotDf, Team)
Main()
      
                
                      
                     







