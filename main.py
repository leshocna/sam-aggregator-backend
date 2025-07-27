
from datetime import datetime, timedelta
import os
import requests
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path="opportunity-radar-frontend.env")

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://opportunity-radar-frontend.onrender.com",
        "https://www.trustedstructuresllc.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SAM_API_KEY = os.getenv("SAM_API_KEY")

@app.get("/opportunities")
def get_opportunities(
    keyword: str = Query(None),
    agency: str = Query(None),
    location: str = Query(None),
    naics: str = Query(None),
    solicitation_type: str = Query(None),
    funding_agency: str = Query(None),
    limit: int = Query(100)
):
    headers = {"X-API-KEY": SAM_API_KEY}
    base_url = "https://api.sam.gov/prod/opportunities/v2/search"

    # Default filters
    default_naics = ["237310", "238110", "238120", "236220", "541330"]
    default_states = ["PA", "VA", "DC"]
    default_keywords = ["concrete"]

    # Date range: last 30 days
    posted_to = datetime.utcnow()
    posted_from = posted_to - timedelta(days=30)
    posted_from_str = posted_from.strftime("%m/%d/%Y")
    posted_to_str = posted_to.strftime("%m/%d/%Y")

    params = {
        "limit": limit,
        "noticeType": "Presolicitation,Solicitation,Combined Synopsis/Solicitation",
        "sort": "-publishedDate",
        "postedFrom": posted_from_str,
        "postedTo": posted_to_str,
        "active": "Yes"
    }

    if keyword:
        params["q"] = keyword
    else:
        params["q"] = " OR ".join(default_keywords)

    if agency:
        params["agency"] = agency

    if location:
        params["placeOfPerformance"] = location
    else:
        params["placeOfPerformance"] = ",".join(default_states)

    if naics:
        params["naics"] = naics
    else:
        params["naics"] = ",".join(default_naics)

    if solicitation_type:
        params["solicitationType"] = solicitation_type

    if funding_agency:
        params["fundingAgency"] = funding_agency

    response = requests.get(base_url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        filtered_opps = [
            opp for opp in data.get("opportunitiesData", [])
            if opp.get("naicsCode") in default_naics
        ]
        return {"opportunitiesData": filtered_opps}
    else:
        return {
            "error": "Failed to fetch data from SAM.gov",
            "status_code": response.status_code,
            "request_url": response.url,
            "params": params,
            "response_body": response.text
        }

# Port binding for Render deployment
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("main_v12:app", host="0.0.0.0", port=port, reload=True)
