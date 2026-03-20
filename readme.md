# 🤖 AI LinkedIn AutoPoster

An automated LinkedIn posting system that generates unique motivational content and posts it automatically — 96 times a day, completely free.

## ✨ What It Does

- Generates a unique motivational topic using **Groq LLaMA**
- Writes a professional LinkedIn caption with hashtags
- Fetches a beautiful relevant image from **Pexels**
- Overlays the topic text on the image
- Posts automatically to **LinkedIn** — no human intervention

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core language |
| Groq API (LLaMA 3.3) | Topic + caption generation |
| Pexels API | Image fetching |
| Pillow (PIL) | Image processing + text overlay |
| LinkedIn API | Auto posting |
| GitHub Actions | Free cloud scheduler |

## 🏗️ Architecture

```
GitHub Actions (every 15 min)
        ↓
main.py — orchestrator
        ↓
Groq → unique motivational topic
        ↓
Groq → LinkedIn caption + hashtags
        ↓
Groq → Pexels search query
        ↓
Pexels → fetch beautiful image
        ↓
PIL → overlay text on image
        ↓
LinkedIn API → post image + caption
        ↓
Logger → record success/failure
```

## 📁 Project Structure

```
linkedin-autoposter/
├── .github/
│   └── workflows/
│       └── post.yml          # GitHub Actions scheduler
├── generate.py               # AI content + image generation
├── post.py                   # LinkedIn API posting
├── main.py                   # Orchestrator + logger
├── get_token.py              # LinkedIn OAuth token setup
├── ArchivoBlack-Regular.ttf  # Font for image text
├── requirements.txt          # Python dependencies
└── .gitignore                # Hides .env and token.txt
```

## ⚙️ Setup

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/linkedin-autoposter.git
cd linkedin-autoposter
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Get API Keys
- **Groq API** → [console.groq.com](https://console.groq.com) (free)
- **Pexels API** → [pexels.com/api](https://www.pexels.com/api) (free)
- **LinkedIn API** → [linkedin.com/developers](https://www.linkedin.com/developers)

### 4. Setup `.env`
```
GROQ_API_KEY=your_groq_key
PEXELS_API_KEY=your_pexels_key
```

### 5. Get LinkedIn Access Token
```bash
python get_token.py
# Open localhost:8000 → Login with LinkedIn → token.txt auto-saved
```

### 6. Test locally
```bash
python main.py
```

### 7. Deploy on GitHub Actions
Add these GitHub Secrets:
- `GROQ_API_KEY`
- `PEXELS_API_KEY`
- `LINKEDIN_ACCESS_TOKEN`

Push to main → GitHub Actions runs every 15 minutes automatically!

## 📊 Free Tier Limits

| Service | Daily Limit | Our Usage |
|---------|------------|-----------|
| Groq API | 14,400 req/day | ~288/day ✅ |
| Pexels API | 4,800 req/day | ~96/day ✅ |
| LinkedIn API | 125 posts/day | 96/day ✅ |
| GitHub Actions | 2,000 min/month | ~864 min/month ✅ |

**Total cost: $0/month** 🎉

## 🚀 Deployment

This project runs entirely on **GitHub Actions** — no server needed.

```yaml
on:
  schedule:
    - cron: '*/15 * * * *'  # Every 15 minutes
```

Every run:
1. Spins up a fresh Ubuntu machine
2. Installs Python + dependencies
3. Runs `main.py`
4. Posts to LinkedIn
5. Machine shuts down

