#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import requests
import json
import pyodbc

from bs4 import BeautifulSoup
from os import getenv

#API COMET
api_user    = 'diegogonzalez'
api_pass    = 'diegogonzalezCON'
api_fifa    = '39393'
api_anho    = '2019'

#DEFAULT
base_con    = 'Driver={SQL Server};Server=CEROUNO-PC-01\MSSQLEXPRESS2016;Database=SMBIANCAV20;Trusted_Connection=yes;'
base_url    = 'https://api.analyticom.de/api/export/comet/'
headers     = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'es-ES,es;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '4',
        'Content-Type': 'application/json; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0'
    }

def getCompetitions():
    try:
        str_connection  = pyodbc.connect(base_con)
        str_cursor      = str_connection.cursor()
        
        try:
            JSONurl     = base_url + 'competitions?organisationFifaIds='+api_fifa+'&season='+api_anho
            JSONResponse= requests.get(JSONurl, auth=(api_user, api_pass), headers=headers, timeout=10).json()
            
            for JSONData in JSONResponse:
                _competitionFifaId          = JSONData['competitionFifaId']
                _ageCategory                = JSONData['ageCategory'].upper().strip()
                _ageCategoryName            = JSONData['ageCategoryName'].upper().strip()
                _dateFrom                   = JSONData['dateFrom']
                _dateTo                     = JSONData['dateTo']
                _discipline                 = JSONData['discipline'].upper().strip()
                _gender                     = JSONData['gender'].upper().strip()
                _internationalName          = JSONData['internationalName'].upper().strip()
                _internationalShortName     = JSONData['internationalShortName'].upper().strip()
                _imageId                    = JSONData['imageId']
                _multiplier                 = JSONData['multiplier']
                _nature                     = JSONData['nature'].upper().strip()
                _numberOfParticipants       = JSONData['numberOfParticipants']
                _orderNumber                = JSONData['orderNumber']
                _organisationFifaId         = JSONData['organisationFifaId']
                _season                     = JSONData['season']
                _status                     = JSONData['status'].upper().strip()
                _teamCharacter              = JSONData['teamCharacter'].upper().strip()
                _superiorCompetitionFifaId  = JSONData['superiorCompetitionFifaId']
                _pictureContentType         = JSONData['picture']['contentType']
                _pictureLink                = JSONData['picture']['pictureLink']
                _pictureValue               = JSONData['picture']['value']
                _flyingSubstitutions        = JSONData['flyingSubstitutions']
                _penaltyShootout            = JSONData['penaltyShootout']
                _matchType                  = JSONData['matchType'].upper().strip()
                
                str_select      = "SELECT * FROM [SMBIANCAV20].[comet].[competitions] WHERE competitionFifaId = ?"
                str_cursor.execute(str_select, (_competitionFifaId))
                str_row         = str_cursor.fetchone()

                if str_row:
                    str_query   = "UPDATE [SMBIANCAV20].[comet].[competitions] SET organisationFifaId = ?, superiorCompetitionFifaId = ?, status = ?, internationalName = ?, internationalShortName = ?, season = ?, ageCategory = ?, ageCategoryName = ?, dateFrom = ?, dateTo = ?, discipline = ?, gender = ?, imageId = ?, multiplier = ?, nature = ?, numberOfParticipants = ?, orderNumber = ?, teamCharacter = ?, flyingSubstitutions = ?, penaltyShootout = ?, matchType = ?, pictureContentType = ?, pictureLink = ?, pictureValue = ?, lastUpdate = GETDATE() WHERE competitionFifaId = ?"
                    str_cursor.execute(str_query, (_organisationFifaId, _superiorCompetitionFifaId, _status, _internationalName, _internationalShortName, _season, _ageCategory, _ageCategoryName, _dateFrom, _dateTo, _discipline, _gender, _imageId, _multiplier, _nature, _numberOfParticipants, _orderNumber, _teamCharacter, _flyingSubstitutions, _penaltyShootout, _matchType, _pictureContentType, _pictureLink, _pictureValue, _competitionFifaId))
                else:
                    str_query   = "INSERT INTO [SMBIANCAV20].[comet].[competitions] (competitionFifaId, organisationFifaId, superiorCompetitionFifaId, status, internationalName, internationalShortName, season, ageCategory, ageCategoryName, dateFrom, dateTo, discipline, gender, imageId, multiplier, nature, numberOfParticipants, orderNumber, teamCharacter, flyingSubstitutions, penaltyShootout, matchType, pictureContentType, pictureLink, pictureValue, lastUpdate) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, GETDATE())"
                    str_cursor.execute(str_query, (_competitionFifaId, _organisationFifaId, _superiorCompetitionFifaId, _status, _internationalName, _internationalShortName, _season, _ageCategory, _ageCategoryName, _dateFrom, _dateTo, _discipline, _gender, _imageId, _multiplier, _nature, _numberOfParticipants, _orderNumber, _teamCharacter, _flyingSubstitutions, _penaltyShootout, _matchType, _pictureContentType, _pictureLink, _pictureValue))
                
                str_connection.commit()

        except requests.ConnectionError as err:
            print('Error getCompetitions => ', err)

        finally:
            print('Finally getCompetitions')

    except pyodbc.Error as err:
        print('Error MSSQL => ', err)

    finally:
        print('Finally MSSQL Connection')
        str_cursor.close()
        str_connection.close()

if __name__ == "__main__":
    getCompetitions()
