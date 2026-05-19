"""
Sentiment Analysis on Fintech App Reviews
Using TextBlob for initial classification
"""

import pandas as pd
from textblob import TextBlob
import sys

def analyze_sentiment(text):
    """Return sentiment label (positive, negative, neutral)"""
    blob = TextBlob(str(text))
    polarity = blob.sentiment.polarity
    
    if polarity > 0.1:
        return 'positive'
    elif polarity < -0.1:
        return 'negative'
    else:
        return 'neutral'

def main():
    # Load data (this would be from your scraped file)
    try:
        df = pd.read_csv('data/raw_reviews.csv')
    except FileNotFoundError:
        print("No data file found. Please run scrape_reviews.py first.")
        sys.exit(1)
    
    # Apply sentiment analysis
    df['sentiment_label'] = df['review_text'].apply(analyze_sentiment)
    
    # Simple sentiment score (mock)
    df['sentiment_score'] = df.apply(
        lambda x: 1 if x['sentiment_label'] == 'positive' 
        else (-1 if x['sentiment_label'] == 'negative' else 0), axis=1
    )
    
    # Summary by bank
    print("\n=== Sentiment Summary by Bank ===")
    summary = df.groupby('bank_name')['sentiment_label'].value_counts().unstack().fillna(0)
    print(summary)
    
    # Save results (do not commit)
    df.to_csv('data/reviews_with_sentiment.csv', index=False)
    print("\nSentiment analysis complete. Results saved to data/reviews_with_sentiment.csv")

if __name__ == "__main__":
    main()