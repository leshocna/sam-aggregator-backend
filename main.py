from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from datetime import datetime, timedelta

app = FastAPI()

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    limit: int = Query(20)
):
    headers = {"X-API-KEY": SAM_API_KEY}
    base_url = "https://api.sam.gov/prod/opportunities/v2/search"

    # Format postedFrom and postedTo as MM/dd/yyyy
    posted_to = datetime.utcnow()
    posted_from = posted_to - timedelta(days=30)
    posted_from_str = posted_from.strftime("%m/%d/%Y")
    posted_to_str = posted_to.strftime("%m/%d/%Y")

    params = {
        "limit": limit,
        "noticeType": "Presolicitation,Combined Synopsis/Solicitation",
        "sort": "-publishedDate",
        "postedFrom": posted_from_str,
        "postedTo": posted_to_str
    }

    if keyword:
        params["q"] = keyword
    if agency:
        params["agency"] = agency
    if location:
        params["placeOfPerformance"] = location
    if naics:
        params["naics"] = naics
    if solicitation_type:
        params["solicitationType"] = solicitation_type
    if funding_agency:
        params["fundingAgency"] = funding_agency

    response = requests.get(base_url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        for item in data.get("opportunitiesData", []):
            title = item.get("title", "").lower()
            if "military construction" in title or "usace" in title or "milcon" in title:
                item["category"] = "MILCON"
            else:
                item["category"] = "General"
        return data
    else:
        return {
            "error": "Failed to fetch data from SAM.gov",
            "status_code": response.status_code,
            "request_url": response.url,
            "params": params,
            "response_body": response.text
        }

