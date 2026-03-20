import logging 
from generate import generate_caption, generate_image
from post import post_to_linkedin
from datetime import datetime
import json 
import os 
import random

logging.basicConfig(
  level=logging.INFO,
  format="%(asctime)s - %(levelname)s - %(message)s",
  handlers=[
    logging.FileHandler("autoposter.log"),
    logging.StreamHandler()
  ]
)
logger = logging.getLogger(__name__)


QUOTES_FILE = "quotes.json"
INDEX_FILE = "index.txt"


def get_topic():
    with open(QUOTES_FILE, "r", encoding="utf-8") as f:
        quotes = json.load(f)
    
  
    seed = int(datetime.now().timestamp())
    random.seed(seed)
    
    item = random.choice(quotes)
    quote = item.get("quote", "").strip()
    author = item.get("author", "Unknown").strip()
    
    logger.info(f"Quote selected: {quote[:40]}...")
    return f"{quote} — {author}"

def run():
    logger.info("=== AutoPoster Started ===")
    
    try:
      topic = get_topic()
      
      logger.info("Generating caption...")
      caption = generate_caption(topic)
      logger.info(f"Caption generated: {caption[:50]}...")
      
      logger.info("Generating image...")
      image_path = generate_image(topic, caption)
      
      if image_path is None:
        logger.error("Image generation failed!")
        return
      
      logger.info(f"Image saved: {image_path}")
      
      logger.info("Posting to LinkedIn...")
      post_to_linkedin(caption, image_path)
      
      logger.info("=== Post Successful! ===")
        
    except Exception as e:
      logger.error(f"Something went wrong: {e}")

if __name__ == "__main__":
  run()

