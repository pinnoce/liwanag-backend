import json
import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal

dynamodb = boto3.resource("dynamodb") # Initialize the DynamoDB table
table = dynamodb.Table("Users") # Specify the table name

def lambda_handler(event, context):

    if event.get("httpMethod") != "GET":
        return {
            "statusCode": 405,
            "body": json.dumps({"message": "Method Not Allowed"})
        }
    
    user_id = event['pathParameters']['user_id'] # Extract user_id from the path parameters

    try:
        # Ensure user_id is treated as a number
        user_id = int(user_id)
        
        response = table.query(KeyConditionExpression=Key('user_id').eq(user_id))

        if 'Items' in response and len(response['Items']) > 0:
            user = response['Items'][0]
            return {
                'statusCode': 200,
                'body': json.dumps(user, default=decimal_default)
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'User not found'})
            }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal Server Error', 'error': str(e)})
        }

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    raise TypeError