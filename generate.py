import os 
import io
import textwrap
from groq import Groq
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont
import requests

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

def get_font(size):
    font_path = "/tmp/Oswald-Bold.ttf"
    if not os.path.exists(font_path):
        print("Downloading font...")
        url = "https://github.com/google/fonts/raw/main/ofl/oswald/Oswald-Bold.ttf"
        r = requests.get(url)
        with open(font_path, "wb") as f:
            f.write(r.content)
        print("Font downloaded!")
    return ImageFont.truetype(font_path, size)

def generate_caption(topic):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": f"""
                Write a LinkedIn post about {topic}.
                - Motivational but engaging tone
                - Maximum 150 words
                - Include 5 relevant hashtags at the end
                - Include 1-2 emojis
                """
            }
        ]
    )
    return response.choices[0].message.content


def generate_image(topic, caption):
    HF_TOKEN = os.getenv("HF_TOKEN")
    API_URL = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    
    prompt_response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": f"""Create a short image generation prompt based on:
                Topic: "{topic}"
                Caption: "{caption[:200]}"
                Rules:
                - Visually represent the EXACT emotion and message of this caption
                - Cinematic, photorealistic scene, dramatic lighting
                - No faces, no text in image
                - Bright and vivid colors
                - Maximum 20 words
                - Return ONLY the prompt, nothing else"""
            }
        ]
    )
    
    image_prompt = prompt_response.choices[0].message.content.strip()
    print("Image prompt:", image_prompt)
    
    print("Generating image...")
    response = requests.post(
        API_URL,
        headers=headers,
        json={"inputs": image_prompt},
        timeout=60
    )
    
    if response.status_code != 200:
        print("Error:", response.content[:200])
        return None
    
    image = Image.open(io.BytesIO(response.content)).convert("RGB")
    W, H = image.size
    print(f"Image size: {W}x{H}")

    font_title = get_font(110)

    headline = topic
    wrapped = textwrap.wrap(headline, width=12)
    print("Wrapped:", wrapped)

    line_height = 125
    total_text_h = len(wrapped) * line_height
    y = (H - total_text_h) // 2

    draw = ImageDraw.Draw(image)
    
    for line in wrapped:
        bbox = draw.textbbox((0, 0), line, font=font_title)
        text_w = bbox[2] - bbox[0]
        x = (W - text_w) // 2
        for dx, dy in [(-4,-4),(4,-4),(-4,4),(4,4),(-4,0),(4,0),(0,-4),(0,4)]:
            draw.text((x+dx, y+dy), line, font=font_title, fill="black")
        draw.text((x, y), line, font=font_title, fill="#FFD700")
        y += line_height

    image.save("image.png")
    print("Image saved!")
    return "image.png"