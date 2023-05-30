from fastapi import FastAPI
import random
import mysql.connector
from pydantic import BaseModel
from pydantic.schema import datetime

from starlette.middleware.cors import CORSMiddleware
from kafka import KafkaConsumer
from json import loads
import json


aulaSel = "ateca"

def cambiarAula():
    global consumerHumedad
    global consumerRuido
    global consumerTemperatura
    global consumerLuminosidad
    global aulaSel


    consumerHumedad = KafkaConsumer(
            'humedadAULA'+aulaSel,
            enable_auto_commit=True,
            value_deserializer=lambda m: loads(m.decode('utf-8')),
            bootstrap_servers=['172.17.10.33:9092', '172.17.10.34:9092', '172.17.10.35:9092'])

    consumerRuido = KafkaConsumer(
        'ruidoAULA'+aulaSel,
        enable_auto_commit=True,
        value_deserializer=lambda m: loads(m.decode('utf-8')),
        bootstrap_servers=['172.17.10.33:9092', '172.17.10.34:9092', '172.17.10.35:9092'])

    consumerTemperatura = KafkaConsumer(
        'temperaturaAULA'+aulaSel,
        enable_auto_commit=True,
        value_deserializer=lambda m: loads(m.decode('utf-8')),
        bootstrap_servers=['172.17.10.33:9092', '172.17.10.34:9092', '172.17.10.35:9092'])

    consumerLuminosidad = KafkaConsumer(
        'luminosidadAULA'+aulaSel,
        enable_auto_commit=True,
        value_deserializer=lambda m: loads(m.decode('utf-8')),
        bootstrap_servers=['172.17.10.33:9092', '172.17.10.34:9092', '172.17.10.35:9092'])

def obtenerPayload(data: str):
    data = json.dumps(data)
    start_index = data.find("'payload':") + len("'payload':")
    end_index = data.find(",", start_index)
    return data[start_index:end_index].strip().replace(',', '.')


def recibirDatosHumedad():
    for m in consumerHumedad:
        return obtenerPayload(str(m.value))
def recibirDatosRuido():
    for m in consumerRuido:
        return obtenerPayload(str(m.value))
def recibirDatosTemperatura():
    for m in consumerTemperatura:
        return obtenerPayload(eval(str(m.value)))
def recibirDatosLuminosidad():
    for m in consumerLuminosidad:
        return obtenerPayload(str(m.value))

cambiarAula()

app = FastAPI()

mydb = mysql.connector.connect(
    host="172.17.10.30",
    user="android",
    password="android",
    database="android"
)



class User(BaseModel):
    nombre: str
    token: str
    rol: int

@app.get("/")
async def root():
    return {"temperatura": str(random.randint(1, 50)), "ruido": str(random.randint(1, 90)),
            "bares": str(random.randint(900, 1500))}


@app.get("/obtenerModulos")
async def obtenerModulos():
    mycursor = mydb.cursor()
    query = "SELECT * FROM modulo WHERE activo=True"
    mycursor.execute(query)
    results = []
    for row in mycursor.fetchall():
        results.append({
            'id': row[0],
            'nombre': row[1],
            'activo': row[2]
        })
    mycursor.close()

    return results

@app.get("/obtenerRol")
async def obtenerRol():
    mycursor = mydb.cursor()
    query = "SELECT * FROM rol"
    mycursor.execute(query)
    results = []
    for row in mycursor.fetchall():
        results.append({
            'id': row[0],
            'nombre': row[1]
        })
    mycursor.close()

    return results

@app.get("/obtenerDatosGenerales")
async def obtenerDatosGenerales():
    return {"temperatura": recibirDatosTemperatura(),"ruido":recibirDatosRuido(),"humedad": recibirDatosHumedad(), "luminosidad": recibirDatosLuminosidad()}

@app.get("/cambiarAula/{aula}")
async def cambiar_aula(aula: str):
    global aulaSel
    aulaSel = aula
    cambiarAula()


@app.post("/crearUsuario")
async def crearUsuario(user: User):
    result = False
    mycursor = mydb.cursor()
    query = "INSERT INTO user (nombre, token, date_last_signUp, rol) VALUES (%s, %s, %s, %s)"
    values = (user.nombre, user.token, datetime.now(), user.rol)
    mycursor.execute(query, values)
    mydb.commit()
    if mycursor.rowcount > 0:
        result = True
    else:
        result = False
    mycursor.close()

    return result


if __name__ ==  '__main__':
    import uvicorn

    origins = ['http://localhost:8000', 'http://informatica.iesalbarregas.com:8888']

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    uvicorn.run(app, host='0.0.0.0', port=8000)

