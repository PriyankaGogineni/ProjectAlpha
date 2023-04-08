import json
import boto3
from datetime import datetime, timedelta
from decimal import Decimal
from boto3.dynamodb.types import TypeDeserializer
from collections import defaultdict


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('label_log')

def count_items_identified(json_data, time_frame, duration):
    
    # Calculate start and end dates for the given time frame and duration
    if time_frame == 'weeks':
        start_date = datetime.now() - timedelta(weeks=duration)
        end_date = datetime.now()
    elif time_frame == 'days':
        start_date = datetime.now() - timedelta(days=duration)
        end_date = datetime.now()
    else:
        return {'error': 'Invalid time frame specified'}
    
    # Initialize the dictionary to store the count of each item identified
    item_count = {'Cardboard': 0, 'Plastic': 0, 'Paper': 0}
    
    # Loop through each data point in the JSON data and add to the count if it falls within the time frame
    for data in json_data:
        date = datetime.fromisoformat(data['created_at'][:19])
        if start_date <= date <= end_date:
            for item, count in data['items_identified'].items():
                if item in item_count:
                    item_count[item] += int(count)
    
    # Initialize a list to store the results
    result = []
    
    # If the time frame is weeks, split the count by week and add to the result list
    if time_frame == 'weeks':
        while start_date <= end_date:
            weekly_count = {'date_range': {'start_date': start_date.date().isoformat(), 'end_date': (start_date + timedelta(weeks=1)).date().isoformat()}, 'Cardboard': 0, 'Plastic': 0, 'Paper': 0}
            for data in json_data:
                date = datetime.fromisoformat(data['created_at'][:19])
                if start_date <= date <= start_date + timedelta(weeks=1):
                    for item, count in data['items_identified'].items():
                        if item in item_count:
                            weekly_count[item] += int(count)
            result.append(weekly_count)
            start_date += timedelta(weeks=1)
    
    # If the time frame is days or months, add the count for the entire time frame to the result list
    else:
        while start_date <= end_date:
            daily_count = {'date_range': {'start_date': start_date.date().isoformat(), 'end_date': (start_date + timedelta(days=1)).date().isoformat()}, 'Cardboard': 0, 'Plastic': 0, 'Paper': 0}
            for data in json_data:
                date = datetime.fromisoformat(data['created_at'][:19])
                if date.date() == start_date.date():
                    for item, count in data['items_identified'].items():
                        if item in item_count:
                            daily_count[item] += int(count)
            result.append(daily_count)
            start_date += timedelta(days=1)
    
    return result

def ddb_deserialize(r, type_deserializer = TypeDeserializer()):
    return type_deserializer.deserialize({"M": r})

def lambda_handler(event, context):
    print("Event", event)
    body = json.loads(event['body'])
    print("Body", body)
    end_date = datetime.today()
    # end_date = datetime.now().date()
    if body['time_frame'] == 'days':
        print("daily")
        start_date = end_date - timedelta(days=1)
    elif body['time_frame'] == 'weeks':
        print("Weekly")
        start_date = end_date - timedelta(weeks=1)
    else:
        print("else")
        return {'statusCode': 400, 'body': 'Invalid time period'}
       
    start_date_str = start_date.isoformat()
    end_date_str = end_date.isoformat()
    print(start_date)
    print(end_date)
    # Query DynamoDB to get the items created within the time period
    response = table.scan(
        FilterExpression='created_at BETWEEN :start_date AND :end_date',
        ExpressionAttributeValues={
            ':start_date': start_date_str,
            ':end_date': end_date_str
        },
        ProjectionExpression="items_identified,created_at",
        ConsistentRead=True
    )
    
    # print(response)
    
    items = response.get('Items', [])
    # my_list = list(items)

    return {
        'statusCode': 200,
        'body': json.dumps(count_items_identified(items, body["time_frame"], body["duration"]-1))
    }    
