from aws_cdk import core
from data_platform.data_lake.stack import DataLakeStack
from data_platform.rds.RDS_instance import RDS_instance


app = core.App()

data_lake = DataLakeStack(app)
rds_instance = RDS_instance(app)


app.synth()
