from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
import pickle

from pathlib import Path

from fastapi.templating import Jinja2Templates


MAIN_DIR_PATH = Path(__file__).parent
templates = Jinja2Templates(directory=MAIN_DIR_PATH.joinpath('templates'))


app = FastAPI()
model = pickle.load(open('model.pkl', 'rb'))


@app.post('/predict', response_class=HTMLResponse)
def predict(request: Request, rooms: str = Form(...), distance: str = Form(...) ):
    roomsi = int(rooms)
    distancei = int(distance)
    prediction = model.predict([[roomsi, distancei]])
    output = round(prediction[0], 2)
    prediction_text=f'A house with {roomsi} rooms per dwelling and located {distancei} km to employment centers has a value of ${output}K'
    return templates.TemplateResponse('index.html', {'request': request, 'prediction_text': prediction_text})

@app.get('/', response_class=HTMLResponse)
def main(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})
##if __name__ == "__main__":
##app.run()