#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#imports GPIO, time, MotionSensor functions, PiCamera functions, PIL and BOTO from AWS
import RPi.GPIO as GPIO
from gpiozero import MotionSensor
import time
from picamera2 import Picamera2, Preview
import boto3
import io
import requests
import json
import uuid

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
#camera.start_preview(Preview.QTGL)

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

#name the bucket
bucket = 'custom-labels-console-us-east-2-267fac5ce3'


#starts the custom model, fully integrated
#Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-custom-labels-developer-guide/blob/master/LICENSE-SAMPLECODE.)
def start_model(project_arn, model_arn, version_name, min_inference_units):

    try:
        # Start the model
        response = client.start_project_version(ProjectVersionArn = model_arn, MinInferenceUnits = min_inference_units)
        # Wait for the model to be in the running state
        project_version_running_waiter = client.get_waiter('project_version_running')
        project_version_running_waiter.wait(ProjectArn = project_arn, VersionNames = [version_name])

        #Get the running status
        describe_response = client.describe_project_versions(ProjectArn=project_arn,
            VersionNames = [version_name])
    except Exception as e:
        print(e)
    


#send photo to webapp
def sendToWebapp(photo):

    #url for webapp
    url = "https://99gixr5c5g.execute-api.us-east-1.amazonaws.com/objects/green_project"

    #define payload to upload to webapp
    payload = json.dumps({
      "image_link": photo
    })
    headers = {
      'Content-Type': 'application/json'
    }

    #send payload to webapp
    requests.request("POST", url, headers=headers, data=payload)

#fuction to stop the model, currently this function is called after 10 images are analyzed
#Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-custom-labels-developer-guide/blob/master/LICENSE-SAMPLECODE.)
def stop_model(model_arn):

    #Stop the model
    try:
        response = client.stop_project_version(ProjectVersionArn=model_arn)
    except Exception as e:  
        print(e)  



#function called from main to detect motion
def detMotion():
    
    #sensor waits for motion
    sensor.wait_for_motion()
    
    #if sensor detects motion take picture
    filename = str(uuid.uuid4())
    camera.capture_file(f'/tmp/{filename}.jpg')
    photo = filename + '.jpg'
    
    #upload the photo to the s3 bucket
    client1.upload_file(f'/tmp/{filename}.jpg', bucket, photo)
    
    #call the get labels function
    sendToWebapp(photo)
    
    #timer to let sensor reset
    time.sleep(10)
        
    #increment count variable
    count += 1
        
    #if more than 30 photos, stop model
    if count == 10:
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

