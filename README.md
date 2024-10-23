# ym-simple-fastapi-sample
A simple API performing CRUD operations for customer records built with fastapi

The API offers following 5 methods:

- GET /cusotmers --- Retrieve a list of customers data
- POST /customers --- Add a customers repord
- GET /customers/{customer_id} --- Retrieve a customer record associated with customer_id
- PUT /customers/{customer_id} --- Update a customer record associated with customer_id
- DELETE /customers/{customer_id} --- Delete a customer record associated with customer_id

The customer data is managed in the memory, namely it is refreshed when restarting the server.
