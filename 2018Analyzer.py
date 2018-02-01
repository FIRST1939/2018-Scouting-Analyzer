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
   

def readScout():
    '''
    Read Scouting Data from a file, fix formatting to numeric where neccessary,
    clean the data, report any implausibile data.  
    '''
    with open('FAKE-DATA-1-TEAM.csv', 'r') as ScoutFile:
        ScoutData = pd.read_csv(ScoutFile) 
    print(ScoutData)
    return ScoutData
    

def FindPartners(Matchlist, team = 1939):
    
    '''
    Takes the Match List from the entire competition and finds the matches we're
    in and finds the teams that are with us.
    '''
    for match in Matchlist:
        if team in match[1:]:
            print(match)
            if team in match[1:4]:
                alliance = 'blue'
                opposing = 'red'
                allies = match[1:4]
                opponents = match[4:7]
                allies.remove(team)
            
                
            else:
                alliance = 'red'
                opposing = 'blue'
                allies = match[4:7]
                opponents = match[1:4]
                allies.remove(team)
            
            
            print(alliance, allies, opposing, opponents)
            
def MatchReport(Scoutdf):
    ''' (dataframe)->dataframe
    (Scouting Data)->PivotTable with upcoming match partners
    Take the scouting data, trim down to only partners and opponents.
    Create a report by match showing partners and opponents.
    '''
    pass

def Day1Report(Scoutdf):
    '''(dataframe)->None
    Take Scouting data and analyze it by creating a report that will be presented
    at the Day 1 Scouting meeting
    '''
    pass

def SearchTeam(Scoutdf, TeamNumber):
    '''
    A Search function where we can find a team and their specific stats.
    '''
    pass

def PickList():
    '''
    List of teams organized by the order we should pick them. Then catagories 
    that rank robotics based on that catagory. Do not pick catagory.
    '''
    pass