# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 10:27:53 2018

@author: Saketh
"""
import tbaUtils

def makeMatchList():
    '''
    Get match list from the Blue Alliance website depending on what event we're 
    going to. Format it and write it to a file. Have that read by the Scouting 
    Program and have formatted so that other scouting software can use it.
    '''
    pass

def readMatchList():
    '''
    Read the Match List file created by makeMatchList. 
    '''
    pass

def readScout():
    '''
    Read Scouting Data from a file, fix formatting to numeric where neccessary,
    clean the data, report any implausibile data.  
    '''
    pass 

def FindPartners(MatchList):
    '''
    Takes the Match List from the entire competition and finds the matches we're
    in and finds the teams that are with us.
    '''
    pass

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