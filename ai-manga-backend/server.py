from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:8000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def main():
    return {"message": "Hello World"}

@app.post("/translate")
async def get_body(request):
    text_to_translate = await request.body()
    def freyaTODO(text):
        return [
            ['orig1', 'trans1'],
            ['orig2', 'trans2'],
            ['orig3', 'trans3'],
            ['orig4', 'trans4'],
            ['orig5', 'trans5'],
            ['orig6', 'trans6'],
        ]
    return freyaTODO(text_to_translate)
