import dataclasses
import json
import os
import uuid
from dataclasses import dataclass, fields
from typing import List
from urllib.parse import unquote_plus

import boto3
from aws_lambda_powertools.utilities.data_classes import S3Event, event_source
from botocore.exceptions import ClientError

from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.typing import LambdaContext

S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')
DYNAMODB_TABLE_NAME = os.environ.get('DYNAMODB_TABLE_NAME')

logger = Logger(log_uncaught_exceptions=True)
tracer = Tracer()

region_name = os.environ['AWS_REGION']
rekognitionClient = boto3.client('rekognition', region_name=region_name)
dynamodb = boto3.resource('dynamodb', region_name=region_name)
table = dynamodb.Table(DYNAMODB_TABLE_NAME)

@tracer.capture_method()
def process_image(bucket_name: str, object_key: str) -> List[str]:
    logger.info(f'Processing {bucket_name}/{object_key} file')

    image = {'S3Object': {'Bucket': bucket_name, 'Name': object_key}}
    response = rekognitionClient.detect_labels(Image=image, MaxLabels=5)
    logger.debug(f'Parsing from response: {response}')

    labels = [label.get('Name') for label in response['Labels']]

    logger.debug(f'Found these labels from image: {labels}')

    return labels


@tracer.capture_method()
def store_image(bucket_name: str, object_key: str, labels: List[str]) -> dict:
    logger.info('Storing image labels into dynamodb')
    image_id = uuid.uuid1()

    item = {
            'image_id': str(image_id),
            'filename': f'{bucket_name}/{object_key}',
            'labels': labels

    }
    table.put_item(Item=item)

    return item


@tracer.capture_lambda_handler
@logger.inject_lambda_context(correlation_id_path=correlation_paths.S3_OBJECT_LAMBDA,
                              log_event=True)
@event_source(data_class=S3Event)
def process(event: S3Event, context: LambdaContext) -> dict:
    bucket_name = event.bucket_name

    logger.info(f'Receiving new file object to process from {bucket_name}')
    items = []
    for record in event.records:
        object_key = unquote_plus(record.s3.get_object.key)
        labels = process_image(bucket_name, object_key)
        items.append(store_image(bucket_name, object_key, labels))

    return {"statusCode": 200, "body": json.dumps({"items": items})}
