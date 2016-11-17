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


class GetJsonStringFromHTML():
	def __init__(self, top_json, f_name):
		self.top_level_json = top_json 
		self.file_name = f_name

	def get_session(self):
		requests_session = requests.session()
		requests_session.mount('file:\\\\', LocalFileAdapter())
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
		out = []
		for val in self.do_parse():
			tmp = {}
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
	a = GetJsonStringFromHTML("\"first_name\"", 'file:\\\\C:\\Users\\jsamost\\EnergyPlusV8-6-0\\ExampleFiles\\CoolingTowerTable.html').get_string()[:-1] + ","
	b = GetJsonStringFromHTML("\"second_name\"", 'file:\\\\C:\\Users\\jsamost\\EnergyPlusV8-6-0\\ExampleFiles\\CoolingTowerTable.html').get_string()[1:-1] + ","
	c = GetJsonStringFromHTML("\"third_name\"", 'file:\\\\C:\\Users\\jsamost\\EnergyPlusV8-6-0\\ExampleFiles\\CoolingTowerTable.html').get_string()[1:]

	with open("team-7.json", "w+") as f:
		f.write(a + b + c)


main()

'''
to do::
1. figure out which three .html files to use (how to get each data set)
2. figure out which data points within the html we want
3. pass command line arguments for file location, name of each top level json object
'''

'''
http://stackoverflow.com/questions/2719017/how-to-set-timeout-on-pythons-socket-recv-method
https://docs.python.org/2/library/socket.html
https://wiki.python.org/moin/TcpCommunication
'''