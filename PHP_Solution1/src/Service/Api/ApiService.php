<?php

namespace App\Service\Api;

use GuzzleHttp\Client;

class ApiService
{
    private $client;
    private $hostname;

    public function __construct(string $hostname)
    {
        $this->hostname = $hostname;
        $this->client = new Client();
    }

    public function getResults(): array
    {
        try {
            $response = $this->client->get($this->hostname);
            if ($response->getStatusCode() === 200) {
                return json_decode($response->getBody(), true);
            }
            return [];
        } catch (\Exception $e) {
            return [];
        }
    }
}
