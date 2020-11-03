import json, boto3

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    #
    bucket = event['Records'][0]['s3']['bucket']['name']
    json_file_name = event['Records'][0]['s3']['object']['key']
    #Get the object
    json_object = s3_client.get_object(Bucket=bucket,Key=json_file_name)
    jsonFileReader = json_object['Body'].read()
    jsonDict = json.loads(jsonFileReader)
    
#the object can be added as new item to Dynamo now
    table = dynamodb.Table('dev-cloud-catalog-api-table-eu-west-1')

    prodList=["tekla-structures","tekla-tsd-tedds-ec","tekla-tsd-tedds-bs","tekla-tsd-tedds-us","tekla-tsd-tedds-au","tekla-epm"]

    for prod in prodList:
        #if (jsonDict['sk']=="product:tekla-structures" and i != "tekla-structures"):
        jsonDict['sk']="product:{}".format(prod)
        jsonDict['productId']="{}".format(prod)
        jsonDict['properties']['overall-depth']=int(jsonDict['properties']['overall-depth'])-10
        jsonDict['properties']['overall-breadth']=int(jsonDict['properties']['overall-breadth'])-10
        table.put_item(Item=jsonDict)
#        print (jsonDict['properties']['overall-depth'])
#        print(jsonDict)
#        print (prod)
#Update the jsonDict for other products and add them to the Dynamo    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
