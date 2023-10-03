from typing import Type

import pandas as pd


def one_hot_encode(df: pd.DataFrame, column: str, dtype: Type[bool | int | float] = bool) -> pd.DataFrame:
    one_hot = pd.get_dummies(df[column], prefix=column, dtype=dtype)
    df = df.drop(column, axis=1)
    df = df.join(one_hot)
    return df
