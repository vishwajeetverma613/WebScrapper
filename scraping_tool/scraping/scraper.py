import os
import requests
from bs4 import BeautifulSoup
from scraping_tool.scraping.cache import product_cache
from scraping_tool.scraping.utils import save_image
from scraping_tool.storage.storage import JSONDataHandler
import time
import re

class ProductScraper:
    def __init__(self, config, json_file_path, image_store_file_path):
        self.config = config
        self.base_url = "https://dentalstall.com/shop/"
        self.products = []
        self.data_handler = JSONDataHandler(json_file_path)
        self.image_store_file_path = image_store_file_path

    def fetch_page(self, page_num, retries=3):
        url = f"{self.base_url}page/{page_num}/"
        for attempt in range(retries):
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                return response.content
            except requests.exceptions.RequestException:
                time.sleep(5)
                continue
        return None
    

    # Remove non-numeric characters (including the currency symbol) and convert the price to an integer
    def clean_price(self, price_str: str) -> int:
        # Remove non-numeric characters (keeping only numbers and decimal points)
        cleaned_price = re.sub(r"[^\d.]", "", price_str)
        
        # Convert the cleaned string to a float and then to an integer (if you want to discard decimals)
        return int(float(cleaned_price))


    def parse_product_details(self, product_card):
        try:
            # Extract product title
            title_element = product_card.find("h2", class_="woo-loop-product__title")
            product_title = title_element.get_text(strip=True) if title_element else "Unknown Title"
            
            # Extract product price
            price_element = product_card.find("ins") or product_card.find("bdi")
            product_price = self.clean_price(price_element.get_text(strip=True)) if price_element else None


            # Extract image URL
            thumbnail_div = product_card.find("div", class_="mf-product-thumbnail")

            thumbnail_div.find("img")
            if thumbnail_div:
                image_element = thumbnail_div.find("img")
                image_url = image_element.get("data-lazy-src") if image_element else None
            else:
                image_url = None

            # Save the image locally
            sanitized_title = "".join(c if c.isalnum() or c in "_-" else "_" for c in product_title)
            image_path = f"{self.image_store_file_path}/{sanitized_title}.jpg"
            if image_url:
                save_image(image_url, image_path)
            
            # Extract short description (if available)
            short_desc_element = product_card.find("div", class_="woocommerce-product-details__short-description")
            short_description = short_desc_element.get_text(strip=True) if short_desc_element else "No Description"
            
            return {
                "product_title": product_title,
                "product_price": product_price,
                "path_to_image": image_path,
                "short_description": short_description
            }
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"Error parsing product details: {e}")
            return None


    def scrape(self):
        for page_num in range(1, self.config.max_pages + 1):
            page_content = self.fetch_page(page_num)
            if page_content is None:
                print(f"Failed to retrieve page {page_num}")
                continue
            soup = BeautifulSoup(page_content, "html.parser")
            product_cards = soup.find_all("ul", class_="products")
            for card in product_cards:
                li_items = card.find_all("li", class_="product")  # Find all <li> within the current <ul>
                for li in li_items:
                    product_data = self.parse_product_details(li)
                    self.update_cache(product_data)
            print(f"Scraping completed for page {page_num}.")

    def update_cache(self, product_data):
        short_description = product_data["short_description"]
        price = product_data["product_price"]
        cached_price = product_cache.get(short_description)
        if cached_price != price:
            product_cache[short_description] = price
            self.products.append(product_data)

    def save_to_json(self):
        self.data_handler.bulk_create_or_update(unique_key_identifier='short_description', records=self.products)

    def notify_status(self):
        print(f"Scraping completed. {len(self.products)} new products added.")
