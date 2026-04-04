from SHREE.core.bot import KAVYA
from SHREE.core.dir import dirr
from SHREE.core.git import git
from SHREE.core.userbot import Userbot
from SHREE.misc import dbb, heroku

from .logging import LOGGER

dirr()
git()
dbb()
heroku()

app = KAVYA()
userbot = Userbot()


from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()
