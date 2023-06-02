import boto3

# AWS 서비스 클라이언트 생성
rds = boto3.client('rds')

def lambda_handler(event, context):
    # 모든 DB 인스턴스의 목록을 가져옴
    db_instances = rds.describe_db_instances()
    
    # 'Env' 태그가 'Test'인 인스턴스를 찾아서 리스트에 추가
    Test_instances = []
    for instance in db_instances['DBInstances']:
        instance_arn = instance['DBInstanceArn']
        tags = rds.list_tags_for_resource(ResourceName=instance_arn)
        for tag in tags['TagList']:
            if tag['Key'] == 'Env' and tag['Value'] == 'Test':
                Test_instances.append(instance['DBInstanceIdentifier'])
    
    # 인스턴스 시작
    start_responses = []
    for instance_id in Test_instances:
        response = rds.start_db_instance(DBInstanceIdentifier=instance_id)
        start_responses.append(response)

        # 실행 결과 출력
        print(f'Started RDS instance: {instance_id}')
    
    # 시작된 인스턴스 ID와 함께 응답 반환
    return {
        'StartedInstances': Test_instances,
        'Responses': start_responses
    }
