# Flask Pymongo Blog

--Just Read The Instructions--

Blog app based on Flask and Pymongo.

Below is instructions to get started connecting to your mongo database
```python
from pymongo import MongoClient
```

if you want to configure this app rename "db_config_example" to "db_config.py" and fill out accordingly
all of these are examples, leave the variable names alone
```python
server_url = 'ds100000.mlab.com:10000' #db uri you want to connect to
db_server_name = 'example_blog' #name of database
```

below the user and pass is for the db, if you're using mlab, do not use your login credentials, it wont work
```python
db_user = 'admin'
db_pass = 'admin123'
```
whats in quotes is the collections pymongo will look for in the actual database
```python
user_collection = 'user-example-collection'
post_collection = 'post-example-collection'
comments_collection = 'comments-example-collection'
```

below is an example secret-key, you do not need this for the
data base, however you do need it for the app
```python
sec_key = 'hello-hsfdsahfsdlakjfldsjfljfsd'
```

to install all the required python packages, in the command line run "pip install -r requirements.txt"

if you have added packages to the projects create a new requirements.txt "pip freeze > requirements.txt"