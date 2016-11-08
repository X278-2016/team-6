import string, requests, os, json, sys
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

def getSession():
	requests_session = requests.session()
	requests_session.mount('file:\\\\', LocalFileAdapter())
	r = requests_session.get('file:\\\\C:\\Users\\jsamost\\EnergyPlusV8-6-0\\ExampleFiles\\CoolingTowerTable.html')
	return BeautifulSoup(r.content, 'html.parser')


def doParse():
	soup = getSession()
	end = []
	for i in soup.find_all(True):
		if i.name == 'b':
			end.append(str(i.get_text()).strip())
		elif i.name == 'table':
			end[len(end)-1] = [end[len(end)-1] , parse_table(i)]
	return filter(lambda x : type(x) == list, end)

def parse_table(soup):
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


def list_to_dict():
	out = []
	for val in doParse():
		tmp = {}
		for i in val[1]:
			sub = [{x[0] : x[1]} for x in i[1]]
			d = {}
			for j in sub:
				d.update(j)
			tmp.update({i[0] : d})
		out += [{val[0] : tmp}]
	return out

print json.dumps(list_to_dict())