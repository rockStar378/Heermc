import math
from pyrogram.types import InlineKeyboardButton
from SHREE.utils.formatters import time_to_seconds

# ================= TRACK =================
def track_markup(_, videoid, user_id, channel, fplay):
    return [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}",
            )
        ],
    ]


# ================= TIMER =================
def stream_markup_timer(_, chat_id, played, dur):
    try:
        played_sec = time_to_seconds(played)
        duration_sec = time_to_seconds(dur)
        percentage = (played_sec / duration_sec) * 100
    except:
        percentage = 0

    bars = int(percentage // 10)
    bar = "—" * bars + "◉" + "—" * (10 - bars)

    return [
        [
            InlineKeyboardButton(
                text=f"{played} {bar} {dur}",
                callback_data="GetTimer",
            )
        ],
        [
            InlineKeyboardButton(
                text="𝐎ᴡɴᴇʀ ✨",
                url="https://t.me/ITZZ_ISTKHAR"
            ),
            InlineKeyboardButton(
                text="𝐆ʀᴏᴜᴘ 💬",
                url="https://t.me/ITZZ_ISTKHAR"
            ),
        ],
        [
            InlineKeyboardButton(
                text="𝐒ᴜᴘᴘᴏʀᴛ 🛠",
                url="https://t.me/ITZZ_ISTKHAR"
            )
        ],
        [
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close")
        ],
    ]


# ================= PLAYER =================
def stream_markup(_, chat_id):
    return [
        [
            InlineKeyboardButton("▷", callback_data=f"ADMIN Resume|{chat_id}"),
            InlineKeyboardButton("II", callback_data=f"ADMIN Pause|{chat_id}"),
            InlineKeyboardButton("↻", callback_data=f"ADMIN Replay|{chat_id}"),
            InlineKeyboardButton("‣‣I", callback_data=f"ADMIN Skip|{chat_id}"),
            InlineKeyboardButton("▢", callback_data=f"ADMIN Stop|{chat_id}"),
        ],
        [
            InlineKeyboardButton(
                text="𝐎ᴡɴᴇʀ ✨",
                url="https://t.me/ITZZ_ISTKHAR"
            ),
            InlineKeyboardButton(
                text="𝐆ʀᴏᴜᴘ 💬",
                url="https://t.me/ITZZ_ISTKHAR"
            ),
        ],
        [
            InlineKeyboardButton(
                text="𝐒ᴜᴘᴘᴏʀᴛ 🛠",
                url="https://t.me/ITZZ_ISTKHAR"
            )
        ],
        [
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close")
        ],
    ]


# ================= PLAYLIST =================
def playlist_markup(_, videoid, user_id, ptype, channel, fplay):
    return [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"AnonyPlaylists {videoid}|{user_id}|{ptype}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"AnonyPlaylists {videoid}|{user_id}|{ptype}|v|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}",
            ),
        ],
    ]


# ================= LIVE =================
def livestream_markup(_, videoid, user_id, mode, channel, fplay):
    return [
        [
            InlineKeyboardButton(
                text=_["P_B_3"],
                callback_data=f"LiveStream {videoid}|{user_id}|{mode}|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}",
            ),
        ],
    ]


# ================= SLIDER =================
def slider_markup(_, videoid, user_id, query, query_type, channel, fplay):
    query = f"{query[:20]}"
    return [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="◁",
                callback_data=f"slider B|{query_type}|{query}|{user_id}|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {query}|{user_id}",
            ),
            InlineKeyboardButton(
                text="▷",
                callback_data=f"slider F|{query_type}|{query}|{user_id}|{channel}|{fplay}",
            ),
        ],
    ]
