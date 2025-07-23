{
    "chunks": [
        {
            "type": "txt",
            "chunk_number": 1,
            "lines": [
                {
                    "line_number": 1,
                    "text": "from fastapi import FastAPI, Query"
                },
                {
                    "line_number": 2,
                    "text": "from fastapi.middleware.cors import CORSMiddleware"
                },
                {
                    "line_number": 3,
                    "text": "import requests"
                },
                {
                    "line_number": 4,
                    "text": "import os"
                },
                {
                    "line_number": 5,
                    "text": ""
                },
                {
                    "line_number": 6,
                    "text": "app = FastAPI()"
                },
                {
                    "line_number": 7,
                    "text": ""
                },
                {
                    "line_number": 8,
                    "text": "# Enable CORS for frontend integration"
                },
                {
                    "line_number": 9,
                    "text": "app.add_middleware("
                },
                {
                    "line_number": 10,
                    "text": "CORSMiddleware,"
                },
                {
                    "line_number": 11,
                    "text": "allow_origins=[\"*\"],"
                },
                {
                    "line_number": 12,
                    "text": "allow_credentials=True,"
                },
                {
                    "line_number": 13,
                    "text": "allow_methods=[\"*\"],"
                },
                {
                    "line_number": 14,
                    "text": "allow_headers=[\"*\"],"
                },
                {
                    "line_number": 15,
                    "text": ")"
                },
                {
                    "line_number": 16,
                    "text": ""
                },
                {
                    "line_number": 17,
                    "text": "SAM_API_KEY = os.getenv(\"SAM_API_KEY\")"
                },
                {
                    "line_number": 18,
                    "text": ""
                },
                {
                    "line_number": 19,
                    "text": "@app.get(\"/opportunities\")"
                },
                {
                    "line_number": 20,
                    "text": "def get_opportunities("
                },
                {
                    "line_number": 21,
                    "text": "keyword: str = Query(None),"
                },
                {
                    "line_number": 22,
                    "text": "agency: str = Query(None),"
                },
                {
                    "line_number": 23,
                    "text": "location: str = Query(None),"
                },
                {
                    "line_number": 24,
                    "text": "naics: str = Query(None),"
                },
                {
                    "line_number": 25,
                    "text": "solicitation_type: str = Query(None),"
                },
                {
                    "line_number": 26,
                    "text": "funding_agency: str = Query(None),"
                },
                {
                    "line_number": 27,
                    "text": "limit: int = Query(20)"
                },
                {
                    "line_number": 28,
                    "text": "):"
                },
                {
                    "line_number": 29,
                    "text": "headers = {\"X-API-KEY\": SAM_API_KEY}"
                },
                {
                    "line_number": 30,
                    "text": "base_url = \"https://api.sam.gov/prod/opportunities/v2/search\""
                },
                {
                    "line_number": 31,
                    "text": "params = {"
                },
                {
                    "line_number": 32,
                    "text": "\"limit\": limit,"
                },
                {
                    "line_number": 33,
                    "text": "\"noticeType\": \"Presolicitation,Combined Synopsis/Solicitation\","
                },
                {
                    "line_number": 34,
                    "text": "\"sort\": \"-publishedDate\""
                },
                {
                    "line_number": 35,
                    "text": "}"
                },
                {
                    "line_number": 36,
                    "text": ""
                },
                {
                    "line_number": 37,
                    "text": "if keyword:"
                },
                {
                    "line_number": 38,
                    "text": "params[\"q\"] = keyword"
                },
                {
                    "line_number": 39,
                    "text": "if agency:"
                },
                {
                    "line_number": 40,
                    "text": "params[\"agency\"] = agency"
                },
                {
                    "line_number": 41,
                    "text": "if location:"
                },
                {
                    "line_number": 42,
                    "text": "params[\"placeOfPerformance\"] = location"
                },
                {
                    "line_number": 43,
                    "text": "if naics:"
                },
                {
                    "line_number": 44,
                    "text": "params[\"naics\"] = naics"
                },
                {
                    "line_number": 45,
                    "text": "if solicitation_type:"
                },
                {
                    "line_number": 46,
                    "text": "params[\"solicitationType\"] = solicitation_type"
                },
                {
                    "line_number": 47,
                    "text": "if funding_agency:"
                },
                {
                    "line_number": 48,
                    "text": "params[\"fundingAgency\"] = funding_agency"
                },
                {
                    "line_number": 49,
                    "text": ""
                },
                {
                    "line_number": 50,
                    "text": "response = requests.get(base_url, headers=headers, params=params)"
                },
                {
                    "line_number": 51,
                    "text": "if response.status_code == 200:"
                },
                {
                    "line_number": 52,
                    "text": "data = response.json()"
                },
                {
                    "line_number": 53,
                    "text": "for item in data.get(\"opportunitiesData\", []):"
                },
                {
                    "line_number": 54,
                    "text": "title = item.get(\"title\", \"\").lower()"
                },
                {
                    "line_number": 55,
                    "text": "if \"military construction\" in title or \"usace\" in title or \"milcon\" in title:"
                },
                {
                    "line_number": 56,
                    "text": "item[\"category\"] = \"MILCON\""
                },
                {
                    "line_number": 57,
                    "text": "else:"
                },
                {
                    "line_number": 58,
                    "text": "item[\"category\"] = \"General\""
                },
                {
                    "line_number": 59,
                    "text": "return data"
                },
                {
                    "line_number": 60,
                    "text": "else:"
                },
                {
                    "line_number": 61,
                    "text": "return {\"error\": \"Failed to fetch data\", \"status_code\": response.status_code}"
                }
            ],
            "token_count": 305
        }
    ]
}
