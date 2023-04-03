import json
import boto3
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('greencount')
def lambda_handler(event, context):
    
    
    # #aws keys
    # aws_access_key_id="AKIASG35BNH4DMWXXGG6"
    # aws_secret_access_key="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"
    
    #define rekognition client
    client = boto3.client('rekognition', region_name='us-east-2')
    
    #define s3 client
    client1 = boto3.client('s3', region_name='us-east-2')
   

    
    
    
    #variables to start the model
    project_arn='arn:aws:rekognition:us-east-2:152196704760:project/GreenCount/1676441484321'
    model_arn='arn:aws:rekognition:us-east-2:152196704760:project/GreenCount/version/GreenCount.2023-02-18T01.47.44/1676702857667'
    min_inference_units=1 
    version_name='GreenCount.2023-02-18T01.47.44'
    
    #define model and minimum confidence percentage
    model='arn:aws:rekognition:us-east-2:152196704760:project/GreenCount/version/GreenCount.2023-02-18T01.47.44/1676702857667'
    min_confidence=10
    
    bucket = 'custom-labels-console-us-east-2-267fac5ce3'
    photo = 'kk.jpg'
    
    def show_custom_labels(model,bucket,photo, min_confidence):
    
        #Call DetectCustomLabels
        response = client.detect_custom_labels(Image = {'S3Object': {'Bucket': bucket, 'Name': photo}},
            MinConfidence = min_confidence,
            ProjectVersionArn = model)
    
        # For object detection use case, uncomment below code to display image.
        # display_image(bucket,photo,response)
    
        return (response)
        
        
    
    # def main():
        
        #start model
        #start_model(project_arn, model_arn, version_name, min_inference_units)
        
        #enter infinite loop to wait for motion
    
    label = show_custom_labels(model, bucket, photo, min_confidence)
    
   
    custom_labels = label['CustomLabels']
    print(custom_labels)
    # print('mynamr')
            
    # if __name__ == "__main__":
    #     main() 
        
    # table.put_item(Item=custom_labels)
    # dictionary = {item['Name']: item['Confidence'] for item in custom_labels}

    # print(dictionary)
    
    
    
    
    
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps(custom_labels)
    }
