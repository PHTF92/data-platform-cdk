from enum import Enum
from aws_cdk import core
from aws_cdk import (
    aws_s3 as s3,
)

from data_platform.environment import Environment
from data_platform.layers import DataLakeLayer


class BaseDataLakeBucket(s3.Bucket):
    """[Class to template the creation of the s3 buckets of the data lake]

    Inherits: The aws_cdk_s3 bucket creation class

    Args:
        scope (core.Construct): The default scope of the cdk application
        deploy_env (Environment): Enviroment to deploy the bucket
        layer (DataLakeLayer): Layer of the data lake that the bucket belongs to
    """

    def __init__(
        self,
        scope: core.Construct,
        deploy_env: Environment,
        layer: DataLakeLayer,
        **kwargs,
    ):
        self.layer = layer
        self.deploy_env = deploy_env
        self.obj_name = f"s3-phtf-{self.deploy_env.value}-data-lake-{self.layer.value}"

        super().__init__(
            scope,
            id=self.obj_name,
            bucket_name=self.obj_name,
            block_public_access=self.default_block_public_access,
            encryption=self.default_encryption,
            versioned=True,
            **kwargs,
        )

        self.set_default_lifecycle_rules()

    @property
    def default_block_public_access(self):
        return s3.BlockPublicAccess(
            ignore_public_acls=True,
            block_public_acls=True,
            block_public_policy=True,
            restrict_public_buckets=True,
        )

    @property
    def default_encryption(self):
        return s3.BucketEncryption.S3_MANAGED

    def set_default_lifecycle_rules(self):
        """[Sets lifecycle rules to the bucket instance]"""

        """ After 7 days, aborts the upload of multiple files"""
        self.add_lifecycle_rule(
            abort_incomplete_multipart_upload_after=core.Duration.days(7), enabled=True
        )

        """ As the bucket has the versioning system enabled, changes the versions to cheaper storage after 30 and 60 days.
            Those storages classes have lower cost to store the data, but if we request it, the SLA will be bigger and more expensive.
        """
        self.add_lifecycle_rule(
            noncurrent_version_transitions=[
                s3.NoncurrentVersionTransition(
                    storage_class=s3.StorageClass.INFREQUENT_ACCESS,
                    transition_after=core.Duration.days(30),
                ),
                s3.NoncurrentVersionTransition(
                    storage_class=s3.StorageClass.GLACIER,
                    transition_after=core.Duration.days(60),
                ),
            ]
        )

        """Deletes the version after 360 days """
        self.add_lifecycle_rule(noncurrent_version_expiration=core.Duration.days(360))
