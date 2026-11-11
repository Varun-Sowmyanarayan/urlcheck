import os
import json
from datetime import datetime, timezone

import boto3
from moto import mock_aws

# Fake keys, so Python never looks for your real AWS keys
os.environ["AWS_ACCESS_KEY_ID"] = "fake"
os.environ["AWS_SECRET_ACCESS_KEY"] = "fake"
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

BUCKET = "urlcheck-results"

# Start the fake AWS (it lives only in memory, nothing leaves your Mac)
mock = mock_aws()
mock.start()

s3 = boto3.client("s3", region_name="us-east-1")
s3.create_bucket(Bucket=BUCKET)


def save_result(result):
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S-%f")
    key = "results/" + timestamp + ".json"
    s3.put_object(
        Bucket=BUCKET,
        Key=key,
        Body=json.dumps(result, indent=2),
        ContentType="application/json",
    )
    return key


def list_results(limit=5):
    response = s3.list_objects_v2(Bucket=BUCKET, Prefix="results/")
    keys = [item["Key"] for item in response.get("Contents", [])]
    keys = sorted(keys, reverse=True)[:limit]
    results = []
    for key in keys:
        body = s3.get_object(Bucket=BUCKET, Key=key)["Body"].read()
        results.append(json.loads(body))
    return results
