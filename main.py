import logging 
from generate import generate_caption, generate_image
from post import post_to_linkedin
from datetime import datetime

logging.basicConfig(
  level=logging.INFO,
  format="%(asctime)s - %(levelname)s - %(message)s",
  handlers=[
    logging.FileHandler("autoposter.log"),
    logging.StreamHandler()
  ]
)
logger = logging.getLogger(__name__)


def get_topic():
    from generate import client
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": """Give me ONE unique motivational quote for a LinkedIn post today.
                - Should be fresh and specific , length should be 25-30 words"""
            }
        ]
    )
    
    topic = response.choices[0].message.content.strip()
    logger.info(f"Topic selected: {topic}")
    return topic 


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
