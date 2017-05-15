
import boto3
import json
from time import gmtime, strftime

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
        
        order = ordertable.get_item(
            Key={
                'order_id': event['order_id']
            }
        )
        
        #print order
        
        menu = menutable.get_item(
            Key={
                'menu_id': order['Item']['menu_id']
            }
        )
        
        if order['Item'].get('order') is None:
            
            ordertable.update_item(
                Key={
                'order_id': event['order_id']
                },
                UpdateExpression="set #or = :val",
                ExpressionAttributeNames = {
                    "#or":"order"
                
                },
                ExpressionAttributeValues={
                    ':val': {
                        "selection": menu['Item']['selection'][int(event['input'])-1]
                        }
                }
            )
            response = "Which size do you want? "
            count = 1
            for i in menu['Item']['size']:
                response += str(count) + ". " + str(i)+" "
                count += 1
            return {
                'Message': response
                }
            
        else :
            
            ordertable.update_item(
                Key={
                'order_id': event['order_id']
                },
                UpdateExpression="set #or.size = :val1,#or.costs = :val2,#or.order_time=:val3,#or.order_status=:val4",
                ExpressionAttributeNames = {
                    "#or":"order"
                
                },
                ExpressionAttributeValues={
                    ':val1': menu['Item']['size'][int(event['input'])-1],
                    ':val2':"15.00",
                    ':val3': strftime("%m-%d-%Y@%H:%M:%S", gmtime()), #"mm-dd-yyyy@hh:mm:ss"
                    ':val4':"processing"
                        
                }
            )
            response = "Your order costs $15.00. We will email you when the order is ready. Thank you!"
            count = 1
            
            return {
                'Message': response
                }
            
            
    except Exception as e:
        return  e
            
