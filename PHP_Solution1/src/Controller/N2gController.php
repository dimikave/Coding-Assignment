<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\Routing\Annotation\Route;

class N2gController extends AbstractController
{
    /**
     * @Route("/main", name="main")
     */
    public function main(API $api, RabbitMQ $rabbitmq, ConsumerService $consumerService)
    {
        // Get data from the API
        $results = $api->getResults();
        
        // Attempt to publish data to the queue
        $filteredResults = $rabbitmq->sendToExchange($results);

        // If the data was successfully published, store it in the database
        if ($filteredResults) {
            $consumerService->storeResults($filteredResults);
        }

        // Start consuming messages
        $consumerService->startConsuming();

        // Print the contents of the database
        $results = $consumerService->getResults();
        dump($results);

        return new Response();
    }
}
