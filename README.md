# TLDRBot

A witty, slightly sarcastic Telegram bot for group chat summarization. Built with Python and an OpenAI-compatible API, TLDRBot helps teams catch up on conversations with personality.

## Features

### Conversation Summarization (`/tldr`)
Summarize the last N messages in a group chat with a snarky commentary.

```
/tldr      → Summarize last 50 messages
/tldr 100  → Summarize last 100 messages
```

### @Mention Replies
Tag the bot and it'll respond with its signature sarcasm.

```
@TLDRBot what's everyone talking about?
```

### Auto Video Downloads
Drop a TikTok, Instagram Reel, or YouTube Shorts link and the bot automatically downloads and shares the video.

### Rate Limiting
Each user gets 10 AI requests per day. The bot will let you know when you're running low (with attitude, of course).

## Personality Examples

**On /tldr:**
> "Summary complete. I'm basically your group's unpaid intern at this point."

**On @mention:**
> "You rang? I was busy judging other chats."

**On rate limit:**
> "Whoa there, chatty! You've used me 10 times today. I need a break."

## Getting Started

### Prerequisites
- Python 3.10+
- Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
- API key for OpenAI or an OpenAI-compatible provider

### Docker Compose

Install Docker with the Compose plugin, then copy the example configuration:

```bash
cp .env.example .env
# PowerShell: Copy-Item .env.example .env
```

Edit `.env` and set `BOT_TOKEN` and `OPENAI_API_KEY`, then start the bot:

```bash
docker compose up -d --build
docker compose logs -f bot
```

The bot uses Telegram polling, so no inbound ports or webhook setup are required.
The image includes FFmpeg for video downloads and runs as a non-root user.
Chat history and daily usage counters are held in memory and reset when the bot
restarts. Set `DATABASE_URL` to a database reachable from the container if you
want optional analytics; Compose does not start a database service.

Stop the bot with `docker compose down`. After updating the source or dependencies,
run `docker compose up -d --build` again to rebuild and restart it.

On Windows with Docker installed inside WSL, enter your distribution first
(for example, `wsl -d Ubuntu`) and run these commands from the repository
directory under `/mnt/c/path/to/tldrbot`. If its Docker
daemon is stopped, start it with `sudo service docker start`. Check that
`docker compose version` works before building.

### Local installation

1. Clone the repository:
```bash
git clone https://github.com/advaitbd/tldrbot.git
cd tldrbot
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set environment variables:
```bash
# Required
export BOT_TOKEN="your_telegram_bot_token"
export OPENAI_API_KEY="your_openai_api_key"

# Optional
export OPENAI_BASE_URL="https://your-provider.example/v1"  # Omit for OpenAI
export AI_MODEL="gpt-4o-mini"      # Default: gpt-4o-mini
export DAILY_LIMIT="10"            # AI uses per user per day
export MAX_MESSAGES="400"          # Max messages to store per chat
export DATABASE_URL="postgresql://..."  # For analytics (optional)
```

5. Run the bot:
```bash
python bot/main.py
```

## Project Structure

```
bot/
├── main.py              # Entry point
├── config.py            # Configuration
├── core/
│   ├── bot.py           # Bot orchestration
│   ├── ai.py            # AI service with personality
│   └── rate_limiter.py  # Per-user rate limiting
├── plugins/
│   ├── help.py          # /help command
│   ├── summarize.py     # /tldr command
│   ├── mention_reply.py # @mention handler
│   └── auto_download.py # Video URL detection
└── storage/
    ├── memory.py        # In-memory message storage
    └── analytics.py     # Optional event logging
```

## Commands

| Command | Description | Rate Limited |
|---------|-------------|--------------|
| `/help` | Show help | No |
| `/tldr [n]` | Summarize last n messages | Yes |
| `@bot` mention | Reply with personality | Yes |
| Auto-download | Detect & download videos | No |

## Configuration

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `BOT_TOKEN` | Yes | - | Telegram bot token |
| `OPENAI_API_KEY` | Yes | - | API key for the selected provider |
| `OPENAI_BASE_URL` | No | OpenAI API | Base URL for an OpenAI-compatible Chat Completions API |
| `AI_MODEL` | No | gpt-4o-mini | Model ID offered by the selected provider |
| `DAILY_LIMIT` | No | 10 | AI uses per user per day |
| `MAX_MESSAGES` | No | 400 | Messages to store per chat |
| `DATABASE_URL` | No | - | PostgreSQL URL for analytics |

### OpenWebUI and other compatible APIs

Both summaries and mention replies use the configured provider. For an
OpenWebUI instance, set these values in `.env`:

```dotenv
OPENAI_BASE_URL=https://openwebui.example.test/api
OPENAI_API_KEY=your_openwebui_api_key
AI_MODEL=your_model_id
```

Replace the example hostname with your server's hostname and `your_model_id`
with an exact ID offered by your instance. Keep your server URL and credentials
in `.env`, which is excluded from Git and Docker builds. OpenWebUI's
[API documentation](https://docs.openwebui.com/reference/api-endpoints/) describes
API key authentication and listing model IDs with `GET /api/models`.
API keys must be enabled in OpenWebUI; generate yours in Settings > Account.

The base URL is the prefix before `/chat/completions`: OpenWebUI uses `/api`,
while many other providers use `/v1`. Do not include `/chat/completions` itself.
The bot sends Chat Completions requests using system/user messages and
`max_tokens`; your provider and model must support these parameters.
For a local server with authentication disabled, use a non-empty placeholder
such as `OPENAI_API_KEY=unused`.

Apply changes with `docker compose up -d --build`. Leave `OPENAI_BASE_URL`
unset to use OpenAI's default endpoint.

## Contributing

Contributions welcome! Feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details.
