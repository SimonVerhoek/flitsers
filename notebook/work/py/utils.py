from typing import Type

import dask.dataframe as dd
import pandas as pd

from py.consts import DATA_DIR, HOURS_OF_DAY


def one_hot_encode(df: pd.DataFrame, column: str, drop_first: bool = True, dtype: Type[bool | int | float] = bool) -> pd.DataFrame:
    print(f"One-hot encoding column {column}...")
    return pd.get_dummies(df[column], prefix=column, drop_first=drop_first, dtype=dtype)


def one_hot_encode_all(ddf: dd.DataFrame, columns: list[str], drop_first: bool = True, dtype: Type[bool | int | float] = bool) -> pd.DataFrame:
    ddf = ddf.categorize(columns=columns)

    for column in columns:
        one_hot = dd.reshape.get_dummies(ddf[column], prefix=column, drop_first=drop_first, dtype=dtype)
        ddf = ddf.drop(column, axis=1)

        # dask_one_hot = dd.from_pandas(one_hot, npartitions=2)

        # ddf = dd.merge(ddf, one_hot)
        ddf = dd.concat([ddf, one_hot], axis=1)

    # ddf = dd.concat([ddf, *one_hot_ddfs], axis=1)
    return ddf


def write_partition_to_parquet(partition, partition_index):
    print(f"partition: {partition} {partition_index}")
    
    # Write the partition to Parquet
    partition.to_parquet(DATA_DIR / f'partition_{partition_index}.parquet', engine='pyarrow')
    return partition_index

    # batch_size = 100  # Number of batches
    # for i in range(batch_size):
    #     start_idx = i * (len(partition) // batch_size)
    #     end_idx = (i + 1) * (len(partition) // batch_size)
    #     partition_batch = partition[start_idx:end_idx]
    #     partition_batch.to_parquet(DATA_DIR / f"batch_{i}.parquet", engine="pyarrow", memory_limit=2e9)
    # return partition_index


def get_all_roads(filename: str = "flitsers.parquet"):
    df = pd.read_parquet(f"../data/{filename}")
    return df.wegnummer.unique()


def get_all_start_stop_hour_combinations():
    all_start_stop_hour_combinations = [(start, stop) for start in HOURS_OF_DAY for stop in HOURS_OF_DAY if start < stop]
    return all_start_stop_hour_combinations

    # start_hours, stop_hours = zip(*all_start_stop_hour_combinations)
    # return start_hours, stop_hours
