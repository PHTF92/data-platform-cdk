from enum import Enum


class DataLakeLayer(Enum):
    RAW = "raw"
    PROCESSED = "processed"
    AGGREGATED = "aggregated"
