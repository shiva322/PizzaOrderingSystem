
import boto3
import json

def lambda_handler(event, context):
    '''Demonstrates a simple HTTP endpoint using API Gateway. You have full
    access to the request and response payload, including headers and
    status code.

    To scan a DynamoDB table, make a GET request with the TableName as a
    query string parameter. To put, update, or delete an item, make a POST,
    PUT, or DELETE request respectively, passing in the payload to the
    DynamoDB API as a JSON body.
    '''
    #print("Received event: " + json.dumps(event, indent=2))

    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    ordertable = dynamodb.Table('pizzaorders')
    
    try :
        
        order = ordertable.get_item(
            Key={
                'order_id': event['order_id']
            }
        )
        
        return order['Item']
                
   
            
    except Exception as e:
        return e
            
