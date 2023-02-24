#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#imports GPIO, time, MotionSensor functions, PiCamera functions and BOTO from AWS
import RPi.GPIO as gpio
import time
from gpiozero import MotionSensor
from picamera import PiCamera
import boto3

#assigns GPIO pin to the motion sensor
sensor = MotionSensor(4)

#assign PiCamera to camera variable
camera = PiCamera()


#function called from main to detect motion
def detMotion():
    #sensor waits for motion
    sensor.wait_for_motion()
    
    #take picture
    camera.capture('/tmp/picture.jpg')
    
    photo = '/tmp/picture.jpg'
    bucket = 's3://custom-labels-console-us-east-2-267fac5ce3/projects/GreenCount/photosToAnalyze/'
    
    #sleep timer so sensor can reset itself
    time.sleep(5)
    
def detect_labels(photo, bucket):

     session = boto3.Session(profile_name='profile-name')
     client = session.client('rekognition')

     response = client.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':photo}},
     MaxLabels=10,
     # Uncomment to use image properties and filtration settings
     #Features=["GENERAL_LABELS", "IMAGE_PROPERTIES"],
     #Settings={"GeneralLabels": {"LabelInclusionFilters":["Cat"]},
     # "ImageProperties": {"MaxDominantColors":10}}
     )

     print('Detected labels for ' + photo)
     print()
     for label in response['Labels']:
         print("Label: " + label['Name'])
         print("Confidence: " + str(label['Confidence']))
         print("Instances:")

         for instance in label['Instances']:
             print(" Bounding box")
             print(" Top: " + str(instance['BoundingBox']['Top']))
             print(" Left: " + str(instance['BoundingBox']['Left']))
             print(" Width: " + str(instance['BoundingBox']['Width']))
             print(" Height: " + str(instance['BoundingBox']['Height']))
             print(" Confidence: " + str(instance['Confidence']))
             print()

         print("Parents:")
         for parent in label['Parents']:
            print(" " + parent['Name'])

         print("Aliases:")
         for alias in label['Aliases']:
             print(" " + alias['Name'])
             
             print("Categories:")
         for category in label['Categories']:
             print(" " + category['Name'])
             print("----------")
             print()

     if "ImageProperties" in str(response):
         print("Background:")
         print(response["ImageProperties"]["Background"])
         print()
         print("Foreground:")
         print(response["ImageProperties"]["Foreground"])
         print()
         print("Quality:")
         print(response["ImageProperties"]["Quality"])
         print()

     return len(response['Labels'])
    

#enter endless loop to call detMotion function
while True:
    detMotion()
