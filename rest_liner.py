from fastapi import FastAPI, Query
from starlette.responses import HTMLResponse
from sklearn.linear_model import LogisticRegression
import numpy as np
import math

app = FastAPI(title="Logistic Regression API")

X = np.array([30, 35, 40, 45, 50, 55, 60, 65, 70, 75]).reshape(-1, 1)
y = np.array([0, 0, 0, 0, 0, 1, 0, 1, 1, 1])

model = LogisticRegression(solver="liblinear")
model.fit(X, y)

# Extract coefficients
b0 = model.intercept_[0]
b1 = model.coef_[0][0]

def predict_probability(x: float) -> float:
    z = b0 + b1 * x
    return 1 / (1 + math.exp(-z))

@app.get("/logistic/predict")
def logistic_predict(x: float = Query(..., description="Annual income")):
    prob = predict_probability(x)
    return {
        "x": x,
        "probability": round(prob, 2)
    }

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title>My Home Page</title>
        </head>
        <body>
            <h1>Welcome to Logistic Regression API 🚀</h1>
            <p>Try: <a href="./logistic/predict?x=55">Predict for x=55</a></p>
        </body>
    </html>
    """