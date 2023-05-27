import boto3
import json
import threading

sqs = boto3.client("sqs")
s3 = boto3.client("s3")
lambda_client = boto3.client("lambda")

input_queue_url = "https://sqs.us-east-1.amazonaws.com/301393284448/HybridQueue"

output_queue_url = "https://sqs.us-east-1.amazonaws.com/301393284448/HybridOutputBucketQueue"

def input_bucket_monitor():
    while True:
        # Poll the SQS queue for new messages
        messages = sqs.receive_message(QueueUrl=input_queue_url, MaxNumberOfMessages=10, WaitTimeSeconds=20)

        if "Messages" in messages:
            message  = messages["Messages"][0]
            receipt_handle = message['ReceiptHandle']
            event = message["Body"]

            # print(event)

            # print(f"New video detected")

            # Trigger the Lambda function
            lambda_client.invoke(
                FunctionName="paas",
                InvocationType="Event",
                Payload=event
            )

            # Delete the message from the queue
            sqs.delete_message(QueueUrl=input_queue_url, ReceiptHandle=message["ReceiptHandle"])

            # print("Queue cleared")


def output_bucket_monitor():
#    bucket_name = 'paas-output-bucket'
   while True:
        response = sqs.receive_message(QueueUrl=output_queue_url)
        messages = response.get('Messages', [])
        for message in messages:
            # Process message here
            # print('Message received from queue {}: {}'.format(output_queue_url, message['Body']))

            event = json.loads(message['Body'])
        	# Get the bucket name and object key from the event
            bucket_name = event['Records'][0]['s3']['bucket']['name']
            object_key = event['Records'][0]['s3']['object']['key']

            bucket_response = s3.get_object(Bucket=bucket_name, Key=object_key)
            file_contents = bucket_response['Body'].read().decode('utf-8')
            print("\n", file_contents)

            # file_name, name, subject, grade  = file_contents.split(",") 
            # print(f"{file_name} : {name}, {subject}, {grade}")
            sqs.delete_message(QueueUrl=output_queue_url, ReceiptHandle=message['ReceiptHandle'])

# Create threads to monitor each queue
thread1 = threading.Thread(target=input_bucket_monitor)
thread2 = threading.Thread(target=output_bucket_monitor)

thread1.start()
thread2.start()

# Wait for threads to finish
thread1.join()
thread2.join()