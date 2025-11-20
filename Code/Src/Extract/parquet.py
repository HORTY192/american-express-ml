import pandas as pd
import numpy as np
import polars as pl

def convertir_parquet(input_data_path):
    
    pl.scan_csv(input_data_path / "raw/train_data.csv").sink_parquet(input_data_path / "parquet/train_data.parquet")
    pl.scan_csv(input_data_path / "raw/test_data.csv").sink_parquet(input_data_path / "parquet/test_data.parquet")