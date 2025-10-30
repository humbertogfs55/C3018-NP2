import pandas as pd
import numpy as np


def remove_highly_correlated_features(df: pd.DataFrame, threshold: float = 0.8):
    """
    Remove highly correlated columns from a DataFrame.
    Keep only one feature from each correlated pair.
    """

    numeric_df = df.select_dtypes(include="number")
    corr_matrix = numeric_df.corr().abs()
    upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
    
    to_drop = [col for col in upper.columns if any(upper[col] > threshold)]
    df_clean = df.drop(columns=to_drop)
    return df_clean, to_drop

