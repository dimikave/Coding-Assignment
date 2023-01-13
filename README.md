# Assignment : Real-time Data Processing Pipeline (Simulation)

## IMPORTANT - Solutions:
For the following assignment, first a Python Solution was programmed (since it is the language I am most comfortable with). This solution is running, it is fully implemented and documented, and is the one I deliver as final solution.  

After that, an effort to provide a second PHP Solution (with Symfony+Doctrine)  was made, but neither the code nor the documentation of this solution is complete (the code is not running). (Note: I never programmed with PHP before this assignment). However, it was an interesting process and I intend to complete this solution on PHP as well in order to get more used to the language.

## Overview of the project:
The project is designed to mimic the dataset received from hardware in the field, and it includes the following tasks:

1. Consume data from an API endpoint (that mimics the dataset usually received from the hardware into the field (gateways) into the platform).
2. Send the results to an exchange on a RabbitMQ instance where they are filtered.
3. Consume the filtered results from a queue.
4. Store these results in a database designed by the user.


## Message Queue
The project utilizes a RabbitMQ instance to filter the results. The following details are provided:

- Hostname
- Credentials
- Exchange name
- Queue name


## Sending Data:
Data must be posted to the exchange in the following format, using the decimal representation of all values:

### Routing Key:
Routing key has the format: 
- (gatewayEui).(profileId).(endpointId).(clusterId).(attributeId)
  
For example, the following routing key is valid:
- 9574384526953556788.260.10.1794.1024

The remaining values of the Result, the timestamp, and the value, are placed in the message body.

## Receiving Data:
Filtered messages are consumed from the queue, and are stored in a mySQL database.

## Database:
The following details are provided for the database:

- Hostname
- Credentials (username and password)
- Database name
  
Please note that the exchange provided is already declared, so the code takes it into consideration (declares the exchange safely if it is not declared, or simply connects if it is). Additionally, the results returned from the API (apart from timestamp and value) are in Hexadecimal format.

