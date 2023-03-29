

import boto3

def detect_labels(photo, bucket):

    client=boto3.client('rekognition')


# bucket name and file name using s3 service
    response = client.detect_labels(Image={'S3Object':{'Bucket':'mytrashdataproject','Name':'trash.jpeg'}},
        MaxLabels=10)

    print('Detected labels for ' + photo) 
    print()   
    for label in response['Labels']:
        print ("Label: " + label['Name'])
        print ("Confidence: " + str(label['Confidence']))
        
        

        print ("Parents:")
        for parent in label['Parents']:
            print ("   " + parent['Name'])
        print ("----------")
        print ()
    return len(response['Labels'])


def main():
    photo=''
    bucket=''
    label_count=detect_labels(photo, bucket)
    print("Labels detected: " + str(label_count))


if __name__ == "__main__":
    main()


