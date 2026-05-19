# Fintech Customer Experience Analytics

## Project Overview
Sentiment analysis of Google Play reviews for three Ethiopian fintech apps:
- CBE Birr
- BOA Mobile Banking
- Dashen Bank App

## Setup Instructions
1. Clone this repository
2. Create virtual environment: `python -m venv venv`
3. Activate: `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Run scraping: `python scripts/scrape_reviews.py`
6. Run sentiment analysis: `python scripts/sentiment_analysis.py`

## Scraping Methodology
- Used `google-play-scraper` library
- Date range: Last 6 months (Nov 2025 – May 2026)
- 500 reviews per bank, sorted by newest

## Project Structure