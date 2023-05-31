# Slack Webhook으로 CloudWatch Event를 전송하는 함수 

from datetime import datetime, timedelta, timezone
import os
import urllib3
import json

# KST 시간대 정의 (UTC +9)
KST = timezone(timedelta(hours=9))

# Slack에 메시지를 전송하는 함수
def send_to_slack(webhook_url, msg):
    http = urllib3.PoolManager()
    encoded_msg = json.dumps(msg).encode('utf-8')
    resp = http.request('POST', webhook_url, body=encoded_msg)
    return resp

# Lambda 함수 핸들러
def lambda_handler(event, context):
    # 환경변수'SLACK_WEBHOOK_URL'에서 Slack Webhook URL 추출
    url = os.environ['SLACK_WEBHOOK_URL']     
    username = '[CloudWatch Alarm]' 
    pretext  = f'🔔 [Event] {event["detail-type"]}'
    account = event['account']

    # 이벤트 시간을 KST로 변환하고, 문자열로 변환
    time = datetime.fromisoformat(event['time'].replace('Z', '+00:00')).astimezone(KST)
    formatted_time = time.strftime('%Y-%m-%d %H:%M:%S KST')  # 'KST' added
    
    region = event['region']
    detail = event['detail']
 
    # 메시지 텍스트 작성
    senText  =  f'Account : {account}\nTime : {formatted_time}\nRegion : {region}\nDetail : {detail}'  # Changed {time} to {formatted_time}
    msg = {
        "username": username,
        "pretext": pretext,
        "text": senText,
        "icon_emoji": ""
    }

    # Slack에 메시지 전송    
    resp = send_to_slack(url, msg)

    # 응답 상태 및 본문 출력
    print({
        "status_code": resp.status, 
        "response": resp.data.decode('utf-8')
    })

    return {
        'statusCode': resp.status,
        'body': resp.data.decode('utf-8')
    }