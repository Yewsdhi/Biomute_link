# Copyright (C) @FZ_CREATOR 
# Channel: https://t.me/BOT_X_SUPPORT 

import re

API_ID = "9049688"  # Your Telegram API ID
API_HASH = "7ac337fa15e58248eaaa8d59a762ad8e"  # Your Telegram API Hash
BOT_TOKEN = "8214716624:AAEPtxKLSVpBM5VDpBwcCxEH64wmavPYo5c"  # Your Bot Token

# <<< YEH ZAROORI HAI >>>
# -----------------------------------------------------------------
# Apni Telegram User ID yahan daalen.
# Aap @userinfobot se apni ID prapt kar sakte hain.
OWNER_ID = 8175624341  # <<-- YAHAN APNI USER ID DALEN
# -----------------------------------------------------------------

# MongoDB connection URI
MONGO_URI = "mongodb+srv://creatorxbot_db_user:mj54YwFxxlRQOgCZ@cluster0.bknm5sf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

DEFAULT_WARNING_LIMIT = 3
DEFAULT_PUNISHMENT = "mute"  # Options: "mute", "ban"
DEFAULT_CONFIG = ("warn", DEFAULT_WARNING_LIMIT, DEFAULT_PUNISHMENT)

# Regex pattern to detect URLs or mentions in user bios
# YEH PEHLE SE HI URLs AUR @USERNAMES DONO KO DETECT KARTA HAI
URL_PATTERN = re.compile(
    r'(https?://|www\.)[a-zA-Z0-9.\-]+(\.[a-zA-Z]{2,})+(/[a-zA-Z0-9._%+-]*)*|@[a-zA-Z0-9_]+'
)
