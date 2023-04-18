from fastapi import FastAPI
import random
import mysql.connector

from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="user",
    password="pass",
    database="nameDB"
)
@app.get("/")
async def root():
    return {"temperatura": str(random.randint(1, 50)),"ruido":str(random.randint(1, 90)),"bares":str(random.randint(900, 1500))}

@app.get("/obtenerModulos")
async def obtenerModulos():
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM modulo")

    myresult = mycursor.fetchall()
    return {"result": myresult}

@app.get("/obtenerDatosGenerales")
async def obtenerDatosGenerales():
    return {"temperatura": str(random.randint(1, 50)),"ruido":str(random.randint(1, 90)),"bares":str(random.randint(900, 1500))}


@app.get("/obtenerDatosModulo/{id}")
async def obtenerDatosModulo(id: str):
    return {"temperatura": str(random.randint(1, 50)),"ruido":str(random.randint(1, 90)),"bares":str(random.randint(900, 1500))}


if __name__ == '__main__':
    import uvicorn

    origins = ['http://localhost:8888']

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    uvicorn.run(app, host='0.0.0.0', port=8888)
