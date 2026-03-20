import logging 
from generate import generate_caption, generate_image
from post import post_to_linkedin
from datetime import datetime
import json 
import os 

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
    if os.path.exists(INDEX_FILE): 
       with open(INDEX_FILE,"r") as f : 
          index = int(f.read().strip())
    else : 
       index = 0 
    
    with open(QUOTES_FILE,"r",encoding="utf-8") as f :
       quotes = json.load(f)

    if index > len(quotes): 
       index = 0
       logger.warning("All quotes are used ! Restarting from beginning")

    item = quotes[index]
    quote = item.get("quote","").strip()
    author = item.get("author","Unknown").strip()

    with open(INDEX_FILE,"w") as f: 
       f.write(str(index+1))

    logger.info(f"Quote #{index} selected. Remaining: {len(quotes) - index - 1}")
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
