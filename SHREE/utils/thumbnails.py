import os
import re
import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from youtubesearchpython.__future__ import VideosSearch
from config import YOUTUBE_IMG_URL

CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)

def trim(text):
    return re.sub(r"\s+", " ", text).strip()


async def get_thumb(videoid: str) -> str:
    path = f"{CACHE_DIR}/{videoid}.png"
    if os.path.exists(path):
        return path

    # ===== YT DATA =====
    try:
        search = VideosSearch(f"https://www.youtube.com/watch?v={videoid}", limit=1)
        data = (await search.next())["result"][0]

        title = trim(data.get("title", "Unknown Title"))
        views = data.get("viewCount", {}).get("short", "Unknown Views")
        duration = data.get("duration", "Unknown")
        thumb = data["thumbnails"][0]["url"].split("?")[0]

    except:
        return YOUTUBE_IMG_URL

    # ===== DOWNLOAD THUMB =====
    temp = f"{CACHE_DIR}/temp_{videoid}.png"
    async with aiohttp.ClientSession() as session:
        async with session.get(thumb) as r:
            if r.status == 200:
                async with aiofiles.open(temp, "wb") as f:
                    await f.write(await r.read())
            else:
                return YOUTUBE_IMG_URL

    base = Image.open(temp).convert("RGBA").resize((1280, 720))

    # ===== BLUR BG =====
    bg = base.filter(ImageFilter.GaussianBlur(20))
    bg = ImageEnhance.Brightness(bg).enhance(0.5)

    draw = ImageDraw.Draw(bg)

    # ===== CENTER THUMB =====
    thumb_img = base.resize((900, 450))
    x = (1280 - 900) // 2
    y = 120

    bg.paste(thumb_img, (x, y))

    # ===== GOLDEN FRAME =====
    frame = Image.new("RGBA", (940, 490), (0, 0, 0, 0))
    fdraw = ImageDraw.Draw(frame)

    for i in range(15):
        fdraw.rectangle(
            [i, i, 940 - i, 490 - i],
            outline=(255, 215, 0, 20),
            width=3,
        )

    fdraw.rectangle(
        [10, 10, 930, 480],
        outline=(255, 215, 0, 255),
        width=5,
    )

    bg.paste(frame, (x - 20, y - 20), frame)

    # ===== FONTS =====
    try:
        title_font = ImageFont.truetype("SHREE/assets/font2.ttf", 42)
        info_font = ImageFont.truetype("SHREE/assets/font.ttf", 28)
    except:
        title_font = ImageFont.load_default()
        info_font = ImageFont.load_default()

    # ===== TITLE =====
    title = title[:60]
    w = draw.textlength(title, font=title_font)

    draw.text(
        ((1280 - w) // 2, 600),
        title,
        fill="white",
        font=title_font,
    )

    # ===== INFO =====
    info = f"YouTube : {views} | Time : {duration} | Player : @ITZZ_ISTKHAR"
    w2 = draw.textlength(info, font=info_font)

    draw.text(
        ((1280 - w2) // 2, 650),
        info,
        fill=(255, 255, 0),
        font=info_font,
    )

    # ===== CLEAN =====
    try:
        os.remove(temp)
    except:
        pass

    bg.save(path)
    return path
