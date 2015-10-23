BucketList Application API ![Travis build badge](https://travis-ci.org/andela-osule/bucket-list-api.svg?branch=master)
==========================
This is a Flask API for a bucket list service. Specification for the API is shown below.

Available Endpoints
-------------------
* POST /auth/login : Logs a user in
* GET /auth/logout : Logs a user out
* POST /bucketlists/ : Create a new bucket list
* GET /bucketlists/ : List all the created bucket lists
* GET /bucketlists/<id> : Get single bucket list
* PUT /bucketlists/<id> : Update single bucket list
* DELETE /bucketlists/<id> : Delete single bucket list
* POST /bucketlists/<id>/items : Add a new item to this bucket list
* PUT /bucketlists/<id>/items/<item_id> : Update this bucket list
* DELETE /bucketlists/<id>/items/<item_id> : Delete this single bucket list
* GET http://localhost:5555/bucketlists?limit=20 : Gets 20 bucket list records belonging to user. Allows for a maximum of 100 records
* GET http://localhost:5555/bucketlists?q=bucket1 : Searches for a bucket lists with bucket1 in their name
