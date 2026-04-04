import os
import re
import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from youtubesearchpython.__future__ import VideosSearch
from config import YOUTUBE_IMG_URL

# ================= CONFIG =================
CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)

PANEL_W, PANEL_H = 763, 545
PANEL_X = (1280 - PANEL_W) // 2
PANEL_Y = 88
TRANSPARENCY = 170
INNER_OFFSET = 36

THUMB_W, THUMB_H = 542, 273
THUMB_X = PANEL_X + (PANEL_W - THUMB_W) // 2
THUMB_Y = PANEL_Y + INNER_OFFSET

TITLE_X = 377
META_X = 377
TITLE_Y = THUMB_Y + THUMB_H + 10
META_Y = TITLE_Y + 45

BAR_X, BAR_Y = 388, META_Y + 45
BAR_RED_LEN = 280
BAR_TOTAL_LEN = 480

ICONS_W, ICONS_H = 415, 45
ICONS_X = PANEL_X + (PANEL_W - ICONS_W) // 2
ICONS_Y = BAR_Y + 48

MAX_TITLE_WIDTH = 580


# ================= UTILS =================
def trim_to_width(text, font, max_w):
    ellipsis = "…"
    try:
        if font.getlength(text) <= max_w:
            return text
    except:
        return text[:40]

    for i in range(len(text) - 1, 0, -1):
        try:
            if font.getlength(text[:i] + ellipsis) <= max_w:
                return text[:i] + ellipsis
        except:
            return text[:40]
    return ellipsis


# ================= MAIN =================
async def get_thumb(videoid: str) -> str:
    cache_path = os.path.join(CACHE_DIR, f"{videoid}.png")
    if os.path.exists(cache_path):
        return cache_path

    # ===== Fetch YouTube Data =====
    try:
        results = VideosSearch(f"https://www.youtube.com/watch?v={videoid}", limit=1)
        data = (await results.next())["result"][0]

        title = re.sub(r"\W+", " ", data.get("title", "Unknown")).title()
        thumbnail = data["thumbnails"][0]["url"].split("?")[0]
        duration = data.get("duration")
        views = data.get("viewCount", {}).get("short", "Unknown Views")

    except Exception:
        title, thumbnail, duration, views = "Unsupported Title", YOUTUBE_IMG_URL, None, "Unknown Views"

    is_live = not duration or str(duration).lower() in ["", "live"]
    duration_text = "Live" if is_live else duration or "Unknown"

    # ===== Download Thumbnail =====
    thumb_path = os.path.join(CACHE_DIR, f"thumb{videoid}.png")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                if resp.status == 200:
                    async with aiofiles.open(thumb_path, "wb") as f:
                        await f.write(await resp.read())
    except:
        return YOUTUBE_IMG_URL

    # ===== Base Image =====
    base = Image.open(thumb_path).resize((1280, 720)).convert("RGBA")
    bg = ImageEnhance.Brightness(base.filter(ImageFilter.GaussianBlur(10))).enhance(0.6)

    draw = ImageDraw.Draw(bg)

    # ===== Panel =====
    panel = bg.crop((PANEL_X, PANEL_Y, PANEL_X + PANEL_W, PANEL_Y + PANEL_H))
    overlay = Image.new("RGBA", (PANEL_W, PANEL_H), (255, 255, 255, TRANSPARENCY))
    panel = Image.alpha_composite(panel, overlay)

    mask = Image.new("L", (PANEL_W, PANEL_H), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, PANEL_W, PANEL_H), 50, fill=255)

    bg.paste(panel, (PANEL_X, PANEL_Y), mask)

    # ===== Fonts =====
    try:
        title_font = ImageFont.truetype("SHREE/assets/font2.ttf", 32)
        small_font = ImageFont.truetype("SHREE/assets/font.ttf", 20)
        side_font = ImageFont.truetype("SHREE/assets/font.ttf", 70)
    except:
        title_font = small_font = side_font = ImageFont.load_default()

    # ===== Thumbnail =====
    thumb = base.resize((THUMB_W, THUMB_H))
    mask = Image.new("L", thumb.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, THUMB_W, THUMB_H), 20, fill=255)

    bg.paste(thumb, (THUMB_X, THUMB_Y), mask)

    # ===== Text =====
    draw.text(
        (TITLE_X, TITLE_Y),
        trim_to_width(title, title_font, MAX_TITLE_WIDTH),
        fill="black",
        font=title_font,
    )

    draw.text(
        (META_X, META_Y),
        f"YouTube | {views}",
        fill="black",
        font=small_font,
    )

    # ===== Progress Bar =====
    draw.line([(BAR_X, BAR_Y), (BAR_X + BAR_RED_LEN, BAR_Y)], fill="red", width=6)
    draw.line([(BAR_X + BAR_RED_LEN, BAR_Y), (BAR_X + BAR_TOTAL_LEN, BAR_Y)], fill="gray", width=5)

    draw.text((BAR_X, BAR_Y + 10), "00:00", fill="black", font=small_font)
    draw.text((BAR_X + BAR_TOTAL_LEN - 60, BAR_Y + 10), duration_text, fill="black", font=small_font)

    # ===== 3D SIDE TEXT =====
    text = "SHREE MUSIC"
    x, y = 30, 200

    for i in range(8):
        draw.text((x + i, y + i), text, font=side_font, fill=(0, 0, 0, 180))

    draw.text((x, y), text, font=side_font, fill=(255, 255, 255))

    # ===== Icons =====
    icons_path = "SHREE/assets/play_icons.png"
    if os.path.isfile(icons_path):
        ic = Image.open(icons_path).resize((ICONS_W, ICONS_H)).convert("RGBA")
        bg.paste(ic, (ICONS_X, ICONS_Y), ic)

    # ===== Cleanup =====
    try:
        os.remove(thumb_path)
    except:
        pass

    bg.save(cache_path)
    return cache_path
