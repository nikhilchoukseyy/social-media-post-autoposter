import os 
import io
from groq import Groq
from dotenv import load_dotenv
from PIL import Image
import requests
from datetime import date


load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)


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
                - Cinematic, photorealistic scene
                - No faces, no text in image
                - Maximum 20 words
                - Return ONLY the prompt, nothing else"""
            }
        ]
    )
    
    image_prompt = prompt_response.choices[0].message.content.strip()
    print("Image prompt:", image_prompt)
    
    payload = {"inputs": image_prompt}
    
    print("Generating image...")
    response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
    
    if response.status_code != 200:
        print("Error:", response.content[:200])
        return None
    
    from PIL import ImageDraw, ImageFont
    import textwrap
    
    image = Image.open(io.BytesIO(response.content)).convert("RGBA")
    W, H = image.size
    
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 140))
    image = Image.alpha_composite(image, overlay)
    
    try:
        font_title = ImageFont.truetype("arialbd.ttf", 42)
        font_sub = ImageFont.truetype("arial.ttf", 26)
    except:
        font_title = ImageFont.load_default()
        font_sub = font_title
    
    
    headline = caption.split('.')[0]
    wrapped = textwrap.wrap(headline, width=22)
    
    line_height = 55
    total_text_h = len(wrapped) * line_height + 60
    y_start = (H - total_text_h) // 2
    
    box = Image.new("RGBA", image.size, (0, 0, 0, 0))
    box_draw = ImageDraw.Draw(box)
    box_draw.rectangle(
        [(40, y_start - 20), (W - 40, y_start + total_text_h)],
        fill=(0, 0, 0, 160)
    )
    image = Image.alpha_composite(image, box).convert("RGB")
    draw = ImageDraw.Draw(image)
    
    y = y_start + 10
    for line in wrapped:
        bbox = draw.textbbox((0, 0), line, font=font_title)
        text_w = bbox[2] - bbox[0]
        x = (W - text_w) // 2
        for dx, dy in [(-2,-2),(2,-2),(-2,2),(2,2)]:
            draw.text((x+dx, y+dy), line, font=font_title, fill="black")
        draw.text((x, y), line, font=font_title, fill="#FFD700")
        y += line_height
    
    
    
    image.save("image.png")
    print("Image saved!")
    return "image.png"