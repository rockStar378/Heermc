import html
from pyrogram import filters
from SHREE import app
from SHREE.utils.thumbnails import get_thumb
from youtubesearchpython.__future__ import VideosSearch

# ===== QUEUE SYSTEM =====
QUEUE = {}

# ===== PLAY COMMAND =====
@app.on_message(filters.command("play", prefixes=["!", "."]) | filters.regex(r"^play"))
async def play_handler(client, message):

    try:
        # ===== QUERY =====
        if len(message.command) > 1:
            query = " ".join(message.command[1:])
        else:
            query = message.text.replace("play", "").strip()

        if not query:
            return await message.reply("❌ Kya play karna hai bata")

        # ===== SEARCH =====
        search = VideosSearch(query, limit=1)
        data = (await search.next())["result"][0]

        title = data.get("title")
        videoid = data.get("id")
        views = data.get("viewCount", {}).get("short", "Unknown")
        duration = data.get("duration", "Unknown")

        # ===== THUMB =====
        thumb = await get_thumb(videoid)

        # ===== QUEUE ADD =====
        chat_id = message.chat.id

        if chat_id not in QUEUE:
            QUEUE[chat_id] = []

        QUEUE[chat_id].append({
            "title": title,
            "id": videoid
        })

        # ===== AUTOPLAY RELATED ADD =====
        related = VideosSearch(title, limit=3)
        rel = (await related.next())["result"]

        for vid in rel:
            if vid["id"] != videoid:
                QUEUE[chat_id].append({
                    "title": vid["title"],
                    "id": vid["id"]
                })
                break

        # ===== CAPTION =====
        caption = f"""
▶️ {title}

👁 {views} | ⏱ {duration}
🤖 @IAMISTKHAR
"""
        caption = html.escape(caption)

        await message.reply_photo(
            photo=thumb,
            caption=caption
        )

    except Exception as e:
        await message.reply(f"❌ Error: {e}")


# ===== AUTOPLAY FUNCTION =====
async def auto_next(client, message):
    chat_id = message.chat.id

    if chat_id not in QUEUE or len(QUEUE[chat_id]) <= 1:
        return

    # remove current
    QUEUE[chat_id].pop(0)

    next_song = QUEUE[chat_id][0]

    thumb = await get_thumb(next_song["id"])

    await message.reply_photo(
        photo=thumb,
        caption=f"▶️ Autoplay\n{next_song['title']}"
    )


# ===== SKIP COMMAND =====
@app.on_message(filters.command("skip", prefixes=["!", "."]))
async def skip_handler(client, message):
    await auto_next(client, message)
