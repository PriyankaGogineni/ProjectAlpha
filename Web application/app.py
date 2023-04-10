import re
from datetime import datetime
from flask import render_template
from flask import Flask
from flask import request, jsonify
import boto3
import requests
import json


app = Flask(__name__)


@app.route("/")
def layout():
     return render_template("basic3.html")

@app.route("/home/")
def home():
     return render_template("home.html")
    
@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/contact/")
def contact():
    return render_template("contact.html")

@app.route('/get-s3-data')
def get_s3_data():
    # Define the S3 bucket name and object key
    bucket = 'custom-labels-console-us-east-2-267fac5ce3'
    object_key = 'my-object-key'

    # Get the S3 object
    s3 = boto3.client('s3', region_name='us-east-2')
    response = s3.get_object(Bucket=bucket, Key=object_key)
    data = response['Body'].read().decode('utf-8')

    # Return the data in JSON format
    return jsonify({'data': data})


if __name__ == '__main__':
    app.run(debug=True)

    