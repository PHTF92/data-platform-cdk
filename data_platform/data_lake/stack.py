from data_platform.data_lake.base import BaseDataLakeBucket

from data_platform.layers import DataLakeLayer

from aws_cdk import core
from aws_cdk import (
    aws_s3 as s3,
)

from data_platform import active_environment as ae


class DataLakeStack(core.Stack):
    """[Class to initialize the creation of the s3 buckets of the data lake based on the BaseDataLakeBucket]

    Args:
        scope (core.Construct): The default scope of the cdk application
    """

    def __init__(self, scope: core.Construct, **kwargs) -> None:
        self.deploy_env = ae.active_environment
        super().__init__(scope, id=f"{self.deploy_env.value}-data-lake-stack", **kwargs)

        self.data_lake_raw_bucket = BaseDataLakeBucket(
            self, deploy_env=self.deploy_env, layer=DataLakeLayer.RAW
        )

        self.data_lake_raw_bucket.add_lifecycle_rule(
            transitions=[
                s3.Transition(
                    storage_class=s3.StorageClass.INTELLIGENT_TIERING,
                    transition_after=core.Duration.days(90),
                ),
                s3.Transition(
                    storage_class=s3.StorageClass.GLACIER,
                    transition_after=core.Duration.days(360),
                ),
            ],
            enabled=True,
        )

        # Data Lake Processed
        self.data_lake_processed_bucket = BaseDataLakeBucket(
            self, deploy_env=self.deploy_env, layer=DataLakeLayer.PROCESSED
        )

        # Data Lake Aggregated
        self.data_lake_aggregated_bucket = BaseDataLakeBucket(
            self, deploy_env=self.deploy_env, layer=DataLakeLayer.AGGREGATED
        )
