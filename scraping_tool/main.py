from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from scraping_tool.scraping.scraper import ProductScraper
from scraping_tool.config import STATIC_TOKEN, ScraperConfig, STORAGE_FILE_PATH, IMAGE_STORAGE_FILE_PATH

app = FastAPI()
security = HTTPBearer()

def authenticate(token: str = Query(...)):
    if token != STATIC_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return token

@app.post("/scrape/")
async def start_scraping(config: ScraperConfig, token: str = Depends(authenticate)):
    scraper = ProductScraper(config, STORAGE_FILE_PATH, IMAGE_STORAGE_FILE_PATH)
    try:
        print("Scraping Started")
        scraper.scrape()
        scraper.save_to_json()
        scraper.notify_status()
        return {"message": "Scraping completed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    


if __name__ == "__main__":
    app.run(debug=True)