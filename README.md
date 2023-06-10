# Classroom-Attendance-Tracker

## openstack setup
- Create an ubuntu instance inside the virtual box or EC2 instance.
https://releases.ubuntu.com/jammy/ubuntu-22.04.2-desktop-amd64.iso (Ubuntu 22.04 LTS) image
- git clone the openstack repository available at
https://git.openstack.org/openstack-dev/devstack
- Update the local.conf file inside the samples directory, specifically
Host IP : <ip address of the ubuntu instance>
Various Passwords : admin
After that run the ./stack.sh command to install openstack.
- Add the hybridPoll.py file to the ubuntu instance on openstack 
  
 ## Face recognition
  - The face recognition code is written inside handler.py file and it needs a video file in mp4 format.
  - upload the handler .py file as a lambda function
  - update the details for dynamo db table as per your account
  - update the details for dynamo db table as per your account
 
## SQS queus 
  - create 2 queues 
  1. Storing the requests from s3 bucket which will be polled by the openstack instance
  2. Storing the response from openstack that will trigger the lambda function
  
## S3 buckets
  - Setup input and output buckets which will store the requests and response
  - Update the names of these buckets in lambda function
  
 ## Workload.py
  - Code can be tested using workload.py file which uploads an object to input s3 bucket
  - results can be obtained in the output s3 bucket
