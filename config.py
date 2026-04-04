import re
from os import getenv
from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

# ================= BASIC =================
API_ID = int(getenv("API_ID", "0"))
API_HASH = getenv("API_HASH", "")
BOT_TOKEN = getenv("BOT_TOKEN", "")

# ================= DATABASE =================
MONGO_DB_URI = getenv("MONGO_DB_URI", "")

# ================= OWNER / LOGGER =================
OWNER_ID = int(getenv("OWNER_ID", "6006232114"))

# 🔥 FIXED (no crash)
LOGGER_ID = int(getenv("LOGGER_ID", "0"))

# ⚠️ IMPORTANT: numeric ID hona chahiye (-100xxxx)
CHAT_GROUP = int(getenv("CHAT_GROUP", "0"))

OWNER_USERNAME = getenv("OWNER_USERNAME", "ITZZ_ISTKHAR")
BOT_USERNAME = getenv("BOT_USERNAME", "ShreMusicBot")

# ================= COMMAND =================
COMMAND_HANDLER = getenv("COMMAND_HANDLER", "! .").split()

# ================= HEROKU =================
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME", "")
HEROKU_API_KEY = getenv("HEROKU_API_KEY", "")

# ================= GIT =================
UPSTREAM_REPO = getenv(
    "UPSTREAM_REPO",
    "https://github.com/TEAM-ISTKHAR/SHREEMUSIC",
)
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "main")
GIT_TOKEN = getenv("GIT_TOKEN", "")

# ================= SUPPORT =================
SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/IAMISTKHAR")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/ITZZ_ISTKHAR")

# ================= LIMITS =================
DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", "54000"))
SONG_DOWNLOAD_DURATION = int(getenv("SONG_DOWNLOAD_DURATION_LIMIT", "54000"))

# ================= AUTO =================
AUTO_LEAVING_ASSISTANT = bool(getenv("AUTO_LEAVING_ASSISTANT", True))
AUTO_SUGGESTION_MODE = getenv("AUTO_SUGGESTION_MODE", "True")
AUTO_SUGGESTION_TIME = int(getenv("AUTO_SUGGESTION_TIME", "500"))

# ================= SPOTIFY =================
SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", None)
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", None)

# ================= API =================
YTPROXY_URL = getenv("YTPROXY_URL", "https://tgapi.xbitcode.com")
YT_API_KEY = getenv("YT_API_KEY", "xbit_zVATHL2zaR9xkUdxIuhx_UeJodl5zkz4")

# ================= LIMIT =================
PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", 25))
CLEANMODE_DELETE_MINS = int(getenv("CLEANMODE_MINS", "5"))

TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", 21474836480))
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", 21474836480))

# ================= STRING =================
STRING1 = getenv("STRING_SESSION", "")
STRING2 = getenv("STRING_SESSION2", None)
STRING3 = getenv("STRING_SESSION3", None)
STRING4 = getenv("STRING_SESSION4", None)
STRING5 = getenv("STRING_SESSION5", None)

# ================= STORAGE =================
BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
confirmer = {}
chatstats = {}
userstats = {}
clean = {}
autoclean = []

# ================= IMAGES =================
START_IMG_URL = getenv("START_IMG_URL", "https://files.catbox.moe/d274gt.jpg")
PING_IMG_URL = getenv("PING_IMG_URL", "https://files.catbox.moe/d274gt.jpg")

PLAYLIST_IMG_URL = "https://files.catbox.moe/k7iykz.jpg"
STATS_IMG_URL = "https://files.catbox.moe/k7iykz.jpg"
TELEGRAM_AUDIO_URL = "https://files.catbox.moe/k7iykz.jpg"
TELEGRAM_VIDEO_URL = "https://files.catbox.moe/k7iykz.jpg"
STREAM_IMG_URL = "https://files.catbox.moe/k7iykz.jpg"
SOUNCLOUD_IMG_URL = "https://files.catbox.moe/k7iykz.jpg"
YOUTUBE_IMG_URL = "https://files.catbox.moe/k7iykz.jpg"
SPOTIFY_ARTIST_IMG_URL = "https://files.catbox.moe/k7iykz.jpg"
SPOTIFY_ALBUM_IMG_URL = "https://files.catbox.moe/k7iykz.jpg"
SPOTIFY_PLAYLIST_IMG_URL = "https://files.catbox.moe/k7iykz.jpg"

# ================= TIME =================
def time_to_seconds(time):
    return sum(int(x) * 60**i for i, x in enumerate(reversed(str(time).split(":"))))

DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))
SONG_DOWNLOAD_DURATION_LIMIT = int(time_to_seconds(f"{SONG_DOWNLOAD_DURATION}:00"))

# ================= VALIDATION =================
if SUPPORT_CHANNEL and not re.match("(?:http|https)://", SUPPORT_CHANNEL):
    raise SystemExit("❌ SUPPORT_CHANNEL must start with https://")

if SUPPORT_CHAT and not re.match("(?:http|https)://", SUPPORT_CHAT):
    raise SystemExit("❌ SUPPORT_CHAT must start with https://")
