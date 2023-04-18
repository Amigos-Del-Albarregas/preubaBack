from fastapi import FastAPI
import random

from starlette.middleware.cors import CORSMiddleware

app = FastAPI()


@app.get("/obtenerMierda")
async def root():
    return {"temperatura": str(random.randint(1, 50)),"ruido":str(random.randint(1, 90)),"bares":str(random.randint(900, 1500))}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


if __name__ == '__main__':
    import uvicorn

    origins = ['http://localhost:8000', 'http://192.168.137.1:8000']

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    uvicorn.run(app, host='0.0.0.0', port=8000)