#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#imports GPIO, time, MotionSensor functions, PiCamera functions, PIL and BOTO from AWS
import RPi.GPIO as GPIO
from gpiozero import MotionSensor
import time
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

#define model and minimum confidence percentage
model='arn:aws:rekognition:us-east-2:152196704760:project/GreenCount/version/GreenCount.2023-02-18T01.47.44/1676702857667'
min_confidence=92


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
    


#get custom labels, function fully integrated
#Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-custom-labels-developer-guide/blob/master/LICENSE-SAMPLECODE.)
def show_custom_labels(model,bucket,photo, min_confidence):

    #Call DetectCustomLabels
    response = client.detect_custom_labels(Image = {'S3Object': {'Bucket': bucket, 'Name': photo}},
        MinConfidence = min_confidence,
        ProjectVersionArn = model)

    return (response['CustomLabels'])

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
    
    #count variable to hold number or times Rekognition is called
    count = 0
    
    #sensor waits for motion
    sensor.wait_for_motion()
    
    #if sensor detects motion take picture
    camera.capture_file('/tmp/picture.jpg')
    
    #upload the photo to the s3 bucket
    client1.upload_file('/tmp/picture.jpg', 'custom-labels-console-us-east-2-267fac5ce3', 'picture.jpg')
    
    #name the photo and the bucket
    photo = 'picture.jpg'
    bucket = 'custom-labels-console-us-east-2-267fac5ce3'
    
    #call the get labels function
    label = show_custom_labels(model, bucket, photo, min_confidence)
    
    #call analyze label function to get a string back
    response = analyzeLabel(str(label))
    
    #timer to let sensor reset
    time.sleep(10)
    
    #print string for test purposes
    print(response)
        
    #increment count variable
    count += 1
        
    #if more than 30 photos, stop model
    if count == 10:
        stop_model(model_arn)
        
#function to analyze the label
def analyzeLabel(label):

    #analyze label and extract string
    if 'metal' in label:
        response = 'aluminum'
    elif 'cardboard' in label:
        response = 'cardboard'
    elif 'paper' in label:
        response = 'paper'
    elif 'glass' in label:
        response = 'glass'
    elif 'plastic' in label:
        response = 'plastic'
    else:
        response = 'not recyclable'
            
    #return string
    return response

    
    
#define main
def main():
    
    #start model
    #start_model(project_arn, model_arn, version_name, min_inference_units)
    
    #enter infinite loop to wait for motion
    while True:
        detMotion()
        
if __name__ == "__main__":
    main()
