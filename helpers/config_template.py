import json
import os

DISCORD_URL = "Enter Channel URL Here"

DISCORD_AUTH = {
    "Authorization": "Enter Username Auth Here"}

API_KEY = "Your Schwab API Key"

SECRET = "Your Schawab Secret"

REDIRECT_URI = "Your Local Host"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TOKEN_PATH = os.path.join(BASE_DIR, "Your Token File Name")
