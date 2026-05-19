import unittest
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.preprocess import drop_duplicate_reviews, remove_missing_values, normalize_dates

class TestPreprocess(unittest.TestCase):
    
    def setUp(self):
        """Create sample data for testing"""
        self.sample_df = pd.DataFrame({
            'review_id': ['1', '2', '2', '3'],
            'review_text': ['Great app!', 'Good', None, 'Awesome'],
            'rating': [5, 4, 3, None],
            'date': ['2025-05-19', '2025-05-18', '2025-05-17', 'invalid date']
        })
    
    def test_drop_duplicates(self):
        """Test duplicate removal"""
        result = drop_duplicate_reviews(self.sample_df)
        self.assertEqual(len(result), 3)  # Should remove one duplicate (review_id '2')
    
    def test_remove_missing(self):
        """Test missing value removal"""
        result = remove_missing_values(self.sample_df)
        self.assertEqual(len(result), 2)  # Should remove rows with missing review_text or rating
    
    def test_normalize_dates(self):
        """Test date normalization"""
        df = pd.DataFrame({'date': ['2025-01-15', '2025-01-16']})
        result = normalize_dates(df)
        self.assertEqual(result['date'].iloc[0], '2025-01-15')

if __name__ == '__main__':
    unittest.main()