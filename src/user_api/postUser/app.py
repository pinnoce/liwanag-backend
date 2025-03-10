import json
import boto3
import random
from datetime import datetime

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Users")

def generate_unique_user_id():
    for _ in range(5):
        user_id = random.randint(100000, 999999)
        response = table.get_item(Key={"user_id": user_id})
        if "Item" not in response:
            return user_id
    raise Exception("Failed to generate a unique user_id after multiple attempts")

def lambda_handler(event, context):
    
    if event.get("httpMethod") != "POST":
        return {
            "statusCode": 405,
            "body": json.dumps({"message": "Method Not Allowed"})
        }
    
    try:
        # Ensure body exists and is not empty
        if not event.get("body"):
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Request body is missing"})
            }

        # Parse JSON safely
        try:
            body = json.loads(event["body"])
        except json.JSONDecodeError:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Invalid JSON format"})
            }

        required_fields = ["first_name", "last_name", "email"] 
        
        if not all(field in body and isinstance(body[field], str) for field in required_fields):
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Missing or invalid required fields"})
            }

        user_id = generate_unique_user_id()

        # Generate current timestamp (UTC)
        current_time = datetime.utcnow().isoformat()

        # Temp avatar (jpg link)
        avatar = "https://static.wikia.nocookie.net/roblox/images/4/40/ManBundle.png/revision/latest/scale-to-width-down/420?cb=20201019175913"

        user_item = {
            "user_id": user_id,
            "first_name": body["first_name"],
            "last_name": body["last_name"],
            "email": body["email"],
            "avatar": avatar,
            "created_time": current_time,
            "updated_time": current_time
        }

        table.put_item(Item=user_item)

        return {
            "statusCode": 201,
            "body": json.dumps({"message": "User created successfully"})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal Server Error", "error": str(e)})
        }
