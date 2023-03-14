#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#imports GPIO, time, MotionSensor functions, PiCamera functions, PIL and BOTO from AWS
import RPi.GPIO as gpio
import time
from gpiozero import MotionSensor
from picamera2 import Picamera2, Preview
import boto3
import io
from PIL import Image, ImageDraw, ExifTags, ImageColor, ImageFont

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


#starts the custom model, some small changes made to source code
#Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-custom-labels-developer-guide/blob/master/LICENSE-SAMPLECODE.)
def start_model(project_arn, model_arn, version_name, min_inference_units):

    try:
        # Start the model
        print('Starting model: ' + model_arn)
        response=client.start_project_version(ProjectVersionArn=model_arn, MinInferenceUnits=min_inference_units)
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
    
#this is a test function to display the label and the photo, this function will be greatly changed in final draft
#Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-custom-labels-developer-guide/blob/master/LICENSE-SAMPLECODE.)
def display_image(bucket,photo,response):
    # Load image from S3 bucket
    s3_connection = boto3.resource('s3')

    s3_object = s3_connection.Object(bucket,photo)
    s3_response = s3_object.get()

    stream = io.BytesIO(s3_response['Body'].read())
    image=Image.open(stream)

    # Ready image to draw bounding boxes on it.
    imgWidth, imgHeight = image.size
    draw = ImageDraw.Draw(image)

    # calculate and display bounding boxes for each detected custom label
    print('Detected custom labels for ' + photo)
    for customLabel in response['CustomLabels']:
        print('Label ' + str(customLabel['Name']))
        print('Confidence ' + str(customLabel['Confidence']))
        if 'Geometry' in customLabel:
            box = customLabel['Geometry']['BoundingBox']
            left = imgWidth * box['Left']
            top = imgHeight * box['Top']
            width = imgWidth * box['Width']
            height = imgHeight * box['Height']

            fnt = ImageFont.truetype('/Library/Fonts/Arial.ttf', 50)
            draw.text((left,top), customLabel['Name'], fill='#00d400', font=fnt)

            print('Left: ' + '{0:.0f}'.format(left))
            print('Top: ' + '{0:.0f}'.format(top))
            print('Label Width: ' + "{0:.0f}".format(width))
            print('Label Height: ' + "{0:.0f}".format(height))

            points = (
                (left,top),
                (left + width, top),
                (left + width, top + height),
                (left , top + height),
                (left, top))
            draw.line(points, fill='#00d400', width=5)

    image.show()
    
    label_count=show_custom_labels(model,bucket,photo, min_confidence)
    print("Custom labels detected: " + str(label_count))

#get custom labels, this function will have some changes for final product
#Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-custom-labels-developer-guide/blob/master/LICENSE-SAMPLECODE.)
def show_custom_labels(model,bucket,photo, min_confidence):

    #Call DetectCustomLabels
    response = client.detect_custom_labels(Image={'S3Object': {'Bucket': bucket, 'Name': photo}},
        MinConfidence=min_confidence,
        ProjectVersionArn=model)

    # For object detection use case, uncomment below code to display image.
    # display_image(bucket,photo,response)

    return len(response['CustomLabels'])

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
    #sensor waits for motion
    sensor.wait_for_motion()
    
    #take picture
    camera.capture_file('/tmp/picture.jpg')
    
    #save the picture and label the bucket
    photo = '/tmp/picture.jpg'
    bucket = 's3://custom-labels-console-us-east-2-267fac5ce3/projects/GreenCount/photosToAnalyze/'
    
    #call the display image function
    display_image(bucket,photo,response)
    
    #sleep timer so sensor can reset itself
    time.sleep(5)
    

    
    
#define main
def main():
    
    #start model
    project_arn='arn:aws:rekognition:us-east-2:152196704760:project/GreenCount/1676441484321'
    model_arn='arn:aws:rekognition:us-east-2:152196704760:project/GreenCount/version/GreenCount.2023-02-18T01.47.44/1676702857667'
    min_inference_units=1 
    version_name='GreenCount.2023-02-18T01.47.44'
    start_model(project_arn, model_arn, version_name, min_inference_units)

    #define model and minimum confidence percentage
    model='arn:aws:rekognition:us-east-2:152196704760:project/GreenCount/version/GreenCount.2023-02-18T01.47.44/1676702857667'
    min_confidence=92
    
    #enter infinite loop to wait for motion
    while True:
        detMotion()
        
if __name__ == "__main__":
    main()
