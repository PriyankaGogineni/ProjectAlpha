#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#imports GPIO, time, MotionSensor functions, PiCamera functions, PIL and BOTO from AWS
import RPi.GPIO as GPIO
from gpiozero import MotionSensor
import time
import requests
import json
import uuid
from picamera2 import Picamera2, Preview
import boto3
import io
from PIL import Image, ImageDraw, ExifTags, ImageColor, ImageFont

#count variable to hold number or times Rekognition is called
count = 0

#assigns GPIO pin to the motion sensor
sensor = MotionSensor(4)

#assign PiCamera to camera variable
camera = Picamera2()

#config camera for stills and live feed
camera_config = camera.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores")

#call config function
camera.configure(camera_config)

#start live preview
camera.start_preview(Preview.QTGL)

#start camera
camera.start()

#define rekognition client
client = boto3.client('rekognition')

#define s3 client
client1 = boto3.client('s3', region_name='us-east-2')

#variables to start the model
project_arn='arn:aws:rekognition:us-east-2:152196704760:project/GreenCount/1676441484321'
model_arn='arn:aws:rekognition:us-east-2:152196704760:project/GreenCount/version/GreenCount.2023-02-18T01.47.44/1676702857667'
min_inference_units=1 
version_name='GreenCount.2023-02-18T01.47.44'

#define model and minimum confidence percentage
model='arn:aws:rekognition:us-east-2:152196704760:project/GreenCount/version/GreenCount.2023-02-18T01.47.44/1676702857667'
min_confidence=92


#starts the custom model, some small changes made to source code
#Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-custom-labels-developer-guide/blob/master/LICENSE-SAMPLECODE.)
def start_model(project_arn, model_arn, version_name, min_inference_units):

    try:
        # Start the model
        print('Starting model: ' + model_arn)
        response = client.start_project_version(ProjectVersionArn=model_arn, MinInferenceUnits=min_inference_units)
        # Wait for the model to be in the running state
        project_version_running_waiter = client.get_waiter('project_version_running')
        project_version_running_waiter.wait(ProjectArn=project_arn, VersionNames=[version_name])

        #Get the running status
        describe_response=client.describe_project_versions(ProjectArn=project_arn,
            VersionNames=[version_name])
        for model in describe_response['ProjectVersionDescriptions']:
            print("Status: " + model['Status'])
            print("Message: " + model['StatusMessage']) 
    except Exception as e:
        print(e)
        
    print('Done...')
    


#get custom labels, this function will have some changes for final product
#Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-custom-labels-developer-guide/blob/master/LICENSE-SAMPLECODE.)
def show_custom_labels(photo):

    #Call DetectCustomLabels
    url = "https://99gixr5c5g.execute-api.us-east-1.amazonaws.com/objects/green_project"

    payload = json.dumps({
      "image_link": photo
    })
    headers = {
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    # For object detection use case, uncomment below code to display image.
    # display_image(bucket,photo,response)

    return (response['CustomLabels'])

#fuction to stop the model, may call this after a certain number of images are used, will be minor changes, currently not integrated
#Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-custom-labels-developer-guide/blob/master/LICENSE-SAMPLECODE.)
def stop_model(model_arn):

    print('Stopping model:' + model_arn)

    #Stop the model
    try:
        response=client.stop_project_version(ProjectVersionArn=model_arn)
        status=response['Status']
        print ('Status: ' + status)
    except Exception as e:  
        print(e)  

    print('Done...')


#function called from main to detect motion
def detMotion():
    
    #count variable to hold number or times Rekognition is called
    count = 0
    
    #sensor waits for motion
    sensor.wait_for_motion()
    
    
    #if sensor detects motion
    #take picture
    filename = str(uuid.uuid4())
    camera.capture_file(f'/tmp/{filename}.jpg')
    
    photo = filename + '.jpg'
    #upload the photo to the s3 bucket
    client1.upload_file(f'/tmp/{filename}.jpg', 'custom-labels-console-us-east-2-267fac5ce3', photo)
    
    #name the photo and the bucket
    bucket = 'custom-labels-console-us-east-2-267fac5ce3'
    
    #call the display image function
    label = show_custom_labels(model, bucket, photo, min_confidence)
    
    print(label)
    
    #sleep timer so sensor can reset itself
    time.sleep(10)
        
    #increment count variable
    count += 1
        
    if count == 30:
        stop_model(model_arn)
    

    
    
#define main
def main():
    
    #start model
    #start_model(project_arn, model_arn, version_name, min_inference_units)
    
    #enter infinite loop to wait for motion
    while True:
        detMotion()
        
if __name__ == "__main__":
    main()
