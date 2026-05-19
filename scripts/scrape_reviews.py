"""
Google Play Reviews Scraper for Ethiopian Fintech Apps
CBE Birr, BOA Mobile Banking, Dashen Bank App
"""

from google_play_scraper import reviews, Sort
import pandas as pd
import time

# Bank app IDs (you need to find the correct package names)
BANKS = {
    "CBE Birr": "com.cbe.birr",
    "BOA Mobile": "com.boa.mobile",
    "Dashen Bank": "com.dashen.bank",
}

def scrape_bank_reviews(bank_name, app_id, count=500):
    """Scrape reviews for a single bank app"""
    print(f"Scraping {bank_name}...")
    try:
        result, continuation_token = reviews(
            app_id,
            lang='en',
            country='et',
            sort=Sort.NEWEST,
            count=count
        )
        return result
    except Exception as e:
        print(f"Error scraping {bank_name}: {e}")
        return []

def main():
    all_reviews = []
    for bank_name, app_id in BANKS.items():
        reviews_data = scrape_bank_reviews(bank_name, app_id, count=500)
        for review in reviews_data:
            all_reviews.append({
                'bank_name': bank_name,
                'review_id': review['reviewId'],
                'user_name': review['userName'],
                'rating': review['score'],
                'review_text': review['content'],
                'date': review['at'].date(),
            })
        time.sleep(2)  # Rate limiting
    
    df = pd.DataFrame(all_reviews)
    print(f"Total reviews scraped: {len(df)}")
    # Note: Do not save CSV to GitHub - it's in .gitignore
    df.to_csv('data/raw_reviews.csv', index=False)
    print("Data saved to data/raw_reviews.csv")

if __name__ == "__main__":
    main()