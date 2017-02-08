from pymongo import MongoClient
#if you want to configure this app rename to "db_config.py" and fill out accordingly
#all of these are examples!
server_url = 'ds100000.mlab.com:10000' #db uri you want to connect to
db_server_name = 'example_blog' #name of database
#below the user and pass is for the db, if you're using mlab, do not use your login credentials, it wont work
db_user = 'admin'
db_pass = 'admin123'
#whats in quotes is the collections pymongo will look for in the actual database
user_collection = 'user-example-collection'
post_collection = 'post-example-collection'
comments_collection = 'comments-example-collection'

#below is an example secret-key, you do not need this for the
#data base, however you do need it for the app
sec_key = 'hello-hsfdsahfsdlakjfldsjfljfsd'