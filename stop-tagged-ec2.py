import boto3

# AWS 서비스 클라이언트 생성
ec2 = boto3.resource('ec2')

def lambda_handler(event, context):
    # 필터를 사용해 'Env' 태그가 'Test'인 인스턴스 찾기
    filters = [{'Name': 'tag:Env', 'Values': ['Test']}]

    # 필터에 일치하는 인스턴스 찾기
    instances = ec2.instances.filter(Filters=filters)

    # 인스턴스 ID 리스트 생성
    InstanceIds = [instance.id for instance in instances]

    # 인스턴스 중지
    stop_responses = ec2.instances.filter(InstanceIds=InstanceIds).stop()

    # 실행 결과 출력
    for instance_id in InstanceIds:
        print(f'Stopped EC2 instance: {instance_id}')

    # 중지된 인스턴스 ID와 함께 응답 반환
    return {
        'StoppedInstances': InstanceIds,
        'Responses': stop_responses
    }
