
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
    menutable = dynamodb.Table('pizzamenu')
    
    try :
        putresponse = ordertable.put_item(
            Item =event
            )
        
        menu = menutable.get_item(
            Key={
                'menu_id': event['menu_id']
            }
        )
        
        response = "Hi "+event['customer_name']+" please choose one of these selection: "
        
        if menu :
            count = 1
            for i in menu['Item']['selection']:
                response += str(count) + ". " + str(i)+" "
                count += 1

        #print(json.dumps(response, indent=4))
        return {
            'Message': response
            }

            
    except Exception as e:
        return  e
            

