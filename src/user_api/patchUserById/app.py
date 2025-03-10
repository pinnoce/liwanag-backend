import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource("dynamodb") # Initialize the DynamoDB table
table = dynamodb.Table("Users") # Specify the table name

def lambda_handler(event, context):
    
    if event.get("httpMethod") != "PATCH":
        return {
            "statusCode": 405,
            "body": json.dumps({"message": "Method Not Allowed"})
        }
    
    user_id = event['pathParameters']['user_id'] # Extract user_id from the path parameters
    body = json.loads(event['body']) # Extract the fields to update from the request body

    try:
        # Ensure user_id is treated as a number
        user_id = int(user_id)
        
        # Check if the user exists
        response = table.query(KeyConditionExpression=Key('user_id').eq(user_id))
        
        if 'Items' in response and len(response['Items']) > 0:
            # Prepare the update expression and attribute values
            update_expression = "SET "
            expression_attribute_values = {}
            for key, value in body.items():
                update_expression += f"{key} = :{key}, "
                expression_attribute_values[f":{key}"] = value
            update_expression = update_expression.rstrip(", ")

            # Update the user
            table.update_item(
                Key={'user_id': user_id},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values
            )
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'User updated successfully'})
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