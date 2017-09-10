########### Python 3.2 #############
import http.client, urllib.request, urllib.parse, urllib.error, base64
import json
def luisQuestion(question):
	data="";
	headers = {
		# Request headers
		'Ocp-Apim-Subscription-Key': '5661c2c4874148509dbd644bacfb579d',
	}

	params = urllib.parse.urlencode({
		# Request parameters
		'q':question,
		'timezoneOffset': '480',
		'verbose': 'true',
		'spellCheck': 'false',
		'staging': 'false',
	})
	#https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/?subscription-key=&timezoneOffset=&verbose=&q=

	try:
		conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
		conn.request("GET", "/luis/v2.0/apps/788959ea-76bf-4618-9fec-a9024f4bc2b2?%s" % params, "{body}", headers)
		response = conn.getresponse()
		data = json.loads(response.read().decode('utf-8'))
		data = data['topScoringIntent']['intent']
		conn.close()
	except Exception as e:
		 print("[Errno {0}] {1}".format(e.errno, e.strerror))

	return data
####################################

