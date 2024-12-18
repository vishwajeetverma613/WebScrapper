from pydantic import BaseModel
from typing import Optional

STATIC_TOKEN = "your-static-token"  # Replace this with your token
STORAGE_FILE_PATH = "data/scraped_data.json"
IMAGE_STORAGE_FILE_PATH = "data/images"

class ScraperConfig(BaseModel):
    max_pages: Optional[int] = 5
    proxy: Optional[str] = None
