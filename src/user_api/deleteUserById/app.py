import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource("dynamodb") # Initialize the DynamoDB table
table = dynamodb.Table("Users") # Specify the table name

def lambda_handler(event, context):
    
    if event.get("httpMethod") != "DELETE":
        return {
            "statusCode": 405,
            "body": json.dumps({"message": "Method Not Allowed"})
        }
    
    user_id = event['pathParameters']['user_id'] # Extract user_id from the path parameters

    try:
        # Ensure user_id is treated as a number
        user_id = int(user_id)
        
        # Check if the user exists
        response = table.query(KeyConditionExpression=Key('user_id').eq(user_id))
        
        if 'Items' in response and len(response['Items']) > 0:
            # Delete the user
            table.delete_item(Key={'user_id': user_id})
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'User deleted successfully'})
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