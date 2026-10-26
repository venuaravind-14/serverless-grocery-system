import json
import boto3
import os
import uuid
from datetime import datetime, timezone
from decimal import Decimal

# Initialize DynamoDB outside handler for connection reuse across invocations
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ.get('DYNAMODB_TABLE', 'inventory-table'))

def lambda_handler(event, context):
    
    try:
        # Parse request body
        body = json.loads(event.get('body', '{}'), parse_float=Decimal)  # Convert floats to Decimal
        
        # Generate unique itemId and timestamps
        item_id = str(uuid.uuid4())
        timestamp = datetime.now(timezone.utc).isoformat()
        
        # Create item object
        item = {
            'itemId': item_id,
            'name': body.get('name'),
            'description': body.get('description'),
            'quantity': int(body.get('quantity', 0)),  # Ensure quantity is integer
            'price': Decimal(str(body.get('price', 0))),  # Convert price to Decimal
            'category': body.get('category'),
            'imageUrl': body.get('imageUrl'),
            'createdAt': timestamp,
            'updatedAt': timestamp
        }
        
        # Save to DynamoDB
        table.put_item(Item=item)
        
        # Convert Decimal back to float for JSON response
        response_item = {
            **item,
            'price': float(item['price'])  # Convert Decimal to float for JSON response
        }
        
        return {
            'statusCode': 201,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type,Authorization,X-Amz-Date,X-Api-Key,X-Amz-Security-Token'
            },
            'body': json.dumps({
                'message': 'Item created successfully',
                'item': response_item
            })
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,Authorization,X-Amz-Date,X-Api-Key,X-Amz-Security-Token'
            },
            'body': json.dumps({
                'message': 'Failed to create item',
                'error': str(e)
            })
        }

