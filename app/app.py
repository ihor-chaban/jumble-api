from fastapi import FastAPI, HTTPException, Header
import random

app = FastAPI()

def authenticate_api_key(api_key: str=Header(...)):
    if api_key != "my-secret-api-key":
        raise HTTPException(status_code=401, detail="Invalid API key")

@app.get("/random_word/{word}")
async def randomize_word(word: str):
    word_list = list(word)
    random.shuffle(word_list)
    return "".join(word_list)

@app.get("/random_word_with_auth/{word}")
def random_word_with_auth(word: str, api_key: str = Header(..., alias="Authorization")):
    authenticate_api_key(api_key)
    word_list = list(word)
    random.shuffle(word_list)
    return "".join(word_list)
