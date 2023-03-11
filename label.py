import boto3
import datetime

def count_analyzed_pictures(start_date, end_date):
    client = boto3.client('rekognition')
    token = None
    count = 0
    
    while True:
        if token:
            response = client.get_label_detection(NextToken=token)
        else:
            response = client.get_label_detection(JobId=job_id)
            
        for label_detection in response['Labels']:
            timestamp = label_detection['Timestamp']
            if start_date <= timestamp <= end_date:
                count += 1
        
        if 'NextToken' in response:
            token = response['NextToken']
        else:
            break
            
    return count
