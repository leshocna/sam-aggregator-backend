# Unified SAM.gov Aggregator Backend

This FastAPI backend aggregates federal contracting opportunities from SAM.gov using your API key.

## Features

- Unified endpoint for MILCON and general opportunities
- Filters by keyword, agency, location, NAICS, solicitation type, and funding agency
- CORS enabled for frontend integration (e.g., React app embedded in Wix)
- Environment variable support for API key

## Setup

1. Create a virtual environment and activate it:
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

2. Install dependencies:
   pip install -r requirements.txt

3. Set your SAM.gov API key as an environment variable:
   export SAM_API_KEY=your_api_key_here

4. Run the app locally:
   uvicorn main:app --reload

## Deploying to Render

1. Create a new Web Service on https://render.com
2. Upload this project folder or connect a GitHub repo
3. Set the Start Command:
   uvicorn main:app --host 0.0.0.0 --port 10000
4. Add environment variable:
   SAM_API_KEY=your_api_key_here
