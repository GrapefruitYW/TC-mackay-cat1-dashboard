from typing import List

# Constants
WINDOW_OPTIONS: List[str] = ['Booking window']
DEFAULT_THRESHOLD: int = 30
MAX_THRESHOLD: int = 60

# Utility functions
def get_conversion_metrics(df, window: str, threshold: int) -> dict:
    """Calculate and return conversion metrics."""
    exceed_df = df[df[window] > threshold]
    exceed = exceed_df.shape[0]
    median = round(df[window].median(), 1)
    mean = round(df[window].mean(), 1)
    
    return {
        'exceed': exceed,
        'median': median,
        'mean': mean
    }
