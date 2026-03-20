import os 
import io
import textwrap
from groq import Groq
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont
import requests

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
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


def get_pexels_image(query):
    headers = {"Authorization": PEXELS_API_KEY}
    response = requests.get(
        "https://api.pexels.com/v1/search",
        headers=headers,
        params={"query": query, "per_page": 5, "orientation": "square"}
    )
    data = response.json()
    photos = data.get("photos", [])
    if not photos:
        return None
    import random
    photo = random.choice(photos)
    image_url = photo["src"]["large"]
    img_response = requests.get(image_url, timeout=30)
    return Image.open(io.BytesIO(img_response.content)).convert("RGB")


def generate_image(topic, caption):
    search_query_response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": f"""Give me a 2-3 word Pexels image search query for this motivational topic: "{topic}"
                - Should return beautiful, inspiring photos
                - Examples: "mountain sunrise", "ocean waves", "forest path"
                - Return ONLY the search query, nothing else"""
            }
        ]
    )
    
    search_query = search_query_response.choices[0].message.content.strip()
    print("Pexels search query:", search_query)
    
    image = get_pexels_image(search_query)
    if image is None:
        image = get_pexels_image("motivation success")
    if image is None:
        print("Image fetch failed!")
        return None
    
    W, H = image.size
    print(f"Image size: {W}x{H}")

    overlay = Image.new("RGBA", image.size, (0, 0, 0, 110))
    image = Image.alpha_composite(image.convert("RGBA"), overlay).convert("RGB")

    font_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ArchivoBlack-Regular.ttf")
    print("Font exists:", os.path.exists(font_path))

    padding_x = 40
    padding_y = 40
    max_text_width = W - (padding_x * 2)

    draw = ImageDraw.Draw(image)

    font_size = 40
    font_title = ImageFont.truetype(font_path, font_size)
    wrapped = textwrap.wrap(topic, width=18)

    while font_size > 20:
        font_title = ImageFont.truetype(font_path, font_size)
        wrapped = textwrap.wrap(topic, width=18)
        fits = all(
            draw.textbbox((0, 0), line, font=font_title)[2] <= max_text_width
            for line in wrapped
        )
        if fits:
            break
        font_size -= 4

    print(f"Font size used: {font_size}")
    print("Wrapped:", wrapped)

    line_height = int(font_size * 1.3)
    total_text_h = len(wrapped) * line_height
    
    max_text_height = H - (padding_y * 2)
    if total_text_h > max_text_height:
        total_text_h = max_text_height

    y = (H - total_text_h) // 2

    for line in wrapped:
        if y + line_height > H - padding_y:
            break
        bbox = draw.textbbox((0, 0), line, font=font_title)
        text_w = bbox[2] - bbox[0]
        x = (W - text_w) // 2
        for dx, dy in [(-3,-3),(3,-3),(-3,3),(3,3),(-3,0),(3,0),(0,-3),(0,3)]:
            draw.text((x+dx, y+dy), line, font=font_title, fill="black")
        draw.text((x, y), line, font=font_title, fill="#FFD700")
        y += line_height

    image.save("image.png")
    print("Image saved!")
    return "image.png"