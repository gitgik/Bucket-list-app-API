# Bucket-list-app-API
[![Build Status](https://travis-ci.org/andela-ggikera/Bucket-list-app-API.svg?branch=master)](https://travis-ci.org/andela-ggikera/Bucket-list-app-API)
A feature-rich Flask API for a bucket list service with token based authentication, pagination and search capabilities.
--------------------------------------------------
This is a bucketlist service API built on Flask.

Features include registering and authenticating a user;
creating, retrieving, updating and deleting bucketlist data and bucketlist item data.

###MIME Type
The MIME type for requests is always application/json


###EXAMPLE Requests
```
curl -i -H 'Accept: application/json' 'http://localhost:5000/auth/register'

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 132
Server: Werkzeug/0.10.4 Python/2.7.10
Date: Fri, 08 Jan 2015 14:27:45 GMT

{
  "message": "Welcome to the BucketList service",
  "more": "Please make a POST /register with username and password"
}
```

*NOTE* after login, ensure you  specify the generated token in subsequent request headers as follows:
```
Authorization: Bearer <token>
```

###Dependencies
Install all package requirements in your python virtual environment.
```
pip install -r requirements.txt
```
###Create Database
You need to initialize database and tables with credentials: username _adelle_, password _hello_. Conveniently, there's a command for that!
```
python manager.py createdb -t
```

###Start The Server
Run the following command to start the server and begin listening for requests to each endpoints.
```
python run.py production
```

You can get available environment options by running:
```
python run.py -h
```

###Available Endpoints

| Endpoint | Description |
| ---- | --------------- |
| [POST /auth/login](#) | Login user. Session token is valid for an hour|
| [POST /auth/logout](#) | Logout user. |
| [POST /auth/register](#) |  Register user. Request should have _username_ and _password_ in form data. |
| [POST /bucketlists/](#) | Create a new bucket list. Request should have _name_ in form data. |
| [GET /bucketlists/](#) | List all the created bucket lists. |
| [GET /bucketlists/:id](#) | Get single bucket list. |
| [PUT /bucketlists/:id](#) | Update single bucket list. Request should have _name_ in form data. |
| [DELETE /bucketlists/:id](#) | Delete single bucket list. |
| [POST /bucketlists/:id/items](#) | Add a new item to this bucket list. Request should have _name_, _done_(defaults to False) in form data. |
| [PUT /bucketlists/:id/items/:item_id](#) | Update this bucket list. Request should have _name_, _done_(True or False) in form data. |
| [DELETE /bucketlists/:id/items/:item_id](#) | Delete this single bucket list. |
| [GET /bucketlists?limit=20](#) | Get 20 bucket list records belonging to user. Allows for a maximum of 100 records. |
| [GET /bucketlists?q=bucket1](#) | Search for bucket lists with bucket1 in name. |



