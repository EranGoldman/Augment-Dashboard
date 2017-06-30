import boto3
from boto3.dynamodb.conditions import Key, Attr
from boto.dynamodb2.table import Table
import simplejson as json
import io
import time
def download():
	dynamodb = boto3.resource('dynamodb',region_name='us-west-2')
	table = dynamodb.Table('dev_engagement_history')


	# with open('data.json', 'w') as outfile:
	#     response = table.scan(
	#         FilterExpression=Attr('agentId').eq('176680014') & Attr('startTime').gt('2017-06-20 15:01:08.834+0000'),
	#     )
	#     items = response['Items']
	#     json.dump(items, outfile)
	#     while 'LastEvaluatedKey' in response:
	#         response = table.scan(
	#             ExclusiveStartKey=response['LastEvaluatedKey'],
	#             FilterExpression=Attr('agentId').eq('176680014') & Attr('startTime').gt('2017-06-20 15:01:08.834+0000'),
	#         )
	#         print "hello \n"
	#         print(response)
	#         items = response['Items']
	#         json.dump(items, outfile)

	retries = 0

	with io.open('data.json', 'w', encoding='utf8') as outfile:
	    finalExport = "[" #outside bracket
	    response = table.scan(
	        FilterExpression=Attr('agentId').eq('176680014') & Attr('startTime').gt('2017-06-28 00:00:00.000+0000'),
	    )
	    items = response['Items']
	    first = json.dumps(items) #firstScan
	    if first.startswith('[') and first.endswith(']'):
	        first = first[1:-1] #strips outside brackets
	    if first: #if first scan contains anything at all, we want to include it
	        finalExport = finalExport + "\n" + first

	    print "hello \n"
	    print(finalExport)
	    while 'LastEvaluatedKey' in response:
	        try:
	            response = table.scan(
	                ExclusiveStartKey=response['LastEvaluatedKey'],
	                FilterExpression=Attr('agentId').eq('176680014') & Attr('startTime').gt('2017-06-20 15:01:08.834+0000'),
	            )
	        except dynamodb2.exceptions.ProvisionedThroughputExceededException:
	            sleepTime = min(60, (2.**retries)/10.)
	            print 'Sleeping for %.02f secs' % sleepTime
	            time.sleep(sleepTime)
	            retries += 1 if retries < 10 else 0
	        items2 = response['Items']
	        nextScan = json.dumps(items2)
	        if nextScan.startswith('[') and nextScan.endswith(']'):
	            nextScan = nextScan[1:-1] #strips outside brackets
	        if nextScan: #if next scan contains anything at all, we want to include it
	            if len(finalExport) != 1: #this just checks for the case where first scan was empty, we don't want to add a comma
	                finalExport = finalExport +  "," + "\n"
	            finalExport = finalExport + nextScan
	        print "hello \n"
	    finalExport = finalExport + "]"
	    outfile.write(finalExport.decode('unicode-escape'))
	return finalExport






#client = boto3.client('dynamodb', region_name='us-west-2')

# ------------------------------------------------------------
# response = table.get_item(
#    Key={
#         'engagementId': '603792634294969152',
# 	 'created_on' : '2017-06-08 01:21:27.292914'
#     }
# )
#
#
# text = response['Item']['line_text']
#
# print(response)
# print(text)
#
# response = table.scan(
#     FilterExpression=Attr('intent').begins_with('')
# )
# items = response['Items']
#
# for x in range(len(items)):
# 	print(items[x]['line_text'])
#



# ------------------------------------------------------------

# response = table.get_item(
#    Key={
#         'engagementId': '603792634295444491',
#         'accountId' : '60379263'
#     }
# )
# print(response)
# items = response['Item']
# print(items)

# ------------------------------------------------------------


#
# print(response)
# items = response['Items']
# print(items)
# with open('data.json', 'w') as outfile:
#     json.dump(items, outfile)
