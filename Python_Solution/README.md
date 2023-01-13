# Python Solution to Assignment

## Installation:
- `git clone https://github.com/dimikave/Coding-Assignment/tree/main/Python_Solution`

### Requirements:
- `pip install -r requirements.txt`

## Code Structure:
The project is using 4 basic scripts:

- api.py: A class to make GET requests to the API and return the results.
- rabbbitmq.py: A class that connects to a RabbitMQ instance and sends messages to an exchange using a routing key (Publisher)
- database.py: A class that connects to a MySQL database and stores and retrieves data.
- consumer.py: A class that consumes messages from a specified RabbitMQ queue, processes them and stores them in a database using the Database object of database.py.

### Run the code:
- `python main.py:` if you want to do all tasks in the same file. In any case, this main file works with KeyboardInterruption (Ctrl+C) and loops, thus let it run for a while to publish some messages (got from the API), then make a KeyboardInterruption by pressing Ctrl+C to activate the Consumer loop and consume the messages (and also store them into the database), and then again, make a KeyboardInterruption by pressing Ctrl+C, to end the operation and finally show the contents of the database.
- `python main_publisher.py:`
