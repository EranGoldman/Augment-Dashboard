import boto3
from urllib import unquote
from boto3.dynamodb.conditions import Key, Attr
from boto.dynamodb2.table import Table
import simplejson as json
import io
import time
def download():

	print "starting query script \n"
	dynamodb = boto3.resource('dynamodb',region_name='us-east-1')
	table = dynamodb.Table('staging_engagement_history')

	retries = 0

	with io.open('data.json', 'w', encoding='utf8') as outfile:
	    finalExport = "[" #outside bracket
	    response = table.scan(
	        FilterExpression=Attr('agentId').eq('176680014') | Attr('agentId').eq('176624514') | Attr('agentId').eq('176643814') & Attr('startTime').gt('2017-07-08 00:00:00.000+0000'),
	    )
	    items = response['Items']
	    first = json.dumps(items) #firstScan
	    if first.startswith('[') and first.endswith(']'):
	        first = first[1:-1] #strips outside brackets
	    if first: #if first scan contains anything at all, we want to include it
	        finalExport = finalExport + "\n" + first

	    print "doing one scan iteration... \n"
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
	        print "doing one scan iteration...  \n"
	    finalExport = finalExport + "]"
	    outfile.write(finalExport.decode('unicode-escape'))
	return finalExport



def download_session(str):
	print "starting session query script \n"
	print str
	# print " <---- URL before unescaping \n"
	# str = str.decode('string_escape')
	# print str
	# print " <---- URL before unescaping \n"
	dynamodb = boto3.resource('dynamodb',region_name='us-east-1')
	table = dynamodb.Table('staging_chat_lines')
	retries = 0

	with io.open('data.json', 'w', encoding='utf8') as outfile:
	    finalExport = "[" #outside bracket
	    response = table.scan(
	        FilterExpression=Attr('engagementId').eq(str),
	    )
	    items = response['Items']
	    first = json.dumps(items) #firstScan
	    if first.startswith('[') and first.endswith(']'):
	        first = first[1:-1] #strips outside brackets
	    if first: #if first scan contains anything at all, we want to include it
	        finalExport = finalExport + "\n" + first

	    print "doing one scan iteration... \n"
	    # print(finalExport)
	    while 'LastEvaluatedKey' in response:
	        try:
	            response = table.scan(
	                ExclusiveStartKey=response['LastEvaluatedKey'],
	                FilterExpression=Attr('engagementId').eq(str),
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
	        print "doing one scan iteration...  \n"
	    finalExport = finalExport + "]"
	    outfile.write(finalExport.decode('unicode-escape'))
	return finalExport




def filter_session(sessionIDs, my_dict):
	print sessionIDs
	# print " <---- URL before unescaping \n"
	# sessionIDs = sessionIDs.decode('string_escape')
	# print sessionIDs
	# print " <---- URL before unescaping \n"
	print "STARTING FILTER SCRIPT \n"
	print my_dict['useAugment']
	print my_dict['haveIntent']
	usingAugmentFilter = 0
	hasProblemStatementFilter = 0
	dynamodb = boto3.resource('dynamodb',region_name='us-east-1')
	table = dynamodb.Table('staging_augment_response')
	if my_dict['haveIntent'] == '1':
		global table
		table = dynamodb.Table('staging_augment_response') #haveIntent => staging_augment_response => intent
	elif my_dict['useAugment'] == '1':
		global table
		table = dynamodb.Table('staging_engagement_history') #useAugment => staging_engagement_history => chatAugment exists
	elif my_dict['noAugment'] == '1':
		global table
		table = dynamodb.Table('staging_engagement_history') #noAugment => staging_engagement_history => chatAugment not exists
	else: #if all checkboxes are off, show all chats from the chatLines table for this particular session
		global table
		table = dynamodb.Table('staging_chat_lines') #else => staging_chat_lines => sessionIDs
	retries = 0

	with io.open('data.json', 'w', encoding='utf8') as outfile:
	    finalExport = "[" #outside bracket
	    if(my_dict['haveIntent'] == '1'): #staging_augment_response
		    print "Has Inent Checkbox Checked! \n"
		    global response
		    response = table.scan(
		        FilterExpression=Attr('engagementId').eq(sessionIDs) & Attr('intent').ne('unmatched'),
		    )
	    elif(my_dict['useAugment'] == '1'): #useAugment => staging_engagement_history => chatAugment exists
		    print "useAugment checked \n"
		    global response
		    response = table.scan(
		        FilterExpression= Attr('engagementId').eq(sessionIDs) & Attr('chatAugment').exists(),
		    )
	    elif(my_dict['noAugment'] == '1'): #noAugment => staging_engagement_history => chatAugment not exists
		    print "Has noAugment checkbox checked  \n"
		    global response
		    response = table.scan(
		        FilterExpression= Attr('engagementId').eq(sessionIDs) & Attr('chatAugment').not_exists(),
		    )
	    else: #else => staging_chat_lines => sessionIDs
		    print "None of the checkboxes are checked, prolly \n"
		    global response
		    response = table.scan(
		        FilterExpression=Attr('engagementId').eq(sessionIDs),
		    )
	    items = response['Items']
	    first = json.dumps(items) #firstScan
	    if first.startswith('[') and first.endswith(']'):
	        first = first[1:-1] #strips outside brackets
	    if first: #if first scan contains anything at all, we want to include it
	        finalExport = finalExport + "\n" + first

	    print "doing one scan iteration... \n"
	    # print(finalExport)
	    while 'LastEvaluatedKey' in response:
	        try:
	            if(my_dict['haveIntent'] == '1'):
	                print "Has Inent Checkbox Checked! \n"
	                print response['LastEvaluatedKey']
	                response = table.scan(
	                    ExclusiveStartKey=response['LastEvaluatedKey'],
	                    FilterExpression=Attr('engagementId').eq(sessionIDs) & Attr('intent').ne('unmatched'),
	                )
	            elif(my_dict['useAugment'] == '1'):
	                print "useAugment checked \n"
	                print response['LastEvaluatedKey']
	                response = table.scan(
	                    ExclusiveStartKey=response['LastEvaluatedKey'],
	                    FilterExpression= Attr('engagementId').eq(sessionIDs) & Attr('chatAugment').exists(),
	                )
	            elif(my_dict['noAugment'] == '1'):
	                print "Has noAugment checkbox checked  \n"
	                print response['LastEvaluatedKey']
	                response = table.scan(
	                    ExclusiveStartKey=response['LastEvaluatedKey'],
	                    FilterExpression= Attr('engagementId').eq(sessionIDs) & Attr('chatAugment').not_exists(),
	                )
	            else:
	                print "None of checkboxes are checked"
	                print response['LastEvaluatedKey']
	                response = table.scan(
	                    ExclusiveStartKey=response['LastEvaluatedKey'],
	                    FilterExpression=Attr('engagementId').eq(sessionIDs)
	                )
	        except dynamodb2.exceptions.ProvisionedThroughputExceededException:
	            sleepTime = min(60, (2.**retries)/10.)
	            print 'Sleeping for %.02f secs' % sleepTime
	            time.sleep(sleepTime)
	            retries += 1 if retries < 10 else 0
	        items2 = response['Items']
	        nextScan = json.dumps(items2)
	        print "Final Export in the middle of loop = \n"
	        print finalExport
	        if nextScan.startswith('[') and nextScan.endswith(']'):
	            nextScan = nextScan[1:-1] #strips outside brackets
	        if nextScan: #if next scan contains anything at all, we want to include it
	            if len(finalExport) != 1: #this just checks for the case where first scan was empty, we don't want to add a comma
	                finalExport = finalExport +  "," + "\n"
	            finalExport = finalExport + nextScan
	        print "doing one scan iteration...  \n"
	    finalExport = finalExport + "]"
	    outfile.write(finalExport.decode('unicode-escape'))
	return finalExport



#client = boto3.client('dynamodb', region_name='us-east-1')

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
