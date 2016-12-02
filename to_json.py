import string, requests, os, json, sys
from requests import Request, Session
from bs4 import BeautifulSoup 
from requests_testadapter import Resp


class LocalFileAdapter(requests.adapters.HTTPAdapter):
    def build_response_from_file(self, request):
        file_path = request.url[7:]
        with open(file_path, 'rb') as file:
            buff = bytearray(os.path.getsize(file_path))
            file.readinto(buff)
            resp = Resp(buff)
            r = self.build_response(request, resp)

            return r

    def send(self, request, stream=False, timeout=None,
             verify=True, cert=None, proxies=None):
        return self.build_response_from_file(request)


class GetJsonStringFromHTML():
	def __init__(self, top_json, f_name):
		self.top_level_json = top_json 
		self.file_name = f_name

	def get_session(self):
		requests_session = requests.session()
		requests_session.mount('file://', LocalFileAdapter())
		r = requests_session.get(self.file_name)
		return BeautifulSoup(r.content, 'html.parser')


	def do_parse(self):
		soup = self.get_session()
		end = []
		for i in soup.find_all(True):
			if i.name == 'b':
				end.append(str(i.get_text()).strip())
			elif i.name == 'table':
				end[len(end)-1] = [end[len(end)-1] , self.parse_table(i)]
		return filter(lambda x : type(x) == list, end)

	def parse_table(self, soup):
		txt = soup.get_text().split('\n')[2:]
		split = 0 
		for j in range(len(txt)-1):
			if txt[j]=='' and txt[j+1]=='':
				split = j
				break

		y_values = 0 
		for j in range(split + 2 , len(txt) - 1):
			if txt[j]=='' and txt[j+1]=='':
				y_values = j
				break

		header = []
		for j in range(split):
			top = [str(txt[j])]
			sub = []
			for k in range(split + 2, len(txt) - 1 , y_values- split):
				try:
					sub.append([str(txt[k]) , str(txt[k + j + 1]).strip()])
				except:
					pass
			top.append(sub)
			header.append(top)
		return header


	def list_to_dict(self):
		_data_points = ['Cooling Coils', 'Heating Coils', 'Fans', 'Pumps']
		out = []
		for val in self.do_parse():
			tmp = {}
			if val[0] in _data_points:
				for i in val[1]:
					sub = [{x[0] : x[1]} for x in i[1]]
					d = {}
					for j in sub:
						d.update(j)
					tmp.update({i[0] : d})
				out.append(({val[0] : tmp}))
		return out


	def get_string(self):
		value =  "{" + self.top_level_json + ": {"
		for i in self.list_to_dict():
			value += str(json.dumps(i))[1:-1] + ","
		value = value[:-1] + "}}"
		return value



def main():
	#input file is CoolingTower.idf, weather file varies
	a = GetJsonStringFromHTML("\"Tampa_Data\"", 'file://' + sys.argv[1]).get_string()[:-1] + ","
	b = GetJsonStringFromHTML("\"San_Fran_Data\"", 'file://' + sys.argv[2]).get_string()[1:-1] + ","
	c = GetJsonStringFromHTML("\"Chicago_Data\"", 'file://' + sys.argv[3]).get_string()[1:]
	
	print a
	sys.exit()
	send_data(a+b+c)
	

def send_data(json_data):
	s = Session()
	s.get('http://29242ae7.ngrok.io')

	csrf_token = s.cookies['CSRF-TOKEN']
	jsession = s.cookies['JSESSIONID']
		
	milk_and_cooks = s.cookies	

	r = s.get('http://29242ae7.ngrok.io/api/padsets')
	
	headers = {'Host': '29242ae7.ngrok.io',
	'Accept': 'application/json, text/plain, */*',
	'Accept-Language': 'en-us',
	'Accept-Encoding': 'gzip, deflate',
	'Content-Type': 'application/x-www-form-urlencoded',
	'Origin': 'http://29242ae7.ngrok.io',
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Safari/602.1.50',
	'Referer': 'http://29242ae7.ngrok.io/',
	'X-CSRF-TOKEN': csrf_token
	}

	print 'session cookies first post', s.cookies, '\n'
	s.headers = headers
	print 'session headers first post', s.headers, '\n'
	r =  s.post('http://29242ae7.ngrok.io/api/authentication?',  data='j_username=admin&j_password=admin&remember-me=true&submit=Login',  allow_redirects=False)
	print 'SECOND POST\n\n'
	print r.text
	print 'session cookies second post', s.cookies
	print 'session headers second post', s.headers
	s.headers['Content-Type']= 'application/json'
	

	r = s.post('http://29242ae7.ngrok.io/api/create/newpadset', data = json_data)
	#r = s.post('http://29242ae7.ngrok.io/api/padsets', data = json_data)
	print r.text
	print s.cookies

main()

'''
http://stackoverflow.com/questions/2719017/how-to-set-timeout-on-pythons-socket-recv-method
https://docs.python.org/2/library/socket.html
https://wiki.python.org/moin/TcpCommunication
http://stackoverflow.com/questions/9733638/post-json-using-python-requests
'''
