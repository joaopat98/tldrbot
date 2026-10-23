# TLDRBot

A witty, slightly sarcastic Telegram bot for group chat summarization. Built with Python and an OpenAI-compatible API, TLDRBot helps teams catch up on conversations with personality.

This is [joaopat98/tldrbot](https://github.com/joaopat98/tldrbot), maintained by
[João Patrício](https://github.com/joaopat98), and forked from
[advaitbd/tldrbot](https://github.com/advaitbd/tldrbot).

This fork adds Docker Compose deployment, public amd64/arm64 container images
at `ghcr.io/joaopat98/tldrbot`, automated image publishing, and configurable
OpenAI-compatible providers including OpenWebUI. The original bot and its
existing features come from the upstream project and its contributors.

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

## Getting Started

### Prerequisites
- Docker with the Compose plugin for container deployment, or Python 3.10+ for local installation
- Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
- API key for OpenAI or an OpenAI-compatible provider

### Docker Compose

#### Run the published image

Create a `compose.yaml` with the following service (also available in
`compose.image.yaml`):

```yaml
services:
  bot:
    image: ghcr.io/joaopat98/tldrbot:latest
    restart: unless-stopped
    init: true
    env_file:
      - .env
```

Create a private `.env` beside `compose.yaml`:

```dotenv
BOT_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_provider_api_key
AI_MODEL=your_model_id
# For OpenWebUI or another compatible provider; omit for OpenAI:
# OPENAI_BASE_URL=https://openwebui.example.test/api
```

Replace the placeholders with your settings and enable `OPENAI_BASE_URL` if
using a custom provider. Compose passes the variables from this file into the
container. Optional settings use the bot's defaults when omitted; see
`.env.example` and the configuration table below. Keep `.env` private.

Start the bot:

```bash
docker compose pull
docker compose up -d
docker compose logs -f bot
```

No source checkout or local build is needed. The image supports Linux amd64 and
arm64. Run `docker compose pull && docker compose up -d` to update. If using
`compose.image.yaml` from this repository, add `-f compose.image.yaml` to each
Compose command.

#### Build from source

Clone this repository, then copy the example configuration:

```bash
git clone https://github.com/joaopat98/tldrbot.git
cd tldrbot
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
git clone https://github.com/joaopat98/tldrbot.git
cd tldrbot
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies (and FFmpeg separately for video processing):
```bash
pip install -r requirements.txt
```

4. Set environment variables in your shell. Local Python execution does not
automatically load `.env`; Docker Compose does.
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
| `/start` | Show help | No |
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
| `VIDEO_URL_PATTERNS` | No | TikTok, Instagram Reels, YouTube Shorts and youtu.be patterns | JSON array of regular expressions for video URL detection (local execution) |

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

After changing `.env`, recreate the container with `docker compose up -d`
(add `-f compose.image.yaml` before `up` if using that file). Add `--build`
when you also changed the source in a local build. Leave `OPENAI_BASE_URL`
unset to use OpenAI's default endpoint.

### Image publishing

GitHub Actions tests and publishes the image to GHCR on pushes to `main`,
`v*` version tags, and manual workflow runs. The default branch publishes
`:latest`; each build also gets a `:sha-<short-commit>` tag. Version tags such
as `v1.2.3` publish `:1.2.3` and `:1.2`. Use a version tag or image digest
when you want to pin a deployment.

When first publishing a fork, set the container package visibility to **Public**
in GitHub's package settings so users can pull without authentication. The
workflow authenticates with `GITHUB_TOKEN`; no registry secret is needed.

## Contributing

Report issues and submit pull requests to
[joaopat98/tldrbot](https://github.com/joaopat98/tldrbot). Provider compatibility
reports should include the provider software, model ID, and error details with
credentials and private URLs removed.

## Attribution

TLDRBot originated in [advaitbd/tldrbot](https://github.com/advaitbd/tldrbot).
Credit goes to [advaitbd](https://github.com/advaitbd) and the
[upstream contributors](https://github.com/advaitbd/tldrbot/graphs/contributors)
for the original Telegram bot, summarization and mention-reply features,
video downloads, rate limiting, and plugin structure inherited by this fork.

Docker deployment, GHCR publishing, and configurable API endpoint support are
maintained in this fork. The bot uses
[python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot),
the [OpenAI Python client](https://github.com/openai/openai-python), and
[yt-dlp](https://github.com/yt-dlp/yt-dlp), with FFmpeg for video processing.

## License

Licensed under the [MIT License](LICENSE). Copyright notices credit this
fork's maintainer and the upstream authors and contributors.
