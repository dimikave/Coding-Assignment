<?php

namespace App\Service\RabbitMQ;

use PhpAmqpLib\Connection\AMQPStreamConnection;
use PhpAmqpLib\Message\AMQPMessage;

class RabbitMQService
{
    private $connection;
    private $channel;
    private $exchange;
    private $queue;
    private $username;
    private $password;
    private $hostname;
    private $MAX_RETRIES = 2;
    private $confirm_deliveries = false;

    public function __construct(string $hostname, string $username, string $password, string $exchange, string $queue)
    {
        $this->hostname = $hostname;
        $this->username = $username;
        $this->password = $password;
        $this->exchange = $exchange;
        $this->queue = $queue;

        $this->connection = new AMQPStreamConnection(
            $this->hostname, 
            5672, 
            $this->username, 
            $this->password
        );
        $this->channel = $this->connection->channel();
        $this->channel->confirm_delivery($this->confirm_deliveries);
    }

    public function sendToExchange(array $results)
    {
        //Convert hex to decimal
        $gateway_eui = intval($results["gatewayEui"], 16);
        $profile = intval($results["profileId"], 16);
        $endpoint = intval($results["endpointId"], 16);
        $cluster = intval($results["clusterId"], 16);
        $attribute = intval($results["attributeId"], 16);
        $timestamp = $results["timestamp"];
        $value = $results["value"];

        //Filtered Results
        $filtered_results = [
            "gatewayEui" => $gateway_eui, 
            "profileId" => $profile,
            "endpointId" => $endpoint, 
            "clusterId" => $cluster,
            "attributeId" => $attribute, 
            "timestamp" => $timestamp, 
            "value" => $value
        ];

        //Build routing key
        $routing_key = "{$gateway_eui}.{$profile}.{$endpoint}.{$cluster}.{$attribute}";

        $message = [
            "timestamp" => $timestamp,
            "value" => $value
        ];

        //Initialize retry counter and start attempting to publish the message
        $retries = 0;
        $published_flag = false;
        while($retries < $this->MAX_RETRIES){
            try {
                $this->channel->basic_publish(
                    new AMQPMessage(json_encode($message)),
                    $this->exchange,
                    $routing_key
                );
                $published_flag = true;
                break;
            } catch (\Exception $e) {
                $retries++;
                $delay = 2 ** $retries;
                sleep($delay);
            }
        }
        if(!$published_flag) {
            echo "Message was return as it reached maximum retries and failed to be published.";
        }
        $this->channel->queue_bind($this->queue, $this->exchange, $routing_key);
        return [$filtered_results, $published_flag];
    }
}
