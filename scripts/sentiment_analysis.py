"""
Sentiment and Thematic Analysis for Fintech App Reviews
Includes: sentiment classification, TF-IDF keyword extraction, theme grouping
"""

import pandas as pd
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
import logging
import sys

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def analyze_sentiment(text: str) -> tuple:
    """
    Analyze sentiment of review text
    
    Args:
        text: Review text string
    
    Returns:
        Tuple of (sentiment_label, sentiment_score)
    """
    blob = TextBlob(str(text))
    polarity = blob.sentiment.polarity
    
    if polarity > 0.1:
        return ('positive', polarity)
    elif polarity < -0.1:
        return ('negative', polarity)
    else:
        return ('neutral', polarity)

def extract_keywords_by_bank(df: pd.DataFrame, top_n: int = 10) -> dict:
    """
    Extract top keywords for each bank using TF-IDF
    
    Args:
        df: DataFrame with review_text and bank_name columns
        top_n: Number of top keywords to return
    
    Returns:
        Dictionary mapping bank_name to list of top keywords
    """
    vectorizer = TfidfVectorizer(
        max_features=50,
        stop_words='english',
        ngram_range=(1, 2)
    )
    
    keywords_by_bank = {}
    
    for bank in df['bank_name'].unique():
        bank_reviews = df[df['bank_name'] == bank]['review_text'].fillna('')
        
        if len(bank_reviews) > 5:
            tfidf_matrix = vectorizer.fit_transform(bank_reviews)
            feature_names = vectorizer.get_feature_names_out()
            
            # Sum TF-IDF scores across all documents
            scores = tfidf_matrix.sum(axis=0).A1
            scored_words = list(zip(feature_names, scores))
            scored_words.sort(key=lambda x: x[1], reverse=True)
            
            keywords_by_bank[bank] = [word for word, score in scored_words[:top_n]]
            logger.info(f"Extracted {top_n} keywords for {bank}")
    
    return keywords_by_bank

def create_themes_summary(keywords_by_bank: dict) -> pd.DataFrame:
    """
    Create a summary table of themes from keywords
    
    Args:
        keywords_by_bank: Dictionary of keywords per bank
    
    Returns:
        DataFrame with themes summary
    """
    themes_data = []
    for bank, keywords in keywords_by_bank.items():
        # Group keywords into preliminary themes
        themes = {
            'performance': ['fast', 'slow', 'speed', 'loading'],
            'login': ['login', 'password', 'access', 'authentication'],
            'transactions': ['transfer', 'payment', 'money', 'send'],
            'reliability': ['crash', 'error', 'bug', 'fix'],
            'support': ['customer', 'service', 'help', 'support']
        }
        
        bank_themes = {}
        for theme, theme_words in themes.items():
            matched = [kw for kw in keywords if any(word in kw.lower() for word in theme_words)]
            if matched:
                bank_themes[theme] = matched
        
        themes_data.append({
            'bank_name': bank,
            'top_keywords': ', '.join(keywords[:5]),
            'identified_themes': ', '.join(bank_themes.keys()),
            'sample_keywords_by_theme': str(bank_themes)
        })
    
    return pd.DataFrame(themes_data)

def main():
    """Main execution function"""
    # Load data
    try:
        df = pd.read_csv('data/raw_reviews.csv')
        logger.info(f"Loaded {len(df)} reviews")
    except FileNotFoundError:
        logger.error("No data file found. Please run scrape_reviews.py first.")
        sys.exit(1)
    
    # Apply sentiment analysis
    logger.info("Applying sentiment analysis...")
    sentiment_results = df['review_text'].apply(analyze_sentiment)
    df['sentiment_label'] = sentiment_results.apply(lambda x: x[0])
    df['sentiment_score'] = sentiment_results.apply(lambda x: x[1])
    
    # Extract keywords by bank
    logger.info("Extracting keywords using TF-IDF...")
    keywords_by_bank = extract_keywords_by_bank(df)
    
    # Create themes summary
    themes_df = create_themes_summary(keywords_by_bank)
    
    # Print summary
    print("\n" + "="*60)
    print("SENTIMENT SUMMARY BY BANK")
    print("="*60)
    summary = df.groupby('bank_name')['sentiment_label'].value_counts().unstack().fillna(0)
    print(summary)
    
    print("\n" + "="*60)
    print("TOP KEYWORDS BY BANK")
    print("="*60)
    for bank, keywords in keywords_by_bank.items():
        print(f"\n{bank}:")
        print(f"  Keywords: {', '.join(keywords[:5])}")
    
    print("\n" + "="*60)
    print("THEMES SUMMARY")
    print("="*60)
    print(themes_df.to_string(index=False))
    
    # Save results
    df.to_csv('data/reviews_with_sentiment.csv', index=False)
    themes_df.to_csv('data/themes_summary.csv', index=False)
    logger.info("Results saved to data/")

if __name__ == "__main__":
    main()