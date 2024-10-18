import os

import pandas as pd

_DATASETS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/raw"))

def dataset_ustrafic_accident() -> pd.DataFrame:
    """Load the a countrywide car accident dataset that covers 49 states of the USA. 
    The accident data were collected from February 2016 to March 2023, using multiple APIs 
    that provide streaming traffic incident (or event) data. These APIs broadcast traffic data 
    captured by various entities, including the US and state departments of transportation, 
    law enforcement agencies, traffic cameras, and traffic sensors within the road networks. 
    The dataset currently contains approximately 7.7 million accident records.

    Source of Data: Kaggle
    (https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents)

    Returns 
    --------
    pd.DataFrame
    """
    return pd.read_csv(os.path.join(_DATASETS_DIR, "US_Accidents_March23.csv"))
