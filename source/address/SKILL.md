---
name: address
description: "Handles Address entity management including street addresses, cities, states, countries, and postal codes in Bone Framework applications."
version: "1.0.0"
author: "Bone Framework Team"
tags: ["php", "bone-framework", "address", "location", "billing", "shipping"]
trigger_patterns:
  - "address"
  - "location"
  - "billing address"
  - "shipping address"
  - "street address"
---

# Address Skill

## When to Use
Activate this skill when working with Address entities in Bone Framework applications for storing and managing physical addresses, billing/shipping addresses, or location information.

## Overview

The Address entity represents a physical location with components like street, city, state/province, postal code, and country. This is commonly used for:
- Customer billing and shipping addresses
- Business locations
- Contact information storage
- Geographic data management

## Address Structure

### Address Components
| Component | Type | Description |
|-----------|------|-------------|
| `id` | int | Unique identifier |
| `address1` | string | Street address (primary line) |
| `address2` | string | Street address (secondary line) |
| `address3` | string | Street address (tertiary line, rarely used) |
| `city` | string | City/town name |
| `state` | string | State/province/region |
| `postal_code` | string | ZIP/postal code |
| `country` | string | Country (2-letter ISO code or full name) |
| `latitude` | float | Geographic latitude (optional) |
| `longitude` | float | Geographic longitude (optional) |

## Entity Example

### Basic Address Entity (Doctrine)
```php
#[ORM\Entity]
#[ORM\Table(name: 'addresses')]
class Address
{
    use Bone\Doctrine\Traits\HasIdTrait;
    use Bone\Doctrine\Traits\TimestampableTrait;

    #[ORM\Column(type: 'string', length: 255)]
    private string $address1;

    #[ORM\Column(type: 'string', length: 255, nullable: true)]
    private ?string $address2;

    #[ORM\Column(type: 'string', length: 100)]
    private string $city;

    #[ORM\Column(type: 'string', length: 50)]
    private string $state;

    #[ORM\Column(type: 'string', length: 20)]
    private string $postalCode;

    #[ORM\Column(type: 'string', length: 50)]
    private string $country;

    #[ORM\Column(type: 'string', length: 50, nullable: true)]
    private ?string $label;

    public function getFullAddress(): string
    {
        $parts = array_filter([
            $this->address1,
            $this->address2,
            $this->city . ', ' . $this->state . ' ' . $this->postalCode,
            $this->country
        ]);
        return implode("\n", $parts);
    }
}
```

## Common Use Cases

### Creating an Address
```php
$address = new Address();
$address->setAddress1('123 Main Street')
        ->setAddress2('Apt 4B')
        ->setCity('New York')
        ->setState('NY')
        ->setPostalCode('10001')
        ->setCountry('US')
        ->setLabel('Home');

$em->persist($address);
$em->flush();
```

### Finding Addresses
```php
// Find by user
$addresses = $em->getRepository(Address::class)->findBy([
    'user' => $user
]);

// Search by city
$addresses = $em->getRepository(Address::class)->findBy([
    'city' => 'Boston'
]);
```

## Address Relationships

### Address to User (Many-to-One)
```php
#[ORM\ManyToOne(targetEntity: User::class, inversedBy: 'addresses')]
#[ORM\JoinColumn(name: 'user_id', referencedColumnName: 'id')]
private User $user;

#[ORM\Column(type: 'string', length: 50, nullable: true)]
private ?string $label = 'Default';
```

### Address to Order
```php
#[ORM\ManyToOne(targetEntity: Address::class)]
#[ORM\JoinColumn(name: 'shipping_address_id', referencedColumnName: 'id')]
private Address $shippingAddress;

#[ORM\ManyToOne(targetEntity: Address::class)]
#[ORM\JoinColumn(name: 'billing_address_id', referencedColumnName: 'id')]
private Address $billingAddress;
```

## Best Practices

1. Use ISO country codes (2-letter)
2. Separate address lines for flexibility
3. Normalize state/province abbreviations
4. Add address type labels (Home, Work, Billing)
5. Index frequently queried fields
6. Handle international address formats
7. Add geographic coordinates for mapping
8. Use enums for address types
9. Add audit fields
10. Consider soft deletes for history

## Address-related Packages

- **bone-user**: User addresses for customer accounts
- **bone-user-api**: REST API for user address management
- **bone-form**: Address form generation and validation
