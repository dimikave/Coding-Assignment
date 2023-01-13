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
- `python main.py:` Run it if you want to perform all tasks in the same file. This main file works with KeyboardInterruption (Ctrl+C) and 2 basic loops, the Publisher loop and the Consumer loop. Let it run for a while to let the publisher publish some messages to the queue (got from the API), then make a KeyboardInterruption by pressing Ctrl+C to activate the Consumer loop and consume the messages (and also store them into the database). Then again, make a KeyboardInterruption by pressing Ctrl+C, to end the consuming (and storing) operation and finally show the contents of the database. Note that there is a line in the main file to choose if you want to reinitialize the database (if you don't want to, simply comment the line).
- `python main_publisher.py:` Same functionality as main, but only performs as a Publisher (it has the first loop of main, it only publishes to the queue.)
- `python main_consumer.py:` Same functionality as main, but only performs as a Consumer (it has the second loop of main, it only consumes messages from queue and stores the contents into the database.

The main_publisher.py and main_consumer.py are programmed in a way to give the flexibility to the user to run them in 2 different terminals, so one file is a Publisher (gets data from the API and publishes messages to the queue) and the other is a Consumer (consumes messages and stores them into the database).

