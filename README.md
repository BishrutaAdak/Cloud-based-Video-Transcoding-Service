# Cloud-Based Video Transcoding Service

This project provides a cloud-based service to convert video files into different formats using AWS resources. It ensures scalability, efficiency, and easy integration with other applications.

## Features
- ✅ Convert videos to multiple formats (MP4, AVI, MKV, etc.).
- ✅ Store and retrieve files using Amazon S3.
- ✅ Use AWS Lambda and MediaConvert for processing.
- ✅ Get notifications when transcoding is complete.

## How It Works
1. Upload a video to an S3 bucket.
2. AWS Lambda triggers a MediaConvert job.
3. The video is transcoded into the desired format.
4. The converted file is stored in another S3 bucket.
5. You get notified when the process is done.

## Setup Instructions
### Prerequisites
- AWS account
- AWS CLI installed
- Node.js or Python (optional)

### Deployment Steps
1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/cloud-video-transcoding.git
   cd cloud-video-transcoding
   ```
2. Set up AWS resources (S3, IAM roles, MediaConvert).
3. Deploy the Lambda function:
   ```sh
   cd lambda/
   zip -r function.zip .
   aws lambda create-function --function-name VideoTranscoder --runtime python3.8 --role <your-iam-role> --handler handler.lambda_handler --zip-file fileb://function.zip
   ```
4. Upload a test video and check the results.



