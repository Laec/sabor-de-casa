import pandas as pd

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from pywhatkit import sendwhatmsg_instantly
from time import sleep

# Use el archivo de credenciales para autenticarse con Google
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

id_fromulario = ['12kz3XEp8lbgCMobJD_h2JY2WEsXneY0NCjuv_9I6sns',
                '17PwSut4FuXhuK9hMZVJI5qy9UliL3o_pSfY14taLRyI']

creds = ServiceAccountCredentials.from_json_keyfile_name('sabordecasakey.json', scope)
client = gspread.authorize(creds)

gc = gspread.authorize(creds)
sh = gc.open_by_key(id_fromulario[0])

hoja_datos = sh.sheet1
datos = hoja_datos.get_all_values()

df = pd.DataFrame(datos[1:], columns=datos[0])

for i in df[df.Enviado == ''].index:
    #Cotizacion
    cotización = df.iloc[i]
    #Datos
    
    nombre = cotización['Nombres y Apellidos'].split()[0]
    celular = cotización['Celular']
    mensaje = 'Hola *' + nombre + '*! Muchas gracias por realizar una cotización de *Desayuno Personalizado* con nosotros. Estamos emocionados de ayudarte a empezar el día con un delicioso desayuno a tu gusto. Estamos aquí para hacer de tu experiencia algo especial y memorable. ¡Estaremos en contacto pronto!'
    #
    sendwhatmsg_instantly("+51" + celular, mensaje,tab_close=True,close_time=4)
    #Actualiza campo
    hoja_datos.update_cell(2 + i, 9, True)
    
    print("Mensaje enviado a ",nombre," con el número de celular ", celular)
    sleep(5)