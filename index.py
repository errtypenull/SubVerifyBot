import discord
from discord.ext import commands
from flask import Flask, request
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

# YouTube OAuth URL for authentication, now including state to track user
AUTH_URL = (
    f"https://accounts.google.com/o/oauth2/auth?"
    f"client_id={YOUTUBE_CLIENT_ID}&redirect_uri={REDIRECT_URI}"
    f"&scope=https://www.googleapis.com/auth/youtube.readonly"
    f"&response_type=code&state="
)

# Bot Setup
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# Flask Web Server for OAuth
app = Flask(__name__)
app.secret_key = "your_secret_key"  # Change this to a random secure key

@app.route("/")
def home():
    return "YouTube Verification Bot is Running!"

# Discord Command to Get Verification Link with User ID Tracking
@bot.command()
async def verify(ctx):
    discord_id = str(ctx.author.id)  # Get the Discord user's ID
    user_auth_url = AUTH_URL + discord_id  # Append user ID as state
    await ctx.author.send(f"Click here to verify your subscription: {user_auth_url}")
    await ctx.send("Check your DMs for the verification link!")

# Callback Route for OAuth
@app.route("/callback")
def callback():
    code = request.args.get("code")  # Get the authorization code
    discord_id = request.args.get("state")  # Get the Discord ID from state

    if not code or not discord_id:
        return "Authorization failed. Missing code or state."

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

    # Get YouTube subscriptions of the user
    youtube_url = "https://www.googleapis.com/youtube/v3/subscriptions"
    params = {"part": "snippet", "mine": "true", "maxResults": 50}
    headers = {"Authorization": f"Bearer {access_token}"}
    sub_response = requests.get(youtube_url, headers=headers, params=params).json()

    # Check if the user is subscribed to the channel
    for item in sub_response.get("items", []):
        if item["snippet"]["resourceId"]["channelId"] == YOUTUBE_CHANNEL_ID:
            bot.loop.create_task(assign_role(discord_id))  # Assign role asynchronously
            return "Subscription verified! You have been granted access."

    return "You are not subscribed to the channel. Please subscribe and try again."

# Function to Assign Role in Discord
async def assign_role(discord_id):
    guild = bot.get_guild(DISCORD_GUILD_ID)
    if guild:
        member = guild.get_member(int(discord_id))
        if member:
            role = guild.get_role(VERIFIED_ROLE_ID)
            if role:
                await member.add_roles(role)
                print(f"✅ Assigned role to {member.name}")

# Start Bot and Web Server
if __name__ == "__main__":
    import threading
    threading.Thread(target=app.run, kwargs={"port": 5000}).start()
    bot.run(DISCORD_BOT_TOKEN)
