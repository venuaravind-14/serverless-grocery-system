import json
import boto3
import os
from datetime import datetime, timezone
from decimal import Decimal

# Custom JSON encoder to handle Decimal types
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

# Initialize DynamoDB outside handler for connection reuse across invocations
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ.get('DYNAMODB_TABLE', 'inventory-table'))

def lambda_handler(event, context):
    
    try:
        # Parse request body
        body = json.loads(event.get('body', '{}'), parse_float=Decimal)
        item_id = body.get('itemId')
        
        if not item_id:
            return {
                'statusCode': 400,
                'headers': get_headers(),
                'body': json.dumps({'message': 'itemId is required'})
            }
        
        # Check if item exists
        response = table.get_item(Key={'itemId': item_id})
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'headers': get_headers(),
                'body': json.dumps({'message': 'Item not found'})
            }
        
        # Prepare update expression
        update_expr = []
        expr_attrs = {}
        expr_values = {}
        
        updateable_fields = ['name', 'description', 'quantity', 'price', 'category', 'imageUrl']
        
        for field in updateable_fields:
            if field in body:
                val = body[field]
                if field == 'price' and val is not None:
                    val = Decimal(str(val))
                elif field == 'quantity' and val is not None:
                    val = int(val)
                
                update_expr.append(f"#{field} = :{field}")
                expr_attrs[f"#{field}"] = field
                expr_values[f":{field}"] = val
        
        # Add updated timestamp
        update_expr.append("#updatedAt = :updatedAt")
        expr_attrs["#updatedAt"] = "updatedAt"
        expr_values[":updatedAt"] = datetime.now(timezone.utc).isoformat()
        
        # Update item
        table.update_item(
            Key={'itemId': item_id},
            UpdateExpression="SET " + ", ".join(update_expr),
            ExpressionAttributeNames=expr_attrs,
            ExpressionAttributeValues=expr_values
        )
        
        # Get updated item
        updated_item = table.get_item(Key={'itemId': item_id})['Item']
        
        return {
            'statusCode': 200,
            'headers': get_headers(),
            'body': json.dumps({
                'message': 'Item updated successfully',
                'item': updated_item
            }, cls=DecimalEncoder)
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': get_headers(),
            'body': json.dumps({
                'message': 'Failed to update item',
                'error': str(e)
            })
        }

def get_headers():
    return {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'PUT, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type,Authorization,X-Amz-Date,X-Api-Key,X-Amz-Security-Token'
    }

