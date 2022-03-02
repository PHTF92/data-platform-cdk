import boto3
import json
from fake_web_events import Simulation
from dotenv import dotenv_values

config = dotenv_values(".env")
ACCESS_KEY = config.get("AWS_ACCESS_KEY_ID")
SECRET_KEY = config.get("AWS_SECRET_ACCESS_KEY")

client = boto3.client(
    "firehose", aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY
)


def put_record(event):
    data = json.dumps(event) + "\n"
    response = client.put_record(
        DeliveryStreamName="firehose-develop-raw-delivery-stream",
        Record={"Data": data},
    )
    print(event)
    return response


simulation = Simulation(user_pool_size=100, sessions_per_day=1000)
events = simulation.run(duration_seconds=10000)

for event in events:
    put_record(event)
