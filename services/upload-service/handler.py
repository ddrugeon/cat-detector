import json
import os
from typing import Dict, Any, Optional

import boto3
from botocore.exceptions import ClientError

from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.typing import LambdaContext

S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')
DEFAULT_TTL = os.environ.get('DEFAULT_TTL', 300)

logger = Logger(log_uncaught_exceptions=True)
tracer = Tracer()


@tracer.capture_method()
def generate_presigned_url(bucket: str, image_name: str, region: str, ttl: int)\
        -> Optional[Dict[str, Any]]:

    s3_client = boto3.client('s3',
                             region_name=region,
                             config=boto3.session.Config(signature_version='s3v4',)
                             )
    try:
        return s3_client.generate_presigned_post(
            Bucket=S3_BUCKET_NAME,
            Key=image_name,
            ExpiresIn=ttl
        ) if image_name is not None else None

    except ClientError as e:
        logger.exception("Get a client error when generating pre-signed url", exc_info=e)
        return None

@tracer.capture_lambda_handler
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_HTTP,
                              log_event=True)
def upload(event: dict, context: LambdaContext) -> dict:
    logger.info("Generating pre-signed url")

    payload = event.get("queryStringParameters", {})
    ttl = int(payload.get("ttl", DEFAULT_TTL))
    image_name = payload.get("image_name", None)

    url = generate_presigned_url(bucket=S3_BUCKET_NAME,
                                 image_name=image_name,
                                 region= "eu-west-1",
                                 ttl=ttl)

    if url is not None:
        logger.append_keys(url=url)
        logger.debug("Pre-signed URL successfully generated.")
        return {"statusCode": 200, "body": json.dumps({"upload_url": url})}

    return {"statusCode": 500, "message": "Error when generating pre-signed url"}
