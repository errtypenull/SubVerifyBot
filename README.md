# creative-bot

my bot for my discord [creative](https://discord.com/invite/ejH2F9D99d) server associated with my YouTube channel [creativeles](https://youtube.com/@creativeless0) used to verify if users are subscribed to my channel before granting them a role. It uses Google's OAuth system to authenticate users and check their subscriptions.

## Features
- OAuth-based YouTube subscription verification
- Automatically assigns a role to verified users
- Simple command to start the verification process
- Flask-powered web server for authentication

## Terms & Privacy 
If you're using the bot on my discord [creative](https://discord.com/invite/ejH2F9D99d) server, you agree to the following:  
- [Terms of Service](https://gist.github.com/errtypenull/dfd02f87732749a1802d831a49e448bb)  
- [Privacy Policy](https://gist.github.com/errtypenull/f959f2877a142ddf66df2b5ef9150d47)  

These only apply if you're using **my hosted version** of the bot. If you're self-hosting, you are responsible for your own terms and policies.


## Requirements
Make sure you have Python installed. Then, install the necessary dependencies:

```
pip install -r requirements.txt
```

### Dependencies
- `discord.py` – For interacting with Discord
- `flask` – To handle OAuth authentication
- `requests` – To make HTTP requests
- `google-auth` – For Google authentication
- `google-auth-oauthlib` – OAuth handling for Google
- `google-auth-httplib2` – HTTP client for Google authentication

## Setup
### 1. Create a Discord Bot
1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Create a new application.
3. Navigate to **Bot**, click **Add Bot**, and copy the bot token.
4. Enable **Privileged Gateway Intents** for Member and Presence.

### 2. Set Up Google OAuth
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project and enable the YouTube Data API v3.
3. Set up OAuth consent and create credentials.
4. Get the **Client ID** and **Client Secret**.
5. Add `http://localhost:5000/callback` as a redirect URI.

### 3. Configure Environment Variables
Create a `.env` file or edit `index.py` with the following:

```python
TOKEN = "YOUR_DISCORD_BOT_TOKEN"
GUILD_ID = YOUR_DISCORD_SERVER_ID
VERIFIED_ROLE_ID = YOUR_VERIFIED_ROLE_ID
CLIENT_ID = "YOUR_GOOGLE_CLIENT_ID"
CLIENT_SECRET = "YOUR_GOOGLE_CLIENT_SECRET"
REDIRECT_URI = "http://localhost:5000/callback"
CHANNEL_ID = "YOUR_YOUTUBE_CHANNEL_ID"
```

### 4. Run the Bot
```bash
python index.py
```

The bot will start, and the web server will be available at `http://localhost:5000`.

## Usage
1. Invite the bot to your Discord server.
2. Type `!verify` in a DM with the bot.
3. Click the provided link to log in with Google and verify your subscription.
4. If successful, the bot assigns you the verified role!

## Contributing
Feel free to submit pull requests or issues to improve the bot.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.


