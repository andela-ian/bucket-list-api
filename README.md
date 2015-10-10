BucketList Application API
==========================
This is a Flask API for a bucket list service. Specification for the API is shown below.

Available Endpoints
-------------------
* POST /auth/login : Logs a user in
* GET /auth/logout : Logs a user out
* POST /bucketlists/ : Create a new bucket list
* GET /bucketlists/ : List all the created bucket lists
* GET /bucketlist/_id_ : Get single bucket list
* POST /bucketlist/_id_ : Add a new item to this bucket list
* PUT /bucketlist/_id_ : Update this bucket list
* DELETE /bucketlist/_id_ : Delete this single bucket list
* GET http://localhost:5555/bucketlists?limit=20 : Gets 20 bucket list records belonging to user. Allows for a maximum of 100 records
* GET http://localhost:5555/bucketlists?q=bucket1 : Searches for a bucket lists with bucket1 in their name
