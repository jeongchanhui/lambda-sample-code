# 하루치의 CloudWatch 로그를 JSON S3에 적재하는 함수 

import boto3
import os
import json
import logging
from datetime import datetime, timedelta

# 로깅을 위한 로거 설정 
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # 환경 변수에서 log group 및 bucket 정보 추출
    log_groups = os.environ['LOG_GROUPS'].split(',')
    s3_bucket_name = os.environ['S3_BUCKET']
    s3_prefixes = os.environ['S3_PREFIX'].split(',')

    # Set up clients for CloudWatch Logs and S3
    logs = boto3.client('logs')
    s3 = boto3.client('s3')

    for i, log_group in enumerate(log_groups):
        # ':'으로 여러개의 로그 그룹 및 스트림 분리 
        log_stream = log_group.split(':')[-1] 
        log_group_name = log_group.split(':')[0]

        current_time = datetime.utcnow()

        start_time = current_time.replace(hour=0, minute=0, second=0, microsecond=0)
        end_time = start_time + timedelta(days=1)

        # CloudWatch 로그 가져오기 
        log_data = logs.get_log_events(
            logGroupName=log_group_name,
            logStreamName=log_stream,
            startTime=int((start_time - datetime(1970, 1, 1)).total_seconds() * 1000),
            endTime=int((end_time - datetime(1970, 1, 1)).total_seconds() * 1000)
        )

        # 로그 데이터 JSON 객체로 변환 
        log_data_json = json.dumps(log_data)

        # S3에 JSON 객체 업로드
        s3.put_object(
            Bucket=s3_bucket_name,
            Key=s3_prefixes[i] + '-' + current_time.strftime('%Y-%m-%d-%H-%M-%S') + '.json',
            Body=log_data_json
        )
        # S3 업로드 작업 로깅 
        logger.info(f"Uploaded logs from {log_group_name}/{log_stream} to {s3_bucket_name}/{s3_prefixes[i]}")
