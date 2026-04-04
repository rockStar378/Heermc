import os
import re
import aiohttp
import aiofiles
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from youtubesearchpython.__future__ import VideosSearch
from config import YOUTUBE_IMG_URL


def clear(text):
    return re.sub("\s+", " ", text).strip()


async def get_thumb(videoid):
    if os.path.isfile(f"cache/{videoid}.png"):
        return f"cache/{videoid}.png"

    try:
        url = f"https://www.youtube.com/watch?v={videoid}"

        results = VideosSearch(url, limit=1)
        data = (await results.next())["result"][0]

        title = data.get("title", "Unsupported Title")
        title = re.sub("\W+", " ", title).title()

        duration = data.get("duration", "Unknown")
        views = data.get("viewCount", {}).get("short", "Unknown Views")
        channel = data.get("channel", {}).get("name", "Unknown Channel")
        thumbnail = data["thumbnails"][0]["url"].split("?")[0]

        # download thumbnail
        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                if resp.status == 200:
                    async with aiofiles.open(f"cache/thumb{videoid}.png", "wb") as f:
                        await f.write(await resp.read())

        youtube = Image.open(f"cache/thumb{videoid}.png").convert("RGBA")

        # background blur
        background = youtube.resize((1280, 720)).filter(ImageFilter.GaussianBlur(10))
        background = ImageEnhance.Brightness(background).enhance(0.6)

        draw = ImageDraw.Draw(background)

        # center image
        center_thumb = youtube.resize((942, 422))

        border = 14
        bordered = Image.new(
            "RGBA",
            (center_thumb.size[0] + border * 2, center_thumb.size[1] + border * 2),
            (255, 255, 255),
        )
        bordered.paste(center_thumb, (border, border))

        pos_x = (1280 - bordered.size[0]) // 2
        pos_y = (720 - bordered.size[1]) // 2 - 30

        background.paste(bordered, (pos_x, pos_y))

        # fonts (FIX PATH)
        arial = ImageFont.truetype("SHREE/assets/font2.ttf", 30)
font = ImageFont.truetype("SHREE/assets/font.ttf", 30)
bold = ImageFont.truetype("SHREE/assets/font.ttf", 33)

        # text
        draw.text((1000, 10), "@YOURBOT", fill="yellow", font=font)

        draw.text((55, 580), f"{channel} | {views}", fill="white", font=arial)
        draw.text((55, 620), title[:50], fill="white", font=font)

        draw.text((55, 655), "00:00", fill="white", font=bold)

        draw.line([(150, 670), (1130, 670)], fill="white", width=4)

        draw.text((1140, 655), duration, fill="white", font=bold)

        os.remove(f"cache/thumb{videoid}.png")

        background.save(f"cache/{videoid}.png")
        return f"cache/{videoid}.png"

    except Exception as e:
        print("THUMB ERROR:", e)
        return YOUTUBE_IMG_URL
