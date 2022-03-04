from aws_cdk import core
from data_platform.data_lake.stack import DataLakeStack
from data_platform.rds.RDS_instance import RDS_instance
from data_platform.dms.stack import DmsStack
from data_platform.kinesis.stack import KinesisStack
from data_platform.glue_catalog.stack import GlueCatalogStack
from data_platform.athena.stack import AthenaStack


app = core.App()

data_lake = DataLakeStack(app)
rds_instance = RDS_instance(app)
# dms = DmsStack(
#     app, common_stack=rds_instance, data_lake_raw_bucket=data_lake.data_lake_raw_bucket
# )
kinesis = KinesisStack(app, data_lake_raw_bucket=data_lake.data_lake_raw_bucket)
glue_catalog = GlueCatalogStack(
    app,
    raw_data_lake_bucket=data_lake.data_lake_raw_bucket,
    processed_data_lake_bucket=data_lake.data_lake_processed_bucket,
)
athena = AthenaStack(app)

app.synth()
