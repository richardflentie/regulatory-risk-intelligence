""""
Handles ingestion of OCC enforcement data.
"""

import pandas as pd
import requests


def fetch_occ_enforcement_actions(api_url: str) -> pd.DataFrame:
    """
    Fetch enforcement actions from OCC API.
    """
    response = requests.get(api_url)
    response.raise_for_status()
    data = response.json()
    df = pd.DataFrame(data)
    return df


def load_local_csv(path: str) -> pd.DataFrame:
    """
    Load enforcement data from a local CSV file.
    """
    return pd.read_csv(path)
