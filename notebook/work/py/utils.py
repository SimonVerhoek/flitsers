import pandas as pd


def one_hot_encode(df: pd.DataFrame, column: str) -> pd.DataFrame:
    one_hot = pd.get_dummies(df[column], prefix=column)
    df = df.drop(column, axis=1)
    df = df.join(one_hot)
    return df
