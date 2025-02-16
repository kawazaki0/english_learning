from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from app.lemma_file_storage import LemmaFileStorage
from app.dictionary import Dictionary

app = FastAPI()
templates = Jinja2Templates(directory="templates")

known_lemmas_store = LemmaFileStorage("known_lemmas.txt")
lemmas_to_learn_store = LemmaFileStorage("lemmas_to_learn.txt")


class TextInput(BaseModel):
    text: str


@app.get("/", response_class=HTMLResponse)
async def get_form():
    return templates.TemplateResponse("form.html", {"request": {}})


@app.post("/process", response_class=HTMLResponse)
async def process_text(text: str = Form(...)):
    dictionary = Dictionary()
    dictionary.import_raw_text(text)
    known_lemmas = known_lemmas_store.load_lines_to_set()
    unknown_lemmas = [word.lemma for word in dictionary.words if word.lemma not in known_lemmas]
    recognized_lemmas = [word.lemma for word in dictionary.words if word.lemma in known_lemmas]

    return templates.TemplateResponse("result.html", {"request": {}, "recognized_lemmas": recognized_lemmas, "unknown_lemmas": unknown_lemmas})

@app.get("/add_as_known/{lemma}", response_class=HTMLResponse)
async def add_as_known(lemma: str):
    known_lemmas_store.save(lemma)
    return HTMLResponse(f"added as known")

@app.get("/add_to_learn/{lemma}", response_class=HTMLResponse)
async def add_to_learn(lemma: str):
    lemmas_to_learn_store.save(lemma)
    return HTMLResponse(f"added to learn")
