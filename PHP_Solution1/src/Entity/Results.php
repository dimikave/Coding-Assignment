<?php

namespace App\Entity;

use App\Repository\ResultsRepository;
use Doctrine\DBAL\Types\Types;
use Doctrine\ORM\Mapping as ORM;

#[ORM\Entity(repositoryClass: ResultsRepository::class)]
class Results
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column]
    private ?int $id = null;

    #[ORM\Column(type: Types::BIGINT)]
    private ?string $gatewayEui = null;

    #[ORM\Column]
    private ?int $profileId = null;

    #[ORM\Column]
    private ?int $endpointId = null;

    #[ORM\Column]
    private ?int $clusterId = null;

    #[ORM\Column]
    private ?int $attributeId = null;

    #[ORM\Column(type: Types::BIGINT)]
    private ?string $timestamp = null;

    #[ORM\Column]
    private ?float $value = null;

    public function getId(): ?int
    {
        return $this->id;
    }

    public function getGatewayEui(): ?string
    {
        return $this->gatewayEui;
    }

    public function setGatewayEui(string $gatewayEui): self
    {
        $this->gatewayEui = $gatewayEui;

        return $this;
    }

    public function getProfileId(): ?int
    {
        return $this->profileId;
    }

    public function setProfileId(int $profileId): self
    {
        $this->profileId = $profileId;

        return $this;
    }

    public function getEndpointId(): ?int
    {
        return $this->endpointId;
    }

    public function setEndpointId(int $endpointId): self
    {
        $this->endpointId = $endpointId;

        return $this;
    }

    public function getClusterId(): ?int
    {
        return $this->clusterId;
    }

    public function setClusterId(int $clusterId): self
    {
        $this->clusterId = $clusterId;

        return $this;
    }

    public function getAttributeId(): ?int
    {
        return $this->attributeId;
    }

    public function setAttributeId(int $attributeId): self
    {
        $this->attributeId = $attributeId;

        return $this;
    }

    public function getTimestamp(): ?string
    {
        return $this->timestamp;
    }

    public function setTimestamp(string $timestamp): self
    {
        $this->timestamp = $timestamp;

        return $this;
    }

    public function getValue(): ?float
    {
        return $this->value;
    }

    public function setValue(float $value): self
    {
        $this->value = $value;

        return $this;
    }
}
