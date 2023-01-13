# Python Solution to Assignment

## Installation:
- `git clone https://github.com/dimikave/Coding-Assignment/tree/main/Python_Solution`

### Requirements:
- `pip install -r requirements.txt`

## Code Structure:
The project is using 4 basic scripts:
- `api.py: A class to make GET requests to the API and return the results.`
- `rabbbitmq.py: A class that connects to a RabbitMQ instance and sends messages to a specified exchange using a specified routing key (Publisher)`
- `database.py: A class that connects to a MySQL database and stores and retrieves data.`
- `consumer.py: A class that consumes messages from a specified RabbitMQ queue, processes them and stores them in a database using the Database object of database.py.`
