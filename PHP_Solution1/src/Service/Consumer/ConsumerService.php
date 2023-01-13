<?php

namespace App\Service\Consumer;

use App\Entity\Results;
use Doctrine\ORM\EntityManagerInterface;
use PhpAmqpLib\Connection\AMQPStreamConnection;
use PhpAmqpLib\Message\AMQPMessage;
use PhpAmqpLib\Exception\AMQPProtocolChannelException;


class ConsumerService
{
    private $em;
    private $connection;
    private $channel;
    private $exchange;
    private $queue;

    public function __construct(EntityManagerInterface $em, $hostname, $username, $password, $exchange, $queue)
    {
        $this->em = $em;
        $this->connection = new AMQPStreamConnection($hostname, 5672, $username, $password);
        $this->channel = $this->connection->channel();

        try {
            $this->channel->exchange_declare($exchange, 'direct', true);
        } catch (PhpAmqpLib\Exception\AMQPProtocolChannelException $e) {
            $this->channel->exchange_declare($exchange, 'direct', false, true, false);
        }
        
        list($queue_name, , ) = $this->channel->queue_declare($queue, false, true, false, false);
        $this->channel->queue_bind($queue_name, $exchange);
    }



    public function startConsuming()
    {
        $callback = function ($msg) {
            $message = json_decode($msg->body, true);
            $routing_key = explode('.', $msg->delivery_info['routing_key']);
            $keys = ["gatewayEui", "profileId", "endpointId", "clusterId", "attributeId"];
            $data = array_combine($keys, $routing_key);
            $data = array_merge($data, $message);
            if (strlen($msg->delivery_info['routing_key']) > 0) {
                $this->storeResults($data);
            } else {
                echo "Empty message.";
            }
        };

        $this->channel->basic_consume($queue, '', false, true, false, false, $callback);

        while (count($this->channel->callbacks)) {
            $this->channel->wait();
        }
    }

    public function stopConsuming()
    {
        $this->channel->close();
        $this->connection->close();
    }

    public function storeResults(array $filteredResults)
    {
        $result = new Results();
        $result->setGatewayEui($filteredResults["gatewayEui"]);
        $result->setProfileId($filteredResults["profileId"]);
        $result->setEndpointId($filteredResults["endpointId"]);
        $result->setClusterId($filteredResults["clusterId"]);
        $result->setAttributeId($filteredResults["attributeId"]);
        $result->setTimestamp($filteredResults["timestamp"]);
        $result->setValue($filteredResults["value"]);

        $this->em->persist($result);
        $this->em->flush();
    }
}