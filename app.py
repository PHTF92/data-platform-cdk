from aws_cdk import core
from data_platform.data_lake.stack import DataLakeStack
from data_platform.rds.RDS_instance import RDS_instance
from data_platform.dms.stack import DmsStack


app = core.App()

data_lake = DataLakeStack(app)
rds_instance = RDS_instance(app)
dms = DmsStack(
    app, common_stack=rds_instance, data_lake_raw_bucket=data_lake.data_lake_raw_bucket
)

app.synth()
