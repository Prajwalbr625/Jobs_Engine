<<<<<<< HEAD
# Jobs_Engine
=======
# IT Jobs Alert Engine 🚀

A fully automated, media-first job board that aggregates IT job postings, deduplicates them, and publishes them to a Static Website (GitHub Pages) and Telegram/social channels.

## Features
- **Multi-Source Fetching**: Python.org, LinkedIn (Public), and extensible for others.
- **Smart Filtering**: Filters by Location (e.g., India only) and Keywords.
- **Static Site Generation**: Builds a fast, SEO-ready HTML website in `docs/` folder.
- **AdSense Ready**: Includes placeholders for ad units.
- **Automation**: GitHub Actions workflow included for hourly updates.

## Setup & Deployment (Free Hosting)

### 1. Local Setup
```bash
# Install dependencies
pip install -r it_jobs_engine/requirements.txt

# Run once to test
python it_jobs_engine/main.py --once

# Preview Site
open docs/index.html
```

### 2. Deploy to GitHub Pages (Free)
1.  Initialize a git repo and push this code to GitHub.
2.  Go to **Settings > Pages**.
3.  Source: **Deploy from a branch**.
4.  Branch: `gh-pages` (This branch will be created automatically by the Action after the first run).
5.  **Done!** Your site will be live at `https://<username>.github.io/<repo-name>/`.

### 3. Monetization (AdSense)
1.  Apply for Google AdSense using your GitHub Pages URL.
2.  Once approved, get your Publisher ID (e.g., `ca-pub-123456`).
3.  Edit `it_jobs_engine/src/processors/static_generator.py` and uncomment the AdScript line in the layout.

## Configuration
Edit `it_jobs_engine/config/settings.py` to change:
- `ALLOWED_LOCATIONS`: Control which cities/countries are accepted.
- `FETCH_INTERVAL`: Schedule frequency.
>>>>>>> d8bdc8e (Initial commit of IT Jobs Engine)
