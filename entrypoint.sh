#!/bin/sh
set -e

# Cloudflare Tunnel
cloudflared tunnel --no-autoupdate run --token "$TUNNEL_TOKEN" --url http://localhost:8501 &

# Streamlit (reads GEMINI_KEY from env)
streamlit run generateCoverLetter.py --server.address=0.0.0.0

# --- Run Docker ----
# docker run -d --env-file .env -e TUNNEL_TOKEN="token" -p 8501:8501 coverletter-app
