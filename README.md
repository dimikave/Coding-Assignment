# Real-time Data Processing API
This project is focused on consuming real-time data from an API endpoint, processing it, and storing it in a database for further analysis.

## Overview
The project is designed to mimic the dataset received from hardware in the field, and it includes the following tasks:

1. Consume data from an API endpoint
2. Send the results to an exchange on a RabbitMQ instance where they are filtered
3. Consume the filtered results from a queue
4. Store these results in a database designed by the user


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

This README file will be updated with more details about the code and how to run the project as the development progresses.
