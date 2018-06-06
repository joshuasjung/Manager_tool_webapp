import json
import requests
import credentials

API_TOKEN = ""
API_URI_BASE = credentials.login['API_URI_BASE']
CLIENT_ID = credentials.login['CLIENT_ID']
CLIENT_SECRET = credentials.login['CLIENT_SECRET']
AUTH_POST_DATA = 'client_id=' + CLIENT_ID +'&client_secret=' + CLIENT_SECRET


def get_account_token():
	api_url = '{}api/oauth/token'.format(API_URI_BASE)
	response = requests.post(api_url, AUTH_POST_DATA)
	
	if response.status_code == 200:
		global API_TOKEN
		API_TOKEN = (json.loads(response.content.decode('utf-8')))['access_token']
		print(API_TOKEN)
		return make_headers(API_TOKEN)
	else:
		return None

def make_headers(token):
	HEADERS = {'Content-Type': 'application/json', 'User-Agent': 'Python',
           'Authorization': 'Bearer {}'.format(token)}
	get_company_id(HEADERS)


def get_company_id(HEADERS):
	COMPANY_ID = {}
	api_url = '{}api/v3/partner/companies?per_page=100'.format(API_URI_BASE)
	response = requests.get(api_url, headers = HEADERS)

	if response.status_code == 200:
		DATAS = (json.loads(response.content.decode('utf-8')))
		for DATA in DATAS:
			COMPANY_ID[DATA['name']] = (DATA['id'])
		return get_cert(COMPANY_ID,HEADERS)
	else:
		return None

def get_cert(COMPANY_ID,HEADERS):
	COMPANIES = {}
	for k, v in COMPANY_ID.items():
		#print(v)
		
		api_url = ('{}api/v3/partner/companies_api/'+v+'/ssl_certificates').format(API_URI_BASE)
		response = requests.get(api_url, headers = HEADERS)
		DATAS = (json.loads(response.content.decode('utf-8')))
		COMPANIES[k] = DATAS
	return make_organize(COMPANIES)

def make_organize(COMPANIES):
	print(COMPANIES)

get_account_token()
