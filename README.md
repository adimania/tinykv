# tinykv
A lightweight python library to perform key value operations on Etcd and Consul

###Supported key values stores:
- Etcd
- Consul

###Supported functions:
- set_value(key, value): sets or updates the value of a key.
- get_json(key, recurse=False): get the raw json output from the key value store 
- get_kv(key, recurse=False): get just the key values from the key value store
- delete(key, recurse=False): delete the key from the key value store

###Requirements
- python-requests

###Example
```python
>>> import tinykv
>>> conn=tinykv.Tinykv("etcd://127.0.0.1:4001")
>>> conn.set_value("key1","value1")
{'response': 201}
>>> conn.set_value("key2","value2")
{'response': 201}
>>> conn.set_value("key3/subkey1","subvalue1")
{'response': 201}
>>> conn.set_value("key3/subkey2","subvalue2")
{'response': 201}
>>> conn.set_value("key3/subkey3/subsubkey1","subsubvalue1")
{'response': 201}
>>> conn.get_kv("key3")
{u'/key3/subkey2': u'subvalue2', u'/key3/subkey1': u'subvalue1'}
>>> conn.get_kv("key3", recurse=True)
{u'/key3/subkey2': u'subvalue2', u'/key3/subkey3/subsubkey1': u'subsubvalue1', u'/key3/subkey1': u'subvalue1'}
>>> >>> conn.get_json("key3")
{u'action': u'get', u'node': {u'createdIndex': 1545631, u'modifiedIndex': 1545631, u'nodes': [{u'createdIndex': 1545631, u'modifiedIndex': 1545631, u'value': u'subvalue1', u'key': u'/key3/subkey1'}, {u'createdIndex': 1545632, u'modifiedIndex': 1545632, u'value': u'subvalue2', u'key': u'/key3/subkey2'}, {u'createdIndex': 1545633, u'modifiedIndex': 1545633, u'dir': True, u'key': u'/key3/subkey3'}], u'dir': True, u'key': u'/key3'}}
>>> conn.get_json("key3", recurse=True)
{u'action': u'get', u'node': {u'createdIndex': 1545631, u'modifiedIndex': 1545631, u'nodes': [{u'createdIndex': 1545631, u'modifiedIndex': 1545631, u'value': u'subvalue1', u'key': u'/key3/subkey1'}, {u'createdIndex': 1545632, u'modifiedIndex': 1545632, u'value': u'subvalue2', u'key': u'/key3/subkey2'}, {u'createdIndex': 1545633, u'modifiedIndex': 1545633, u'nodes': [{u'createdIndex': 1545633, u'modifiedIndex': 1545633, u'value': u'subsubvalue1', u'key': u'/key3/subkey3/subsubkey1'}], u'dir': True, u'key': u'/key3/subkey3'}], u'dir': True, u'key': u'/key3'}}
>>> conn.delete("key3", recurse=True)
{'response': 200


