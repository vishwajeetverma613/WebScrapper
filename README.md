
# Web Scraping Tool with FastAPI

## Overview

This project is a simple web scraping tool built with **FastAPI** and Python. The tool scrapes product data (name, price, and image) from the **Dental Stall** product catalog and stores it in a local JSON file. It features basic authentication and a caching mechanism to avoid updating unchanged product prices.

## Features
- **Web Scraping**: Extract product details like title, price, image, and description.
- **API Integration**: Access scraped data via a REST API.
- **Caching**: Avoid redundant processing using a simple in-memory cache.
- **Bulk Create/Update**: Efficiently handles large datasets.
- **JSON Storage**: Save data locally in structured JSON format.
- **Image Handling**: Downloads product images for offline use.


## Requirements
- Python 3.8+
- FastAPI
- Requests
- BeautifulSoup4
- Hypercorn (for running FastAPI)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/scraping-tool.git
    cd scraping-tool
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Make sure to have an image folder (`images/`) where product images will be saved.

## Configuration

- **Static Token**: Replace `STATIC_TOKEN` in `config.py` with your actual authentication token.
- **Data Storage Path**: Replace `STORAGE_FILE_PATH` in `config.py` with your desired file path.
- **Image Storage PAth**: Replace `IMAGE_STORAGE_FILE_PATH` in `config.py` with your desired file path.
- **Scraping Configuration**: You can adjust the number of pages to scrape and provide a proxy string by modifying the request to the `/scrape/` endpoint.


## Running the Application


To run the FastAPI app, use **Hypercorn**:

```bash
hypercorn app:app --reload
```

## Curl for the API:--

```curl --location 'localhost:8000/scrape/?token=your-static-token' \
--header 'Content-Type: application/json' \
--data '{
    "max_pages": 6
}'```