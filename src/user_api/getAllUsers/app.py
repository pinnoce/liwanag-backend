import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Users")

# Function to convert DynamoDB response (with Decimal) to a serializable format
def decimal_to_float(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, list):
        return [decimal_to_float(item) for item in obj]
    elif isinstance(obj, dict):
        # Check if the key is "user_id" and keep it as int, otherwise convert to float
        return {key: decimal_to_float(value) if key != 'user_id' else int(value) for key, value in obj.items()}
    else:
        return obj

def lambda_handler(event, context):
    
    if event.get("httpMethod") != "GET":
        return {
            "statusCode": 405,
            "body": json.dumps({"message": "Method Not Allowed"})
        }

    try:
        # Scan the Users table to get all items
        response = table.scan()

        # Get the list of users from the response
        users = response.get("Items", [])

        # Convert Decimal values to float in the users list, except for user_id
        users = decimal_to_float(users)

        # Return the list of users in the response body
        return {
            "statusCode": 200,
            "body": json.dumps({"users": users})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal Server Error", "error": str(e)})
        }
