import uvicorn
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from dashboard import app as combustibleDashboard
import pandas as pd
from db import engine


# Define the FastAPI server
app = FastAPI()
# Mount the Dash app as a sub-application in the FastAPI server
app.mount("/dashboard", WSGIMiddleware(combustibleDashboard.server))

@app.get("/")
def index():
    return "Go to /dashboard or to /api/combustibles"

# Define the main API endpoint
@app.get("/api/combustibles")
def index():
    try:
        df = pd.read_sql("""
            SELECT *
                FROM public.donnees_emissions
                WHERE "Statut de l'élément" IN ('Valide générique', 'Valide spécifique')
                AND "code1" = 'Combustibles'
                AND "Sous-localisation géographique français" = 'France continentale'
            """, con=engine)
        df = df.fillna('')
        print(df)
        return {"data": df.to_dict(orient="records")}
    except Exception as e:
        return {"error": str(e)}


# Start the FastAPI server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8050)
