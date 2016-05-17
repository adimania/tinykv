import requests
import base64

class Tinykv:
	def __init__(self, url):
		self.backend = url.split("://")[0]
		self.parent_url = url.split("://")[1]

	def get_endpoint(self, key, recurse=False):
		if self.backend == "consul":
			base_endpoint = "http://%s/v1/kv/%s" % (self.parent_url, key)
			if recurse == True:
				endpoint = base_endpoint + "?recurse=true"
		elif self.backend == "etcd":
			base_endpoint = "http://%s/v2/keys/%s" % (self.parent_url, key)
			if recurse == True:
				endpoint = base_endpoint + "?recursive=true"
	
		if recurse == False:
			endpoint = base_endpoint
	
		return endpoint
	
	def get_json(self, key, recurse=False):
		try:
			endpoint = self.get_endpoint(key, recurse)
			data = requests.get(endpoint)
			if data.status_code == 200:
				return data.json()
			else:
				return {"error":"data not found"}
		except:
			return {"error":"cannot retrive data"}
	
	def etcd_tree(self, json_data, recurse, kv = {}):
		try:
			if recurse:
				for data in json_data:
					if 'nodes' in data:
						self.etcd_tree(data['nodes'],  kv)
					else:
						kv[data['key']] = data['value']
			else:
				for data in json_data:
					if 'value' in data:
						kv[data['key']] = data['value']
					
		except:
			return {"error":"cannot parse etcd tree"}
		return kv    
	
	def get_kv(self, key, recurse=False):
		try:
			json_data = self.get_json(key, recurse)
			if self.backend == "etcd":
				return self.etcd_tree(json_data['node']['nodes'], recurse)
			if self.backend == "consul":
				kv = {}
				for data in json_data:
					kv[data['Key']] = base64.b64decode(data['Value'])
				return kv
		
		except:
			return {"error":"cannot retrive data"}
	
	def set_value(self, key, value, **kwargs):
		try:
			endpoint = self.get_endpoint(key, recurse=False)
			if self.backend == "consul":
				payload = value
			elif self.backend == "etcd":
				payload = {"value": value}
			
			request = requests.put(endpoint, payload)
			return {"response":request.status_code}
		except:
			return {"error":"cannot set data"}
	
	def delete(self, key, recurse=False):
		try:
			endpoint = self.get_endpoint(key, recurse)
			data = requests.delete(endpoint)
			return {"response":data.status_code}
		except:
			return {"error":"cannot delete data"}
