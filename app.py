from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
import pickle


from pathlib import Path

from fastapi.templating import Jinja2Templates

try:
    import jinja2

    # @contextfunction was renamed to @pass_context in Jinja 3.0, and was removed in 3.1
    # hence we try to get pass_context (most installs will be >=3.1)
    # and fall back to contextfunction,
    # adding a type ignore for mypy to let us access an attribute that may not exist
    if hasattr(jinja2, "pass_context"):
        pass_context = jinja2.pass_context
    else:  # pragma: nocover
        pass_context = jinja2.contextfunction  # type: ignore[attr-defined]
except ImportError:  # pragma: nocover
    jinja2 = None  # type: ignore[assignment]


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