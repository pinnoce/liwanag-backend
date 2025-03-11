# AWS SAM Lambda Deployment Guide

## Prerequisites

Before you start, ensure you have the following installed:

-   [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
-   [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
-   [Visual Studio Code](https://code.visualstudio.com/)
-   Python (compatible version with AWS Lambda runtime)
-   Git (to clone the repository)

## Step 1: Clone the Repository

Clone the existing GitHub repository that contains the AWS SAM project, in this case we are going to clone the *word_api* branch and create a sample function:

```sh
git clone -b word_api https://github.com/pinnoce/liwanag-backend
cd liwanag-backend
```

## Step 2: Configure AWS Credentials

You need to configure your AWS credentials before deploying:

```sh
aws configure
```
Enter the following details:

-   **AWS Access Key ID**
-   **AWS Secret Access Key**
-   **Default region name** (e.g., `us-west-1`)
-   **Default output format** (leave blank or enter `json`)

## Step 3: Create a New Lambda Function

Navigate to the `liwanag-backend` directory and create a new folder for your API function (you can also do this with file explorer in Visual Studio Code instead of using commands):

```sh
cd liwanag-backend
mkdir src
cd src
mkdir word_api/addVocabulary
cd word_api/addVocabulary
```

Create a new `app.py` file inside the folder with the following structure:

```python
import json

def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Hello from Lambda!"})
    }
```

## Step 4: Update `template.yaml`

Modify `template.yaml` to include the new function:

```yaml
Resources:

  addVocabulary:
		Type: AWS::Serverless::Function
		Properties:
			CodeUri: src/word_api/addVocabulary
			Handler: app.lambda_handler
			Runtime: python3.13
			Policies:
				- AWSLambdaBasicExecutionRole
			Architectures:
				- x86_64
			Events:
				ApiEvent:
					Type: Api
					Properties:
						# RestApiId: "lghoog0yu1"
						Path: /words
						Method: post
```

This hypothetical function would require access to DynamoDB , so you would have to update the IAM policy accordingly:

```yaml
      Policies:
        - AWSLambdaBasicExecutionRole
        - AmazonDynamoDBFullAccess  # Modify as per least privilege principle
```
Some functions will require custom policies which you can also add in the template. For example, I used this custom policy statement for the *deleteUserById* function in *user_api*.
```yaml
      Policies:
        - AWSLambdaBasicExecutionRole
        - AmazonDynamoDBFullAccess
        - Statement:
						- Effect: Allow
							Action:
								- dynamodb:DeleteResourcePolicy
								- dynamodb:DeleteItem
								- dynamodb:Query
							Resource: arn:aws:dynamodb:us-west-1:207567790755:table/Users					
```
If you want to see what the template looks like for a DynamoDB table, you can take a look in the *user_api* GitHub repository branch.

## Step 5: Build and Deploy the Function

### Deploy using guided mode (first-time setup):

```sh
sam deploy --guided
```
Follow the prompts to configure stack name (*liwanag-backend*), AWS region (*us-west-1*), and answer the next responses according to the image below.  

[SAM Deploy Responses](https://photos.app.goo.gl/gusVPrfxuF6yhjzt5)

After the first deployment, you can use:

```sh
sam deploy
```

## Step 6: Test the Deployment

After deployment, you can travel to *liwanag-backend* found in API Gateway and go to Stages. There you will find the "Stage" stage and it's URL endpoint. Use it to test the function in [Postman](https://www.postman.com/) by creating a new request and choosing the *POST* method, shown in the image below.

[Postman Request](https://photos.app.goo.gl/oSKL1wxcKbXVnNeeA)

## Additional Notes

-   If using DynamoDB, ensure IAM roles are updated for Lambda permissions.
-   To update an existing function, modify `app.py`, then rebuild and redeploy using `sam deploy`.
-   To add another API, repeat steps 3–5, adjusting paths and function names accordingly.

This setup ensures quick API function development within the existing repository. Happy coding!
