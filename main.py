from fastapi import FastAPI
import random
import mysql.connector
from pydantic import BaseModel
from pydantic.schema import datetime

from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="admin",
    database="smartclassroommonitor"
)

data = {"id": 1, "nombre": "John Doe", "activo": True}


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
    return {"temperatura": str(random.randint(1, 50)), "ruido": str(random.randint(1, 90)),
            "bares": str(random.randint(900, 1500))}


@app.get("/obtenerDatosModulo/{id}")
async def obtenerDatosModulo(id: str):
    return {"temperatura": str(random.randint(1, 50)), "ruido": str(random.randint(1, 90)),
            "bares": str(random.randint(900, 1500))}

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


if __name__ == '__main__':
    import uvicorn

    origins = ['http://localhost:8888', 'http://informatica.iesalbarregas.com:8888']

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    uvicorn.run(app, host='0.0.0.0', port=8888)
