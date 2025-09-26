# Exam-plan-checker

This application checks if the exam plan for Software Engineers (Odense) at SDU changes.

## Features

- Downloads and compares exam plan PDFs using SHA256 hashes
- Sends Discord notifications when changes are detected
- Dockerized for easy deployment

## Setup

### Discord Webhook Configuration

To receive Discord notifications when the exam plan changes:

1. Create a Discord webhook in your desired channel:

   - Go to your Discord server
   - Right-click on the channel where you want notifications
   - Select "Edit Channel" → "Integrations" → "Webhooks"
   - Click "New Webhook" and copy the webhook URL

2. Set the webhook URL as an environment variable:

   ```bash
   export DISCORD_WEBHOOK_URL="your_webhook_url_here"
   ```

   Or create a `.env` file:

   ```
   DISCORD_WEBHOOK_URL=your_webhook_url_here
   ```

### Running the Application

```bash
# Install dependencies
pip install -r requirements.txt

# Run the checker
python main.py
```

### Docker

```bash
# Build and run with Docker Compose
docker-compose up --build
```

Make sure to set the `DISCORD_WEBHOOK_URL` environment variable in your Docker environment or docker-compose.yml file.
