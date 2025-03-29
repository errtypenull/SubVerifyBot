import discord
from discord.ext import commands
from flask import Flask, request, redirect
import requests
import os


# Configuration 

DISCORD_BOT_TOKEN = ""  # Add your Discord bot token here
DISCORD_GUILD_ID = 0  # Replace with your Discord server ID
VERIFIED_ROLE_ID = 0  # Replace with the role ID to assign verified users

YOUTUBE_CLIENT_ID = ""  # Replace with your Google OAuth Client ID
YOUTUBE_CLIENT_SECRET = ""  # Replace with your Google OAuth Client Secret
YOUTUBE_CHANNEL_ID = ""  # Replace with your YouTube Channel ID
REDIRECT_URI = "http://localhost:5000/callback"  # Change if hosted online

# YouTube OAuth URL for authentication
AUTH_URL = f"https://accounts.google.com/o/oauth2/auth?client_id={YOUTUBE_CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=https://www.googleapis.com/auth/youtube.readonly&response_type=code"


# Bot Setup
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


# Flask Web Server for OAuth
app = Flask(__name__)
app.secret_key = "your_secret_key"  # Change this to a random secure key

@app.route("/")
def home():
    return f'<a href="{AUTH_URL}">Login with Google to verify subscription</a>'

@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "Authorization failed."

    # Exchange authorization code for access token
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "client_id": YOUTUBE_CLIENT_ID,
        "client_secret": YOUTUBE_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI
    }
    response = requests.post(token_url, data=data).json()
    access_token = response.get("access_token")

    if not access_token:
        return "Failed to retrieve access token."

    # Get YouTube subscriptions
    youtube_url = "https://www.googleapis.com/youtube/v3/subscriptions"
    params = {"part": "snippet", "mine": "true", "maxResults": 50}
    headers = {"Authorization": f"Bearer {access_token}"}
    sub_response = requests.get(youtube_url, headers=headers, params=params).json()

    # Check if the user is subscribed to the channel
    for item in sub_response.get("items", []):
        if item["snippet"]["resourceId"]["channelId"] == YOUTUBE_CHANNEL_ID:
            return "Subscription verified! Contact the bot in Discord to get your role."

    return "You are not subscribed to the channel."


# Discord Command to Get Verification Link
@bot.command()
async def verify(ctx):
    await ctx.author.send(f"Click here to verify your subscription: {AUTH_URL}")
    await ctx.send("Check your DMs for the verification link!")


# Start Bot and Web Server
if __name__ == "__main__":
    import threading
    threading.Thread(target=app.run, kwargs={"port": 5000}).start()
    bot.run(DISCORD_BOT_TOKEN)
