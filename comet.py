#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import requests
import json
import pyodbc
import datetime

from bs4 import BeautifulSoup
from os import getenv

#DEFAULT
#base_con    = 'Driver={SQL Server};Server=CEROUNO-PC-01\MSSQLEXPRESS2016;Database=COMET;Trusted_Connection=yes;'
#base_con    = 'Driver={SQL Server};Server=PC-CZELAYA\SQLEXPRESS2014;Database=COMET;Trusted_Connection=yes;'
base_con    = 'Driver={ODBC Driver 17 for SQL Server};Server=10.10.10.17;Database=CSF_LESIONES;UID=user_lesiones;PWD=C0nm3b0l..!LESIONES'
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

def getDateTime():
    str_datetime    = datetime.datetime.now()
    str_fecha       = str(str_datetime.year) + '-' + str(str_datetime.month).zfill(2) + '-' + str(str_datetime.day).zfill(2)
    str_hora        = str(str_datetime.hour).zfill(2) + ':' + str(str_datetime.minute).zfill(2) + ':' + str(str_datetime.second).zfill(2)
    str_fecha_hora  = str_fecha + ' ' + str_hora

    return str_fecha_hora
        
def getOrganisations(p_organisationFifaId, p_status, p_organisationName, p_organisationNature, p_organisationShortName):
    try:
        print(getDateTime(), 'getOrganisations(): INGRESO')

        str_connection  = pyodbc.connect(base_con)
        str_cursor      = str_connection.cursor()

        str_query00     = "SELECT status FROM [comet].[organisations] WHERE organisationFifaId = ?"
        str_cursor.execute(str_query00, (p_organisationFifaId))
        str_row00       = str_cursor.fetchone()

        if str_row00:
            if str_row00[0] == 'UPDATE':
                str_query   = "UPDATE [comet].[organisations] SET status = 'ACTIVE', organisationName = ?, organisationNature = ?, organisationShortName = ?, lastUpdate = GETDATE() WHERE organisationFifaId = ?"
                str_cursor.execute(str_query, (p_organisationName, p_organisationNature, p_organisationShortName, p_organisationFifaId))
                str_connection.commit()
                print(getDateTime(), 'getOrganisations(): UPDATE organisations organisationFifaId:', p_organisationFifaId)
        else:
            str_query   = "INSERT INTO [comet].[organisations] (organisationFifaId, status, organisationName, organisationNature, organisationShortName, lastUpdate) VALUES (?, ?, ?, ?, ?, GETDATE())"
            str_cursor.execute(str_query, (p_organisationFifaId, p_status, p_organisationName, p_organisationNature, p_organisationShortName))
            str_connection.commit()
            print(getDateTime(), 'getOrganisations(): INSERT organisations organisationFifaId:', p_organisationFifaId)

    except pyodbc.Error as err:
        print(getDateTime(), 'getOrganisations(p_organisationFifaId: ' +p_organisationFifaId + '): Error MSSQL => ', err)
        setProceso('getOrganisations(p_organisationFifaId: ' + p_organisationFifaId + ') pyodbc => ', err)

    finally:
        str_cursor.close()
        str_connection.close()

def getCompetitions():
    try:
        print(getDateTime(), 'getCompetitions(): INGRESO')

        str_connection  = pyodbc.connect(base_con)
        str_cursor      = str_connection.cursor()

        str_query00     = "SELECT organisationFifaId, season, username, password FROM [comet].[logins] WHERE status = 'ACTIVE'"
        str_cursor.execute(str_query00)
        str_row00       = str_cursor.fetchone()
        
        if str_row00:
            try:
                print(getDateTime(), 'getCompetitions(): EXISTE logins')

                api_fifa    = str_row00[0]
                api_anho    = str_row00[1]
                api_user    = str_row00[2]
                api_pass    = str_row00[3]

                JSONurl     = base_url + 'competitions?organisationFifaIds='+str(api_fifa)+'&season='+str(api_anho)
                JSONResponse= requests.get(JSONurl, auth=(api_user, api_pass), headers=headers).json()
                
                for JSONData in JSONResponse:
                    _competitionFifaId          = JSONData['competitionFifaId']

                    if JSONData['ageCategory']:
                        _ageCategory                = JSONData['ageCategory'].upper().strip()
                    else:
                        _ageCategory                = JSONData['ageCategory']

                    if JSONData['ageCategoryName']:
                        _ageCategoryName            = JSONData['ageCategoryName'].upper().strip()
                    else:
                        _ageCategoryName            = JSONData['ageCategoryName'].upper().strip()
                    
                    if JSONData['dateFrom']:
                        _dateFrom                   = JSONData['dateFrom']
                    else:
                        _dateFrom                   = JSONData['dateFrom']

                    if JSONData['dateTo']:
                        _dateTo                     = JSONData['dateTo']
                    else:
                        _dateTo                     = JSONData['dateTo']

                    if JSONData['discipline']:
                        _discipline                 = JSONData['discipline'].upper().strip()
                    else:
                        _discipline                 = JSONData['discipline']

                    if JSONData['gender']:
                        _gender                     = JSONData['gender'].upper().strip()
                    else:
                        _gender                     = JSONData['gender']

                    if JSONData['internationalName']:
                        _internationalName          = JSONData['internationalName'].upper().strip()
                    else:
                        _internationalName          = JSONData['internationalName']

                    if JSONData['internationalShortName']:
                        _internationalShortName     = JSONData['internationalShortName'].upper().strip()
                    else:
                        _internationalShortName     = JSONData['internationalShortName']

                    if JSONData['imageId']:
                        _imageId                    = JSONData['imageId']
                    else:
                        _imageId                    = JSONData['imageId']
                    
                    if JSONData['multiplier']:
                        _multiplier                 = JSONData['multiplier']
                    else:
                        _multiplier                 = JSONData['multiplier']

                    if JSONData['nature']:
                        _nature                     = JSONData['nature'].upper().strip()
                    else:
                        _nature                     = JSONData['nature']

                    if JSONData['numberOfParticipants']:
                        _numberOfParticipants       = JSONData['numberOfParticipants']
                    else:
                        _numberOfParticipants       = JSONData['numberOfParticipants']

                    if JSONData['orderNumber']:
                        _orderNumber                = JSONData['orderNumber']
                    else:
                        _orderNumber                = JSONData['orderNumber']

                    if JSONData['organisationFifaId']:
                        _organisationFifaId         = JSONData['organisationFifaId']
                    else:
                        _organisationFifaId         = 1

                    if JSONData['season']:
                        _season                     = JSONData['season']
                    else:
                        _season                     = JSONData['season']

                    if JSONData['status']:
                        _status                     = JSONData['status'].upper().strip()
                    else:
                        _status                     = JSONData['status']
                    
                    if JSONData['teamCharacter']:
                        _teamCharacter              = JSONData['teamCharacter'].upper().strip()
                    else:
                        _teamCharacter              = JSONData['teamCharacter']

                    if JSONData['superiorCompetitionFifaId']:
                        _superiorCompetitionFifaId  = JSONData['superiorCompetitionFifaId']
                    else:
                        _superiorCompetitionFifaId  = JSONData['superiorCompetitionFifaId']

                    if JSONData['picture']['contentType']:
                        _pictureContentType         = JSONData['picture']['contentType']
                    else:
                        _pictureContentType         = JSONData['picture']['contentType']

                    if JSONData['picture']['pictureLink']:
                        _pictureLink                = JSONData['picture']['pictureLink']
                    else:
                        _pictureLink                = JSONData['picture']['pictureLink']

                    if JSONData['picture']['value']:
                        _pictureValue               = JSONData['picture']['value']
                    else:
                        _pictureValue               = JSONData['picture']['value']

                    if JSONData['flyingSubstitutions']:
                        _flyingSubstitutions        = JSONData['flyingSubstitutions']
                    else:
                        _flyingSubstitutions        = JSONData['flyingSubstitutions']

                    if JSONData['penaltyShootout']:
                        _penaltyShootout            = JSONData['penaltyShootout']
                    else:
                        _penaltyShootout            = JSONData['penaltyShootout']
                        
                    if JSONData['matchType']:
                        _matchType                  = JSONData['matchType'].upper().strip()
                    else:
                        _matchType                  = JSONData['matchType']
                    
                    str_select      = "SELECT * FROM [comet].[competitions] WHERE competitionFifaId = ?"
                    str_cursor.execute(str_select, (_competitionFifaId))
                    str_row         = str_cursor.fetchone()

                    if str_row:
                        str_query01     = "UPDATE [comet].[competitions] SET organisationFifaId = ?, superiorCompetitionFifaId = ?, status = ?, internationalName = ?, internationalShortName = ?, season = ?, ageCategory = ?, ageCategoryName = ?, dateFrom = ?, dateTo = ?, discipline = ?, gender = ?, imageId = ?, multiplier = ?, nature = ?, numberOfParticipants = ?, orderNumber = ?, teamCharacter = ?, flyingSubstitutions = ?, penaltyShootout = ?, matchType = ?, pictureContentType = ?, pictureLink = ?, pictureValue = ?, lastUpdate = GETDATE() WHERE competitionFifaId = ?"
                        str_cursor.execute(str_query01, (_organisationFifaId, _superiorCompetitionFifaId, _status, _internationalName, _internationalShortName, _season, _ageCategory, _ageCategoryName, _dateFrom, _dateTo, _discipline, _gender, _imageId, _multiplier, _nature, _numberOfParticipants, _orderNumber, _teamCharacter, _flyingSubstitutions, _penaltyShootout, _matchType, _pictureContentType, _pictureLink, _pictureValue, _competitionFifaId))
                        str_connection.commit()
                        print(getDateTime(), 'getCompetitions(): UPDATE competitions competitionFifaId:', _competitionFifaId)
                        getTeams(api_user, api_pass, _competitionFifaId)

                    else:
                        str_query01     = "INSERT INTO [comet].[competitions] (competitionFifaId, organisationFifaId, superiorCompetitionFifaId, status, internationalName, internationalShortName, season, ageCategory, ageCategoryName, dateFrom, dateTo, discipline, gender, imageId, multiplier, nature, numberOfParticipants, orderNumber, teamCharacter, flyingSubstitutions, penaltyShootout, matchType, pictureContentType, pictureLink, pictureValue, lastUpdate) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, GETDATE())"
                        str_cursor.execute(str_query01, (_competitionFifaId, _organisationFifaId, _superiorCompetitionFifaId, _status, _internationalName, _internationalShortName, _season, _ageCategory, _ageCategoryName, _dateFrom, _dateTo, _discipline, _gender, _imageId, _multiplier, _nature, _numberOfParticipants, _orderNumber, _teamCharacter, _flyingSubstitutions, _penaltyShootout, _matchType, _pictureContentType, _pictureLink, _pictureValue))
                        str_connection.commit()
                        print(getDateTime(), 'getCompetitions(): INSERT competitions competitionFifaId:', _competitionFifaId)
                        getTeams(api_user, api_pass, _competitionFifaId)
                        
                    getImagenCompetitions(api_user, api_pass, _competitionFifaId)
                    getMatches(api_user, api_pass, _competitionFifaId)
                    
            except requests.ConnectionError as err:
                print(getDateTime(), 'getCompetitions(): Error => ', err)
                setProceso('getCompetitions(_competitionFifaId: ' + _competitionFifaId + ') requests => ', err)

    except pyodbc.Error as err:
        print(getDateTime(), 'getCompetitions: Error MSSQL => ', err)
        setProceso('getCompetitions(_competitionFifaId: ' + _competitionFifaId + ') pyodbc => ', err)

    finally:
        str_cursor.close()
        str_connection.close()

def getImagenCompetitions(p_user, p_pass, p_competitionFifaId):
    try:
        print(getDateTime(), 'getImagenCompetitions(): INGRESO')

        str_connection  = pyodbc.connect(base_con)
        str_cursor      = str_connection.cursor()

        str_query00     = "SELECT * FROM [comet].[competitions] WHERE competitionFifaId = ?"
        str_cursor.execute(str_query00, (p_competitionFifaId))
        str_row00       = str_cursor.fetchone()
        
        if str_row00:
            try:
                print(getDateTime(), 'getImagenCompetitions(): EXISTE competitionFifaId')

                JSONurl     = base_url + 'images/competition/'+str(p_competitionFifaId)
                JSONResponse= requests.get(JSONurl, auth=(p_user, p_pass), headers=headers).json()
                
                for JSONData in JSONResponse:
                    if JSONData['contentType']:
                        _pictureContentType         = JSONData['contentType']
                    else:
                        _pictureContentType         = JSONData['contentType']

                    if JSONData['pictureLink']:
                        _pictureLink                = JSONData['pictureLink']
                    else:
                        _pictureLink                = JSONData['pictureLink']

                    if JSONData['value']:
                        _pictureValue               = JSONData['value']
                    else:
                        _pictureValue               = JSONData['value']
                    
                    str_select      = "SELECT * FROM [comet].[competitions] WHERE competitionFifaId = ? AND pictureValue IS NULL"
                    str_cursor.execute(str_select, (_competitionFifaId))
                    str_row         = str_cursor.fetchone()

                    if str_row:
                        str_query01     = "UPDATE [comet].[competitions] SET pictureContentType = ?, pictureLink = ?, pictureValue = ?, lastUpdate = GETDATE() WHERE competitionFifaId = ?"
                        str_cursor.execute(str_query01, (_pictureContentType, _pictureLink, _pictureValue, p_competitionFifaId))
                        str_connection.commit()
                        print(getDateTime(), 'getImagenCompetitions(): UPDATE competitions competitionFifaId:', p_competitionFifaId)
                    
            except requests.ConnectionError as err:
                print(getDateTime(), 'getImagenCompetitions(): Error => ', err)
                setProceso('getImagenCompetitions(p_competitionFifaId: ' + p_competitionFifaId + ') requests => ', err)

    except pyodbc.Error as err:
        print(getDateTime(), 'getImagenCompetitions: Error MSSQL => ', err)
        setProceso('getImagenCompetitions(p_competitionFifaId: ' + p_competitionFifaId + ') pyodbc => ', err)

    finally:
        str_cursor.close()
        str_connection.close()

def getTeams(p_user, p_pass, p_competitionFifaId):
    try:
        print(getDateTime(), 'getTeams(): INGRESO')
        
        str_connection  = pyodbc.connect(base_con)
        str_cursor      = str_connection.cursor()

        str_query00     = "SELECT * FROM [comet].[competitions] WHERE competitionFifaId = ?"
        str_cursor.execute(str_query00, (p_competitionFifaId))
        str_row00       = str_cursor.fetchone()

        if str_row00:
            print(getDateTime(), 'getTeams(): EXISTE competitions competitionFifaId:', p_competitionFifaId)

            try:
                JSONurl     = base_url + 'competition/' + p_competitionFifaId + '/teams'
                JSONResponse= requests.get(JSONurl, auth=(p_user, p_pass), headers=headers).json()
                
                for JSONData in JSONResponse:
                    _teamFifaId                 = JSONData['teamFifaId']
                    _competitionFifaId          = JSONData['competitionFifaId']
                    
                    if JSONData['organisationFifaId']:
                        _organisationFifaId         = JSONData['organisationFifaId']
                        getOrganisations(JSONData['organisationFifaId'], 'ACTIVE', JSONData['organisationName'], JSONData['organisationShortName'], JSONData['organisationShortName'])
                    else:
                        _organisationFifaId         = 1

                    if JSONData['facilityFifaId']:
                        _facilityFifaId             = JSONData['facilityFifaId']
                        getFacilities(p_user, p_pass, _facilityFifaId)
                    else:
                        _facilityFifaId             = JSONData['facilityFifaId']

                    if JSONData['status']:
                        _status                     = JSONData['status'].upper().strip()
                    else:
                        _status                     = JSONData['status']

                    if JSONData['internationalName']:
                        _internationalName          = JSONData['internationalName'].upper().strip()
                    else:
                        _internationalName          = JSONData['internationalName']

                    if JSONData['internationalShortName']:
                        _internationalShortName     = JSONData['internationalShortName'].upper().strip()
                    else:
                        _internationalShortName     = JSONData['internationalShortName']

                    if JSONData['organisationNature']:
                        _organisationNature         = JSONData['organisationNature'].upper().strip()
                    else:
                        _organisationNature         = JSONData['organisationNature']

                    if JSONData['country']:
                        _country                    = JSONData['country'].upper().strip()
                    else:
                        _country                    = JSONData['country']

                    if JSONData['region']:                        
                        _region                     = JSONData['region'].upper().strip()
                    else:
                        _region                     = JSONData['region']

                    if JSONData['town']:
                        _town                       = JSONData['town'].upper().strip()
                    else:
                        _town                       = JSONData['town']
                    
                    if JSONData['postalCode']:
                        _postalCode                 = JSONData['postalCode'].upper().strip()
                    else:
                        _postalCode                 = JSONData['postalCode']

                    str_query01     = "SELECT * FROM [comet].[teams] WHERE teamFifaId = ?"
                    str_cursor.execute(str_query01, (_teamFifaId))
                    str_row01       = str_cursor.fetchone()

                    if str_row01 == None:
                        str_query02 = "INSERT INTO [comet].[teams] (teamFifaId, organisationFifaId, facilityFifaId, status, internationalName, internationalShortName, organisationNature, country, region, town, postalCode, lastUpdate) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, GETDATE())"
                        str_cursor.execute(str_query02, (_teamFifaId, _organisationFifaId, _facilityFifaId, _status, _internationalName, _internationalShortName, _organisationNature, _country, _region, _town, _postalCode))
                        str_connection.commit()
                        print(getDateTime(), 'getTeams(): INSERT teams teamFifaId:', _teamFifaId)
                    
                    str_query03     = "SELECT * FROM [comet].[competitions_teams] WHERE competitionFifaId = ? AND teamFifaId = ?"
                    str_cursor.execute(str_query03, (_competitionFifaId, _teamFifaId))
                    str_row03       = str_cursor.fetchone()

                    if str_row03 == None:
                        str_query04 = "INSERT INTO [comet].[competitions_teams] (competitionFifaId, teamFifaId, lastUpdate) VALUES (?, ?, GETDATE())"
                        str_cursor.execute(str_query04, (_competitionFifaId, _teamFifaId))
                        str_connection.commit()
                        print(getDateTime(), 'getTeams(): INSERT competitions_teams competitions:',  _competitionFifaId, ', teams:', _teamFifaId)

                    getPlayers(p_user, p_pass, _competitionFifaId, _teamFifaId)

            except requests.ConnectionError as err:
                print(getDateTime(), 'getTeams(): Error => ', err)
                setProceso('getTeams(p_competitionFifaId: ' + p_competitionFifaId + ') requests => ', err)

    except pyodbc.Error as err:
        print(getDateTime(), 'getTeams(): Error MSSQL =>', err)
        setProceso('getTeams(p_competitionFifaId: ' + p_competitionFifaId + ') pyodbc => ', err)

    finally:
        str_cursor.close()
        str_connection.close()

def getPlayers(p_user, p_pass, p_competitionFifaId, p_teamFifaId):
    try:
        print(getDateTime(), 'getPlayers(): INGRESO')

        str_connection  = pyodbc.connect(base_con)
        str_cursor      = str_connection.cursor()

        str_query00     = "SELECT competitionFifaId, teamFifaId FROM [comet].[competitions_teams] WHERE competitionFifaId = ? AND teamFifaId = ?"
        str_cursor.execute(str_query00, (p_competitionFifaId, p_teamFifaId))
        str_row00       = str_cursor.fetchone()

        if str_row00:
            print(getDateTime(), 'getPlayers(): EXISTE competitions_teams competitionFifaId:', p_competitionFifaId, ', teamFifaId:', p_teamFifaId)
            
            try:
                JSONUrl             = base_url + 'competition/' + p_competitionFifaId + '/' + p_teamFifaId + '/players' 
                JSONResponse        = requests.get(JSONUrl, auth=(p_user, p_pass), headers=headers).json()

                for JSONData in JSONResponse['players']:
                    if JSONData['person']['personFifaId']:
                        _personFifaId               = JSONData['person']['personFifaId']
                        getPersons(p_user, p_pass, _personFifaId)
                    else:
                        _personFifaId               = 1

                    if JSONData['shirtNumber']:
                        _shirtNumber                = JSONData['shirtNumber']
                    else:
                        _shirtNumber                = JSONData['shirtNumber']

                    str_query01     = "SELECT * FROM [comet].[competitions_teams_players] WHERE competitionFifaId = ? AND teamFifaId = ? AND playerFifaId = ?"
                    str_cursor.execute(str_query01, (p_competitionFifaId, p_teamFifaId, _personFifaId))
                    str_row01       = str_cursor.fetchone()

                    if str_row01 == None:
                        str_query_02    = "INSERT INTO [comet].[competitions_teams_players] (competitionFifaId, teamFifaId, playerFifaId, shirtNumber, lastUpdate) VALUES (?, ?, ?, ?, GETDATE())"
                        str_cursor.execute(str_query_02, (p_competitionFifaId, p_teamFifaId, _personFifaId, _shirtNumber))
                        str_connection.commit()
                        print(getDateTime(), 'getPlayers(): INSERT competitions_teams_players competitionFifaId:', p_competitionFifaId, ', teamFifaId:', p_teamFifaId, ', playerFifaId:', _personFifaId)

            except requests.ConnectionError as err:
                print(getDateTime(), 'getPlayers(p_competitionFifaId: ' + p_competitionFifaId + ', p_teamFifaId: ' + p_teamFifaId + '): Error => ', err)
                setProceso('getPlayers(p_competitionFifaId: ' + p_competitionFifaId + ', p_teamFifaId: ' + p_teamFifaId + ') requests => ', err)

    except pyodbc.Error as err:
        print(getDateTime(), 'getPlayers(p_competitionFifaId: ' + p_competitionFifaId + ', p_teamFifaId: ' + p_teamFifaId + '): Error MSSQL =>', err)
        setProceso('getPlayers(p_competitionFifaId: ' + p_competitionFifaId + ', p_teamFifaId: ' + p_teamFifaId + ') pyodbc => ', err)

    finally:
        str_cursor.close()
        str_connection.close()

def getMatches(p_user, p_pass, p_competitionFifaId):
    try:
        print(getDateTime(), 'getMatches(): INGRESO')

        str_connection  = pyodbc.connect(base_con)
        str_cursor      = str_connection.cursor()

        str_query00     = "SELECT * FROM [comet].[competitions] WHERE competitionFifaId = ?"
        str_cursor.execute(str_query00, (p_competitionFifaId))
        str_row00       = str_cursor.fetchone()

        if str_row00:
            print(getDateTime(), 'getMatches(): EXISTE competitions competitionFifaId:', p_competitionFifaId)
            
            try:
                JSONurl     = base_url + 'competition/' + p_competitionFifaId + '/matches'
                JSONResponse= requests.get(JSONurl, auth=(p_user, p_pass), headers=headers).json()
                
                for JSONData in JSONResponse:
                    _matchFifaId                = JSONData['matchFifaId']
                    _competitionFifaId          = JSONData['competitionFifaId']

                    if JSONData['facilityFifaId']:
                        _facilityFifaId             = JSONData['facilityFifaId']
                        getFacilities(p_user, p_pass, _facilityFifaId)
                    else:
                        _facilityFifaId             = JSONData['facilityFifaId']

                    if JSONData['attendance']:
                        _attendance                 = JSONData['attendance']
                    else:
                        _attendance                 = JSONData['attendance']

                    if JSONData['dateTimeLocal']:
                        _dateTimeLocal              = JSONData['dateTimeLocal']
                        _dateTimeLocal              = _dateTimeLocal.replace(' ', 'T')
                    else:
                        _dateTimeLocal              = JSONData['dateTimeLocal']

                    if JSONData['matchDay']:
                        _matchDay                   = JSONData['matchDay']
                    else:
                        _matchDay                   = JSONData['matchDay']
                    
                    if JSONData['matchDayDesc']:
                        _matchDayDesc               = JSONData['matchDayDesc'].upper().strip()
                    else:
                        _matchDayDesc               = JSONData['matchDayDesc']

                    if JSONData['matchOrderNumber']:
                        _matchOrderNumber           = JSONData['matchOrderNumber']
                    else:
                        _matchOrderNumber           = JSONData['matchOrderNumber']

                    if JSONData['status']:
                        _status                     = JSONData['status'].upper().strip()
                    else:
                        _status                     = JSONData['status']

                    if JSONData['resultSupplement']:
                        _resultSupplement           = JSONData['resultSupplement']
                    else:
                        _resultSupplement           = JSONData['resultSupplement']

                    if JSONData['resultSupplementHome']:
                        _resultSupplementHome       = JSONData['resultSupplementHome']
                    else:
                        _resultSupplementHome       = JSONData['resultSupplementHome']

                    if JSONData['resultSupplementAway']:
                        _resultSupplementAway       = JSONData['resultSupplementAway']
                    else:
                        _resultSupplementAway       = JSONData['resultSupplementAway']

                    str_query01     = "SELECT * FROM [comet].[matches] WHERE matchFifaId = ?"
                    str_cursor.execute(str_query01, (_matchFifaId))
                    str_row01       = str_cursor.fetchone()

                    if str_row01:
                        str_query02 = "UPDATE [comet].[matches] SET competitionFifaId = ?, facilityFifaId = ?, status = ?, attendance = ?, dateTimeLocal = ?, matchDay = ?, matchDayDesc = ?, matchOrderNumber = ?, resultSupplement = ?, resultSupplementHome = ?, resultSupplementAway = ?, lastUpdate = GETDATE() WHERE matchFifaId = ?"
                        str_cursor.execute(str_query02, (_competitionFifaId, _facilityFifaId, _status, _attendance, _dateTimeLocal, _matchDay, _matchDayDesc, _matchOrderNumber, _resultSupplement, _resultSupplementHome, _resultSupplementAway, _matchFifaId))
                        str_connection.commit()
                        print(getDateTime(), 'getMatches(): UPDATE matches matchFifaId:', _matchFifaId)

                    else:
                        str_query02 = "INSERT INTO [comet].[matches] (matchFifaId, competitionFifaId, facilityFifaId, status, attendance, dateTimeLocal, matchDay, matchDayDesc, matchOrderNumber, resultSupplement, resultSupplementHome, resultSupplementAway, lastUpdate) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, GETDATE())"
                        str_cursor.execute(str_query02, (_matchFifaId, _competitionFifaId, _facilityFifaId, _status, _attendance, _dateTimeLocal, _matchDay, _matchDayDesc, _matchOrderNumber, _resultSupplement, _resultSupplementHome, _resultSupplementAway))
                        str_connection.commit()
                        print(getDateTime(), 'getMatches(): INSERT matches matchFifaId:', _matchFifaId)

                    for JSONDataTeam in JSONData['matchTeams']:
                        _matchFifaId    = JSONDataTeam['matchFifaId']
                        _teamFifaId     = JSONDataTeam['teamFifaId']
                        
                        if JSONDataTeam['teamNature']:
                            _teamNature     = JSONDataTeam['teamNature'].upper().strip()
                        else:
                            _teamNature     = JSONDataTeam['teamNature']

                        str_query03     = "SELECT * FROM [comet].[matches_teams] WHERE matchFifaId = ? AND teamFifaId = ?"
                        str_cursor.execute(str_query03, (_matchFifaId, _teamFifaId))
                        str_row03       = str_cursor.fetchone()

                        if str_row03 == None:
                            str_query_04    = "INSERT INTO [comet].[matches_teams] (matchFifaId, teamFifaId, teamNature, lastUpdate) VALUES (?, ?, ?, GETDATE())"
                            str_cursor.execute(str_query_04, (_matchFifaId, _teamFifaId, _teamNature))
                            str_connection.commit()
                            print(getDateTime(), 'getMatches(): INSERT matches_teams matchFifaId:', _matchFifaId, 'teamFifaId:', _teamFifaId, 'teamNature:', _teamNature)
                    
                    for JSONDataPhases in JSONData['matchPhases']:
                        _matchFifaId    = JSONDataPhases['matchFifaId']

                        if JSONDataPhases['phase']:
                            _phase          = JSONDataPhases['phase'].upper().strip()
                        else:
                            _phase          = JSONDataPhases['phase']

                        if JSONDataPhases['homeScore']:
                            _homeScore      = JSONDataPhases['homeScore']
                        else:
                            _homeScore      = JSONDataPhases['homeScore']

                        if JSONDataPhases['awayScore']:
                            _awayScore      = JSONDataPhases['awayScore']
                        else:
                            _awayScore      = JSONDataPhases['awayScore']

                        if JSONDataPhases['startDateTime']:
                            _startDateTime  = JSONDataPhases['startDateTime']
                            _startDateTime  = _startDateTime.replace(' ', 'T')
                        else:
                            _startDateTime  = JSONDataPhases['startDateTime']

                        if JSONDataPhases['endDateTime']:
                            _endDateTime    = JSONDataPhases['endDateTime']
                            _endDateTime    = _endDateTime.replace(' ', 'T')
                        else:
                            _endDateTime    = JSONDataPhases['endDateTime']

                        if JSONDataPhases['regularTime']:
                            _regularTime    = JSONDataPhases['regularTime']
                        else:
                            _regularTime    = JSONDataPhases['regularTime']
                        
                        if JSONDataPhases['stoppageTime']:
                            _stoppageTime   = JSONDataPhases['stoppageTime']
                        else:
                            _stoppageTime   = JSONDataPhases['stoppageTime']

                        if JSONDataPhases['phaseLength']:
                            _phaseLength    = JSONDataPhases['phaseLength']
                        else:
                            _phaseLength    = JSONDataPhases['phaseLength']

                        str_query05     = "SELECT * FROM [comet].[matches_phases] WHERE matchFifaId = ? AND phase = ?"
                        str_cursor.execute(str_query05, (_matchFifaId, _phase))
                        str_row05       = str_cursor.fetchone()

                        if str_row05:
                            str_query_06    = "UPDATE [comet].[matches_phases] SET homeScore = ?, awayScore = ?, startDateTime = ?, endDateTime = ?, regularTime = ?, stoppageTime = ?, phaseLength = ?, lastUpdate = GETDATE() WHERE matchFifaId = ? AND phase = ?"
                            str_cursor.execute(str_query_06, (_homeScore, _awayScore, _startDateTime, _endDateTime, _regularTime, _stoppageTime, _phaseLength, _matchFifaId, _phase))
                            str_connection.commit()
                            print(getDateTime(), 'getMatches(): UPDATE matches_phases matchFifaId:', _matchFifaId, 'phase:', _phase)

                        else:
                            str_query_06    = "INSERT INTO [comet].[matches_phases] (matchFifaId, phase, homeScore, awayScore, startDateTime, endDateTime, regularTime, stoppageTime, phaseLength, lastUpdate) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, GETDATE())"
                            str_cursor.execute(str_query_06, (_matchFifaId, _phase, _homeScore, _awayScore, _startDateTime, _endDateTime, _regularTime, _stoppageTime, _phaseLength))
                            str_connection.commit()
                            print(getDateTime(), 'getMatches(): INSERT matches_phases matchFifaId:', _matchFifaId, 'phase:', _phase)

                    for JSONDataOfficials in JSONData['matchOfficials']:
                        _matchFifaId        = JSONDataOfficials['matchFifaId']

                        if JSONDataOfficials['personFifaId']:
                            _personFifaId       = JSONDataOfficials['personFifaId']
                            getPersons(p_user, p_pass, _personFifaId)
                        else:
                            _personFifaId       = 1

                        if JSONDataOfficials['personName']:
                            _personName         = JSONDataOfficials['personName'].upper().strip()
                        else:
                            _personName         = JSONDataOfficials['personName']

                        if JSONDataOfficials['role']:
                            _role               = JSONDataOfficials['role'].upper().strip()
                        else:
                            _role               = JSONDataOfficials['role']

                        if JSONDataOfficials['roleDescription']:
                            _roleDescription    = JSONDataOfficials['roleDescription'].upper().strip()
                        else:
                            _roleDescription    = JSONDataOfficials['roleDescription']

                        if JSONDataOfficials['cometRoleName']:
                            _cometRoleName      = JSONDataOfficials['cometRoleName'].upper().strip()
                        else:
                            _cometRoleName      = JSONDataOfficials['cometRoleName']

                        if JSONDataOfficials['cometRoleNameKey']:
                            _cometRoleNameKey   = JSONDataOfficials['cometRoleNameKey'].upper().strip()
                        else:
                            _cometRoleNameKey   = JSONDataOfficials['cometRoleNameKey']

                        str_query07     = "SELECT * FROM [comet].[matches_officials] WHERE matchFifaId = ? AND personFifaId = ?"
                        str_cursor.execute(str_query07, (_matchFifaId, _personFifaId))
                        str_row07       = str_cursor.fetchone()

                        if str_row07 == None:
                            str_query_08    = "INSERT INTO [comet].[matches_officials] (matchFifaId, personFifaId, personName, role, roleDescription, cometRoleName, cometRoleNameKey, lastUpdate) VALUES (?, ?, ?, ?, ?, ?, ?, GETDATE())"
                            str_cursor.execute(str_query_08, (_matchFifaId, _personFifaId, _personName, _role, _roleDescription, _cometRoleName, _cometRoleNameKey))
                            str_connection.commit()
                            print(getDateTime(), 'getMatches(): INSERT matches_officials matchFifaId:', _matchFifaId, 'personFifaId:', _personFifaId)

            except requests.ConnectionError as err:
                print(getDateTime(), 'getMatches(): Error => ', err)
                setProceso('getMatches(p_competitionFifaId: ' + p_competitionFifaId + ', _matchFifaId: ' + _matchFifaId + ') requests => ', err)

    except pyodbc.Error as err:
        print(getDateTime(), 'getMatches(): Error MSSQL =>', err)
        setProceso('getMatches(p_competitionFifaId: ' + p_competitionFifaId + ', _matchFifaId: ' + _matchFifaId + ') pyodbc => ', err)

    finally:
        str_cursor.close()
        str_connection.close()

def getPersons(p_user, p_pass, p_personFifaId):
    try:
        print(getDateTime(), 'getPersons(): INGRESO')

        str_connection  = pyodbc.connect(base_con)
        str_cursor      = str_connection.cursor()

        str_query00     = "SELECT * FROM [comet].[persons] WHERE personFifaId = ?"
        str_cursor.execute(str_query00, (p_personFifaId))
        str_row00       = str_cursor.fetchone()

        if str_row00 == None:
            print(getDateTime(), 'getPersons(): NO EXISTE persons personFifaId:', p_personFifaId)

            try:
                JSONurl     = base_url + 'player/' + str(p_personFifaId)
                JSONResponse= requests.get(JSONurl, auth=(p_user, p_pass), headers=headers).json()
                JSONData    = JSONResponse['person']

                if JSONData:
                    _personFifaId               = JSONData['personFifaId']

                    if JSONData['internationalFirstName']:
                        _internationalFirstName     = JSONData['internationalFirstName'].upper().strip()
                    else:
                        _internationalFirstName     = JSONData['internationalFirstName']

                    if JSONData['internationalLastName']:
                        _internationalLastName      = JSONData['internationalLastName'].upper().strip()
                    else:
                        _internationalLastName      = JSONData['internationalLastName']

                    if JSONData['localPersonNames']:
                        if JSONData['localPersonNames'][0]['firstName']:
                            _firstName      = JSONData['localPersonNames'][0]['firstName'].upper().strip()
                        else:
                            _firstName      = JSONData['localPersonNames'][0]['firstName']
                        
                        if JSONData['localPersonNames'][0]['lastName']:
                            _lastName       = JSONData['localPersonNames'][0]['lastName'].upper().strip()
                        else:
                            _lastName       = JSONData['localPersonNames'][0]['lastName']

                        if JSONData['localPersonNames'][0]['popularName']:
                            _popularName    = JSONData['localPersonNames'][0]['popularName'].upper().strip()
                        else:
                            _popularName    = JSONData['localPersonNames'][0]['popularName']

                        if JSONData['localPersonNames'][0]['birthName']:
                            _birthName      = JSONData['localPersonNames'][0]['birthName'].upper().strip()
                        else:
                            _birthName      = JSONData['localPersonNames'][0]['birthName']

                        if JSONData['localPersonNames'][0]['language']:
                            _language       = JSONData['localPersonNames'][0]['language'].upper().strip()
                        else:
                            _language       = JSONData['localPersonNames'][0]['language']
                        
                        if JSONData['localPersonNames'][0]['title']:
                            _title          = JSONData['localPersonNames'][0]['title'].upper().strip()
                        else:
                            _title          = JSONData['localPersonNames'][0]['title']
                    else:
                        _firstName          = None
                        _lastName           = None
                        _popularName        = None
                        _birthName          = None
                        _language           = None
                        _title              = None
                    
                    if JSONData['countryOfBirth']:
                        _countryOfBirth             = JSONData['countryOfBirth'].upper().strip()
                    else:
                        _countryOfBirth             = JSONData['countryOfBirth']

                    if JSONData['countryOfBirthFIFA']:
                        _countryOfBirthFIFA         = JSONData['countryOfBirthFIFA'].upper().strip()
                    else:
                        _countryOfBirthFIFA         = JSONData['countryOfBirthFIFA']

                    if JSONData['regionOfBirth']:
                        _regionOfBirth              = JSONData['regionOfBirth'].upper().strip()
                    else:
                        _regionOfBirth              = JSONData['regionOfBirth']

                    if JSONData['placeOfBirth']:
                        _placeOfBirth               = JSONData['placeOfBirth'].upper().strip()
                    else:
                        _placeOfBirth               = JSONData['placeOfBirth']

                    if JSONData['dateOfBirth']:
                        _dateOfBirth                = JSONData['dateOfBirth']
                    else:
                        _dateOfBirth                = JSONData['dateOfBirth']

                    if JSONData['gender']:
                        _gender                     = JSONData['gender'].upper().strip()
                    else:
                        _gender                     = JSONData['gender']

                    if JSONData['homegrown']:
                        _homegrown                  = JSONData['homegrown']
                    else:
                        _homegrown                  = JSONData['homegrown']

                    if JSONData['national_team']:
                        _national_team              = JSONData['national_team'].upper().strip()
                    else:
                        _national_team              = JSONData['national_team']
                    
                    if JSONData['nationality']:
                        _nationality                = JSONData['nationality'].upper().strip()
                    else:
                        _nationality                = JSONData['nationality']

                    if JSONData['nationalityFIFA']:
                        _nationalityFIFA            = JSONData['nationalityFIFA'].upper().strip()
                    else:
                        _nationalityFIFA            = JSONData['nationalityFIFA']

                    if JSONData['place']:
                        _place                      = JSONData['place'].upper().strip()
                    else:
                        _place                      = JSONData['place']

                    if JSONData['playerPosition']:
                        _playerPosition             = JSONData['playerPosition'].upper().strip()
                    else:
                        _playerPosition             = JSONData['playerPosition']

                    if JSONData['rowNumber']:
                        _rowNumber                  = JSONData['rowNumber']
                    else:
                        _rowNumber                  = JSONData['rowNumber']

                    str_query01     = "SELECT * FROM [comet].[persons] WHERE personFifaId = ?"
                    str_cursor.execute(str_query01, (_personFifaId))
                    str_row01       = str_cursor.fetchone()

                    if str_row01 == None:
                        str_query_02    = "INSERT INTO [comet].[persons] (personFifaId, internationalFirstName, internationalLastName, firstName, lastName, popularName, birthName, language, title, countryOfBirth, countryOfBirthFIFA, regionOfBirth, placeOfBirth, dateOfBirth, gender, homegrown, national_team, nationality, nationalityFIFA, place, playerPosition, rowNumber, lastUpdate) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, GETDATE())"
                        str_cursor.execute(str_query_02, (_personFifaId, _internationalFirstName, _internationalLastName, _firstName, _lastName, _popularName, _birthName, _language, _title, _countryOfBirth, _countryOfBirthFIFA, _regionOfBirth, _placeOfBirth, _dateOfBirth, _gender, _homegrown, _national_team, _nationality, _nationalityFIFA, _place, _playerPosition, _rowNumber))
                        str_connection.commit()
                        print(getDateTime(), 'getPersons(): INSERT persons personFifaId:', _personFifaId)

            except requests.ConnectionError as err:
                print(getDateTime(), 'getPersons(): Error => ', err)
                setProceso('getPersons(p_personFifaId: ' + p_personFifaId + ') requests => ', err)

    except pyodbc.Error as err:
        print(getDateTime(), 'getPersons(): Error MSSQL =>', err)
        setProceso('getPersons(p_personFifaId: ' + p_personFifaId + ') pyodbc => ', err)

    finally:
        str_cursor.close()
        str_connection.close()

def getFacilities(p_user, p_pass, p_facilityFifaId):
    try:
        print(getDateTime(), 'getFacilities(): INGRESO')

        str_connection  = pyodbc.connect(base_con)
        str_cursor      = str_connection.cursor()

        str_query00     = "SELECT * FROM [comet].[facilities] WHERE facilityFifaId = ?"
        str_cursor.execute(str_query00, (p_facilityFifaId))
        str_row00       = str_cursor.fetchone()

        if str_row00 == None:
            print(getDateTime(), 'getFacilities(): NO EXISTE facilities facilityFifaId:', p_facilityFifaId)

            try:
                JSONurl     = base_url + 'facilities?facilityFifaId=' + p_facilityFifaId
                JSONResponse= requests.get(JSONurl, auth=(p_user, p_pass), headers=headers).json()
                
                for JSONData in JSONResponse:
                    _facilityFifaId             = JSONData['facilityFifaId']

                    if JSONData['fields']:
                        if JSONData['fields'][0]['orderNumber']:
                            _orderNumber        = JSONData['fields'][0]['orderNumber']
                        else:
                            _orderNumber        = JSONData['fields'][0]['orderNumber']

                        if JSONData['fields'][0]['discipline']:
                            _discipline         = JSONData['fields'][0]['discipline'].upper().strip()
                        else:
                            _discipline         = JSONData['fields'][0]['discipline']

                        if JSONData['fields'][0]['capacity']:
                            _capacity           = JSONData['fields'][0]['capacity']
                        else:
                            _capacity           = JSONData['fields'][0]['capacity']

                        if JSONData['fields'][0]['groundNature']:
                            _groundNature       = JSONData['fields'][0]['groundNature'].upper().strip()
                        else:
                            _groundNature       = JSONData['fields'][0]['groundNature']

                        if JSONData['fields'][0]['length']:
                            _length             = JSONData['fields'][0]['length']
                        else:
                            _length             = JSONData['fields'][0]['length']

                        if JSONData['fields'][0]['width']:
                            _width              = JSONData['fields'][0]['width']
                        else:
                            _width              = JSONData['fields'][0]['width']

                        if JSONData['fields'][0]['latitude']:
                            _latitude           = JSONData['fields'][0]['latitude']
                        else:
                            _latitude           = JSONData['fields'][0]['latitude']

                        if JSONData['fields'][0]['longitude']:
                            _longitude          = JSONData['fields'][0]['longitude']
                        else:
                            _longitude          = JSONData['fields'][0]['longitude']
                    else:
                        _orderNumber    = None
                        _discipline     = None
                        _capacity       = None
                        _groundNature   = None
                        _length         = None
                        _width          = None
                        _latitude       = None
                        _longitude      = None

                    if JSONData['status']:
                        _status                     = JSONData['status'].upper().strip()
                    else:
                        _status                     = JSONData['status']

                    if JSONData['internationalName']:
                        _internationalName          = JSONData['internationalName'].upper().strip()
                    else:
                        _internationalName          = JSONData['internationalName']

                    if JSONData['internationalShortName']:
                        _internationalShortName     = JSONData['internationalShortName'].upper().strip()
                    else:
                        _internationalShortName     = JSONData['internationalShortName']

                    if JSONData['organisationFifaId']:
                        _organisationFifaId         = JSONData['organisationFifaId']
                    else:
                        _organisationFifaId         = 1

                    if JSONData['parentFacilityFifaId']:
                        _parentFacilityFifaId       = JSONData['parentFacilityFifaId']
                        getFacilities(p_user, p_pass, _parentFacilityFifaId)
                    else:
                        _parentFacilityFifaId       = JSONData['parentFacilityFifaId']

                    if JSONData['town']:
                        _town                       = JSONData['town'].upper().strip()
                    else:
                        _town                       = JSONData['town']

                    if JSONData['address']:
                        _address                    = JSONData['address'].upper().strip()
                    else:
                        _address                    = JSONData['address']

                    if JSONData['webAddress']:
                        _webAddress                 = JSONData['webAddress'].upper().strip()
                    else:
                        _webAddress                 = JSONData['webAddress']

                    if JSONData['email']:
                        _email                      = JSONData['email'].upper().strip()
                    else:
                        _email                      = JSONData['email']
                    
                    if JSONData['phone']:
                        _phone                      = JSONData['phone']
                    else:
                        _phone                      = JSONData['phone']
                    
                    if JSONData['fax']:
                        _fax                        = JSONData['fax']
                    else:
                        _fax                        = JSONData['fax']

                    if JSONData['localNames']:
                        if JSONData['localNames'][0]['name']:
                            _name               = JSONData['localNames'][0]['name'].upper().strip()
                        else:
                            _name               = JSONData['localNames'][0]['name']

                        if JSONData['localNames'][0]['shortName']:
                            _shortName          = JSONData['localNames'][0]['shortName'].upper().strip()
                        else:
                            _shortName          = JSONData['localNames'][0]['shortName']

                        if JSONData['localNames'][0]['placeName']:
                            _placeName          = JSONData['localNames'][0]['placeName'].upper().strip()
                        else:
                            _placeName          = JSONData['localNames'][0]['placeName']
                        
                        if JSONData['localNames'][0]['regionName']:
                            _regionName         = JSONData['localNames'][0]['regionName'].upper().strip()
                        else:
                            _regionName         = JSONData['localNames'][0]['regionName']
                        
                        if JSONData['localNames'][0]['language']: 
                            _language           = JSONData['localNames'][0]['language'].upper().strip()
                        else:
                            _language           = JSONData['localNames'][0]['language']
                    
                    else:
                        _name           = None
                        _shortName      = None
                        _placeName      = None
                        _regionName     = None
                        _language       = None
                    
                    str_query01     = "SELECT * FROM [comet].[facilities] WHERE facilityFifaId = ?"
                    str_cursor.execute(str_query01, (_facilityFifaId))
                    str_row01       = str_cursor.fetchone()

                    if str_row01 == None:
                        str_query_02    = "INSERT INTO [comet].[facilities] (facilityFifaId, organisationFifaId, parentFacilityFifaId, status, internationalName, internationalShortName, name, shortName, town, placeName, regionName, language, address, webAddress, email, phone, fax, capacity, discipline, groundNature, latitude, longitude, length, orderNumber, width, lastUpdate) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, GETDATE())"
                        str_cursor.execute(str_query_02, (_facilityFifaId, _organisationFifaId, _parentFacilityFifaId, _status, _internationalName, _internationalShortName, _name, _shortName, _town, _placeName, _regionName, _language, _address, _webAddress, _email, _phone, _fax, _capacity, _discipline, _groundNature, _latitude, _longitude, _length, _orderNumber, _width))
                        str_connection.commit()
                        print(getDateTime(), 'getFacilities(): INSERT facilities facilityFifaId:', _facilityFifaId)

            except requests.ConnectionError as err:
                print(getDateTime(), 'getFacilities(): Error => ', err)
                setProceso('getFacilities(p_facilityFifaId: ' + p_facilityFifaId + ') requests => ', err)

    except pyodbc.Error as err:
        print(getDateTime(), 'getFacilities(): Error MSSQL =>', err)
        setProceso('getFacilities(p_facilityFifaId: ' + p_facilityFifaId + ') pyodbc => ', err)

    finally:
        str_cursor.close()
        str_connection.close()

def setProceso(p_status, p_errors):
    try:
        print(getDateTime(), 'setProceso(): INGRESO')

        str_connection  = pyodbc.connect(base_con)
        str_cursor      = str_connection.cursor()

        str_query   = "INSERT INTO [comet].[processes] (status, errors, lastUpdate) VALUES (?, ?, GETDATE())"
        str_cursor.execute(str_query, (p_status, p_errors))
        str_connection.commit()
        print(getDateTime(), 'setProceso(): INSERT processes status:' p_status)

    except pyodbc.Error as err:
        print(getDateTime(), 'setProceso(): Error MSSQL => ', err)
        setProceso('setProceso() pyodbc => ', err)

    finally:
        str_cursor.close()
        str_connection.close()

if __name__ == "__main__":
    setProceso('__name__', '-')
    getCompetitions()
    setProceso('__name__', '-')