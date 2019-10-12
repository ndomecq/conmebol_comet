#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import requests
import json
import pyodbc
import os
import base64
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

def setOrganisationsImagen():
    try:
        print(getDateTime(), 'setOrganisationsImagen(): INGRESO')

        str_connection  = pyodbc.connect(base_con)
        str_cursor      = str_connection.cursor()

        str_query00     = "SELECT organisationFifaId, pictureContentType, pictureValue FROM [comet].[organisations] WHERE pictureValue IS NOT NULL"
        str_cursor.execute(str_query00)
        str_row00       = str_cursor.fetchall()
        
        for str_row in str_row00:
            setImagen('organizacion', str_row[0], str_row[1], str_row[2])

    except pyodbc.Error as err:
        print(getDateTime(), 'setOrganisationsImagen: Error MSSQL => ', err)
        str_pro = getDateTime() + ' setOrganisationsImagen()'
        str_err = 'setOrganisationsImagen() pyodbc => ' + str(err)
        setProceso(str_pro, str_err)

    finally:
        str_cursor.close()
        str_connection.close()

def setCompetitionsImagen():
    try:
        print(getDateTime(), 'setCompetitionsImagen(): INGRESO')

        str_connection  = pyodbc.connect(base_con)
        str_cursor      = str_connection.cursor()

        str_query00     = "SELECT competitionFifaId, pictureContentType, pictureValue FROM [comet].[competitions] WHERE pictureValue IS NOT NULL"
        str_cursor.execute(str_query00)
        str_row00       = str_cursor.fetchall()
        
        for str_row in str_row00:
            setImagen('competencia', str_row[0], str_row[1], str_row[2])

    except pyodbc.Error as err:
        print(getDateTime(), 'setCompetitionsImagen: Error MSSQL => ', err)
        str_pro = getDateTime() + ' setCompetitionsImagen()'
        str_err = 'setCompetitionsImagen() pyodbc => ' + str(err)
        setProceso(str_pro, str_err)

    finally:
        str_cursor.close()
        str_connection.close()

def setPlayersImagen():
    try:
        print(getDateTime(), 'setPlayersImagen(): INGRESO')

        str_connection  = pyodbc.connect(base_con)
        str_cursor      = str_connection.cursor()

        str_query00     = "SELECT personFifaId, pictureContentType, pictureValue FROM [comet].[persons] WHERE pictureValue IS NOT NULL"
        str_cursor.execute(str_query00)
        str_row00       = str_cursor.fetchall()
        
        for str_row in str_row00:
            setImagen('jugador', str_row[0], str_row[1], str_row[2])

    except pyodbc.Error as err:
        print(getDateTime(), 'setPlayersImagen: Error MSSQL => ', err)
        str_pro = getDateTime() + ' setPlayersImagen()'
        str_err = 'setPlayersImagen() pyodbc => ' + str(err)
        setProceso(str_pro, str_err)

    finally:
        str_cursor.close()
        str_connection.close()

def setImagen(var01, var02, var03, var04):
    str_exth    = '.png' 
    str_path    = '/var/www/portalmedico.conmebol.com/public_html/imagen/' + var01 + '/img_' + str(var02)

    if var03 == 'image/png':
        str_exth = '.png'

    elif var03 == 'image/jpeg':
        str_exth = '.jpeg'

    elif var03 == 'image/jpg':
        str_exth = '.jpg'

    else:
        str_exth = '.png'

    str_img     = str_path + str_exth
    fil_img     = base64.b64decode(var04)

    if os.path.isfile(str_img) == False:
        with open(str_img, 'wb') as fh:
            fh.write(fil_img)
        
def setProceso(p_status, p_errors):
    try:
        print(getDateTime(), 'setProceso(): INGRESO')

        str_connection  = pyodbc.connect(base_con)
        str_cursor      = str_connection.cursor()

        str_query   = "INSERT INTO [comet].[processes] (status, errors, lastUpdate) VALUES (?, ?, GETDATE())"
        str_cursor.execute(str_query, (p_status, p_errors))
        str_connection.commit()
        print(getDateTime(), 'setProceso(): INSERT processes status:', p_status)

    except pyodbc.Error as err:
        print(getDateTime(), 'setProceso(): Error MSSQL => ', err)
        setProceso('setProceso() pyodbc => ', str(err))

    finally:
        str_cursor.close()
        str_connection.close()

if __name__ == "__main__":
    setProceso('INICIO GENERAR IMAGENES', '-')
    setOrganisationsImagen()
    setCompetitionsImagen()
    setPlayersImagen()
    setProceso('FIN GENERAR IMAGENES', '-')