"""
Handler for getting a pre-signed URL to allow image uploading on s3
"""
import json
import os
from typing import Any, Dict, Optional

import boto3
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.typing import LambdaContext
from botocore.exceptions import ClientError

# pylint: disable=logging-fstring-interpolation

S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")
DEFAULT_TTL = os.environ.get("DEFAULT_TTL", 300)

logger = Logger(log_uncaught_exceptions=True)
tracer = Tracer()


@tracer.capture_method()
def generate_presigned_url(
    image_name: str, region: str, ttl: int
) -> Optional[Dict[str, Any]]:
    """
    It generates a presigned URL for an image in an S3 bucket

    Parameters
    ----------
    image_name : str
        The name of the image to be uploaded.
    region : str
        The AWS region where the bucket is located.
    ttl : int
        Time to live in seconds.

    """

    s3_client = boto3.client(
        "s3",
        region_name=region,
        config=boto3.session.Config(
            signature_version="s3v4",
        ),
    )
    try:
        return (
            s3_client.generate_presigned_post(
                Bucket=S3_BUCKET_NAME, Key=image_name, ExpiresIn=ttl
            )
            if image_name is not None
            else None
        )

    except ClientError as err:
        logger.exception(
            "Get a client error when generating pre-signed url", exc_info=err
        )
        return None


@tracer.capture_lambda_handler
@logger.inject_lambda_context(
    correlation_id_path=correlation_paths.API_GATEWAY_HTTP, log_event=True
)
# pylint: disable=unused-argument
def upload(event: dict, context: LambdaContext) -> dict:
    """
    It is the handler of the lambda triggered by API Gateway

    Parameters
    ----------
    event : dict
        This is the event that triggered the lambda function. In this case, it's the API
    Gateway.
    context : LambdaContext
        LambdaContext

    """
    logger.info("Generating pre-signed url")

    payload = event.get("queryStringParameters", {})
    ttl = int(payload.get("ttl", DEFAULT_TTL))
    image_name = payload.get("image_name", None)

    url = generate_presigned_url(image_name=image_name, region="eu-west-1", ttl=ttl)

    if url is not None:
        logger.append_keys(url=url)
        logger.debug("Pre-signed URL successfully generated.")
        return {"statusCode": 200, "body": json.dumps({"upload_url": url})}

    return {"statusCode": 500, "message": "Error when generating pre-signed url"}
