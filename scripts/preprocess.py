def drop_duplicate_reviews(df):
    """Remove duplicate reviews based on review_id"""
    return df.drop_duplicates(subset='review_id')

def remove_missing_values(df):
    """Remove rows with missing values in review_text or rating"""
    return df.dropna(subset=['review_text', 'rating'])

def normalize_dates(df):
    """Normalize date format"""
    df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.strftime('%Y-%m-%d')
    return df