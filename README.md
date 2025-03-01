## Overview of Idea Hub

Idea Hub is an innovative application designed to help users capture, organize, and develop their ideas efficiently. The core functionality revolves around converting spoken ideas into structured outlines and storing them for future reference. The app leverages advanced AI models and AWS services to provide a seamless and scalable experience.

### Key Components and Technologies

#### Speech-to-Text Conversion
- **Whisper**: An advanced speech recognition model used to convert audio recordings of user ideas into text.

#### Outline Generation
- **GPT-4**: A powerful language model used to generate structured outlines from the transcribed text.

#### Frontend and UI
- **Gradio**: A user-friendly interface for users to interact with the application, record their ideas, and view generated outlines.

#### Backend and Cloud Services
- **AWS Lambda**: Serverless compute service to handle backend logic and API requests.
- **Amazon SageMaker**: Service to deploy and host the GPT-4 model for generating outlines.
- **Amazon S3**: Storage service for user-uploaded audio recordings.
- **Amazon DynamoDB**: NoSQL database for storing generated outlines.
- **Amazon SNS**: Notification service to send confirmation messages to users.
- **Amazon API Gateway**: Service to route API requests from the frontend to the backend.
- **Amazon EventBridge**: Event bus service to trigger events based on changes in DynamoDB.
- **Amazon CloudWatch**: Monitoring service to track application performance and logs.

### Detailed Workflow
![aws diagram](idea_hub_aws_diagram.jpeg)
#### User Interaction
- The user interacts with the application hosted on an EC2 instance, using the Gradio interface to record their idea.

#### Audio Recording
- The recorded audio file is uploaded to Amazon S3 for storage.

#### Speech-to-Text Conversion
- The audio file is processed using Whisper to convert the speech into text.

#### Outline Generation
- The transcribed text is sent to the GPT-4 model hosted on Amazon SageMaker via a Lambda function. The model generates a structured outline from the input text.

#### Data Storage
- The generated outline is stored in Amazon DynamoDB for future reference.

#### Notification
- An event is triggered in Amazon EventBridge when a new item is added to DynamoDB. EventBridge routes the event to Amazon SNS, which sends a confirmation notification to the user.

#### Response Handling
- The Lambda function sends the generated outline back to the EC2 instance via API Gateway, and the result is displayed to the user.

### AWS Flow and Components

#### EC2 Instance
- Hosts the main application and Gradio interface.
- Sends API requests to API Gateway.

#### API Gateway
- Routes incoming API requests from the EC2 instance to the appropriate Lambda function.

#### Lambda Function
- Handles backend logic, including calling the SageMaker endpoint, uploading files to S3, storing data in DynamoDB, and sending notifications via SNS.

#### Amazon SageMaker
- Hosts the GPT-4 model and processes input text to generate outlines.

#### Amazon S3
- Stores user-uploaded audio recordings.

#### Amazon DynamoDB
- Stores generated outlines and other related data.

#### Amazon SNS
- Sends confirmation notifications to users when their outlines are successfully stored.

#### Amazon EventBridge
- Triggers events based on changes in DynamoDB and routes them to SNS.

#### Amazon CloudWatch
- Monitors the entire application, including Lambda functions, API Gateway, and other AWS resources. Collects and tracks metrics, sets alarms, and logs data.
