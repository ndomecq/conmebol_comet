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
api_comp    = '30205939'
api_anho    = '2019'

#DEFAULT
#base_con    = 'Driver={SQL Server};Server=CEROUNO-PC-01\MSSQLEXPRESS2016;Database=SMBIANCAV20;Trusted_Connection=yes;'
base_con    = 'Driver={SQL Server};Server=PC-CZELAYA\SQLEXPRESS2014;Database=SMBIANCAV20;Trusted_Connection=yes;'
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

def getOrganisations(var01, var02, var03, var04):
    try:
        str_connection  = pyodbc.connect(base_con)
        str_cursor      = str_connection.cursor()

        str_query00     = "SELECT * FROM [SMBIANCAV20].[comet].[organisations] WHERE organisationFifaId = ?"
        str_cursor.execute(str_query00, (var01))
        str_row00       = str_cursor.fetchone()

        if str_row00 == False:
            str_query   = "INSERT INTO [SMBIANCAV20].[comet].[organisations] (organisationFifaId, organisationName, organisationNature, organisationShortName, lastUpdate) VALUES (?, ?, ?, ?, GETDATE())"
            str_cursor.execute(str_query, (var01, var02, var03, var04))

        str_connection.commit()
    except pyodbc.Error as err:
        print('getOrganisations(): Error MSSQL => ', err)

    finally:
        str_cursor.close()
        str_connection.close()

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
            print('getCompetitions(): Error => ', err)

    except pyodbc.Error as err:
        print('getCompetitions: Error MSSQL => ', err)

    finally:
        str_cursor.close()
        str_connection.close()

def getTeams():
    try:
        str_connection  = pyodbc.connect(base_con)
        str_cursor      = str_connection.cursor()

        str_query00     = "SELECT competitionFifaId FROM [SMBIANCAV20].[comet].[competitions] WHERE season = ?"
        str_cursor.execute(str_query00, (api_anho))
        str_row00       = str_cursor.fetchall()

        for row00 in str_row00:
            try:
                JSONurl     = base_url + 'competition/' + str(row00[0]) + '/teams'
                JSONResponse= requests.get(JSONurl, auth=(api_user, api_pass), headers=headers).json()
                
                for JSONData in JSONResponse:
                    _teamFifaId                 = JSONData['teamFifaId']
                    _competitionFifaId          = JSONData['competitionFifaId']
                    
                    if JSONData['organisationFifaId']:
                        _organisationFifaId         = JSONData['organisationFifaId']
                        getOrganisations(JSONData['organisationFifaId'], JSONData['organisationName'], JSONData['organisationShortName'], JSONData['organisationShortName'])
                    else:
                        _organisationFifaId         = 1

                    _facilityFifaId             = JSONData['facilityFifaId']

                    if JSONData['status']:
                        _status                 = JSONData['status'].upper().strip()
                    else:
                        _status                 = JSONData['status']

                    if JSONData['internationalName']:
                        _internationalName      = JSONData['internationalName'].upper().strip()
                    else:
                        _internationalName      = JSONData['internationalName']

                    if JSONData['internationalShortName']:
                        _internationalShortName = JSONData['internationalShortName'].upper().strip()
                    else:
                        _internationalShortName = JSONData['internationalShortName']

                    if JSONData['organisationNature']:
                        _organisationNature     = JSONData['organisationNature'].upper().strip()
                    else:
                        _organisationNature     = JSONData['organisationNature']

                    if JSONData['country']:
                        _country                = JSONData['country'].upper().strip()
                    else:
                        _country                = JSONData['country']

                    if JSONData['region']:                        
                        _region                 = JSONData['region'].upper().strip()
                    else:
                        _region                 = JSONData['region']

                    if JSONData['town']:
                        _town                   = JSONData['town'].upper().strip()
                    else:
                        _town                   = JSONData['town']
                    
                    if JSONData['postalCode']:
                        _postalCode             = JSONData['postalCode'].upper().strip()
                    else:
                        _postalCode             = JSONData['postalCode']

                    str_query01     = "SELECT * FROM [SMBIANCAV20].[comet].[teams] WHERE teamFifaId = ?"
                    str_cursor.execute(str_query01, (_teamFifaId))
                    str_row01       = str_cursor.fetchone()

                    if str_row01:
                        str_query11 = "UPDATE [SMBIANCAV20].[comet].[teams] SET organisationFifaId = ?, facilityFifaId = ?, status = ?, internationalName = ?, internationalShortName = ?, organisationNature = ?, country = ?, region = ?, town = ?, postalCode = ?, lastUpdate = GETDATE() WHERE teamFifaId = ?"
                        str_cursor.execute(str_query11, (_organisationFifaId, _facilityFifaId, _status, _internationalName, _internationalShortName, _organisationNature, _country, _region, _town, _postalCode, _teamFifaId))
                    else:
                        str_query11 = "INSERT INTO [SMBIANCAV20].[comet].[teams] (teamFifaId, organisationFifaId, facilityFifaId, status, internationalName, internationalShortName, organisationNature, country, region, town, postalCode, lastUpdate) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, GETDATE())"
                        str_cursor.execute(str_query11, (_teamFifaId, _organisationFifaId, _facilityFifaId, _status, _internationalName, _internationalShortName, _organisationNature, _country, _region, _town, _postalCode))
                    
                    str_query02     = "SELECT * FROM [SMBIANCAV20].[comet].[competitions_teams] WHERE competitionFifaId = ? AND teamFifaId = ?"
                    str_cursor.execute(str_query02, (_competitionFifaId, _teamFifaId))
                    str_row02       = str_cursor.fetchone()

                    if str_row02:
                        str_query21 = "UPDATE [SMBIANCAV20].[comet].[competitions_teams] SET lastUpdate = GETDATE() WHERE competitionFifaId = ? AND teamFifaId = ?"
                        str_cursor.execute(str_query21, (_competitionFifaId, _teamFifaId))
                    else:
                        str_query21 = "INSERT INTO [SMBIANCAV20].[comet].[competitions_teams] (competitionFifaId, teamFifaId, lastUpdate) VALUES (?, ?, GETDATE())"
                        str_cursor.execute(str_query21, (_competitionFifaId, _teamFifaId))

                    str_connection.commit()

            except requests.ConnectionError as err:
                print('getTeams(): Error => ', err)

    except pyodbc.Error as err:
        print('getTeams(): Error MSSQL =>', err)

    finally:
        str_cursor.close()
        str_connection.close()

def getPlayers():
    try:
        str_connection  = pyodbc.connect(base_con)
        str_cursor      = str_connection.cursor()

        str_query00     = "SELECT competitionFifaId, teamFifaId FROM [SMBIANCAV20].[comet].[competitions_teams]"
        str_cursor.execute(str_query00)
        str_row00       = str_cursor.fetchone()

        if str_row00:
#        str_row00       = str_cursor.fetchall()
#        for row00 in str_row00:
            try:
#                JSONurl     = base_url + 'competition/' + str(row00[0]) + '/' + str(row00[1]) + '/players' 
                JSONurl     = base_url + 'competition/28641757/54741/players' 
                JSONResponse= requests.get(JSONurl, auth=(api_user, api_pass), headers=headers).json()
                
                for JSONData in JSONResponse['players']:
                    _personFifaId               = JSONData['person']['personFifaId']

                    if JSONData['person']['internationalFirstName']:
                        _internationalFirstName     = JSONData['person']['internationalFirstName'].upper().strip()
                    else:
                        _internationalFirstName     = JSONData['person']['internationalFirstName']

                    _internationalLastName      = JSONData['person']['internationalLastName']
                    _firstName                  = JSONData['person']['localPersonNames']['firstName']
                    _lastName                   = JSONData['person']['localPersonNames']['lastName']
                    _popularName                = JSONData['person']['localPersonNames']['popularName']
                    _birthName                  = JSONData['person']['localPersonNames']['birthName']
                    _language                   = JSONData['person']['localPersonNames']['language']
                    _title                      = JSONData['person']['localPersonNames']['title']
                    _countryOfBirth             = JSONData['person']['countryOfBirth']
                    _countryOfBirthFIFA         = JSONData['person']['countryOfBirthFIFA']
                    _regionOfBirth              = JSONData['person']['regionOfBirth']
                    _placeOfBirth               = JSONData['person']['placeOfBirth']
                    _dateOfBirth                = JSONData['person']['dateOfBirth']
                    _gender                     = JSONData['person']['gender']
                    _homegrown                  = JSONData['person']['homegrown']
                    _national_team              = JSONData['person']['national_team']
                    _nationality                = JSONData['person']['nationality']
                    _nationalityFIFA            = JSONData['person']['nationalityFIFA']
                    _place                      = JSONData['person']['place']
                    _playerPosition             = JSONData['person']['playerPosition']
                    _rowNumber                  = JSONData['person']['rowNumber']
                    _shirtNumber                = JSONData['shirtNumber']

            except requests.ConnectionError as err:
                print('getPlayers(): Error => ', err)

    except pyodbc.Error as err:
        print('getPlayers(): Error MSSQL =>', err)

    finally:
        str_cursor.close()
        str_connection.close()

def getPersons():
    print('')

if __name__ == "__main__":
#    getCompetitions()
#    getTeams()
    getPlayers()