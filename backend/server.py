from typing import Union
from fastapi import FastAPI
from gramformer import Gramformer

from fastapi import Body, FastAPI, status
from fastapi.responses import JSONResponse

gf = Gramformer(models = 1, use_gpu=False) # 1=corrector, 2=detector

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/correct-sentence/{answer}")
def solve_quiz(answer):
    corrected_sentences = gf.correct(answer, max_candidates=1)
    print("[Input] ", answer)
    correct_sentence = list(corrected_sentences)[0]
    print("[Correction] ",correct_sentence)
    return JSONResponse(content={ "correct_sentence": correct_sentence}, status_code=200)

if __name__ == '__main__':
    uvicorn.run(f"{Path(__file__).stem}:app", host="127.0.0.1", port=8888, reload=True)