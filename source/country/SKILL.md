---
name: country
description: "Handles country data and country selection in Bone Framework applications."
version: "1.0.0"
author: "Bone Framework Team"
tags: ["php", "bone-framework", "country", "location", "billing", "shipping"]
trigger_patterns:
  - "country"
  - "countries"
  - "location"
  - "billing country"
  - "shipping country"
---

# Country Skill

## When to Use
Activate this skill when working with country data, country selection, or address management in Bone Framework applications.

## Overview

Country data is essential for:
- Address forms (billing/shipping)
- User registration
- Store location data
- International shipping calculations
- Tax calculations

## ISO 3166-1 Alpha-2 Country Codes

| Code | Country |
|------|---------|
| US | United States |
| CA | Canada |
| GB | United Kingdom |
| DE | Germany |
| FR | France |
| AU | Australia |
| JP | Japan |
| CN | China |
| IN | India |
| BR | Brazil |
| MX | Mexico |
| ES | Spain |
| IT | Italy |
| NL | Netherlands |
| SE | Sweden |
| NO | Norway |
| DK | Denmark |
| FI | Finland |
| PL | Poland |
| CZ | Czech Republic |
| AT | Austria |
| CH | Switzerland |
| BE | Belgium |
| IE | Ireland |
| PT | Portugal |
| GR | Greece |
| RO | Romania |
| HU | Hungary |
| SK | Slovakia |
| SI | Slovenia |

## Form Implementation

### Country Select in Form
```php
use Del\Form\Form;
use Del\Form\Field\Select;

class AddressForm extends Form
{
    public function init(): void
    {
        $this->addField((new Select('country'))
            ->setLabel('Country')
            ->setRequired(true)
            ->setOptions($this->getCountries())
            ->setValue('US'));
    }
    
    public function getCountries(): array
    {
        return [
            '' => 'Select Country',
            'US' => 'United States',
            'CA' => 'Canada',
            'GB' => 'United Kingdom',
            'DE' => 'Germany',
            'FR' => 'France',
            'AU' => 'Australia',
            'JP' => 'Japan',
            'CN' => 'China',
            'IN' => 'India',
            'BR' => 'Brazil',
            'MX' => 'Mexico',
            'ES' => 'Spain',
            'IT' => 'Italy',
            'NL' => 'Netherlands',
            'SE' => 'Sweden',
        ];
    }
}
```

## Person Entity with Country

```php
#[ORM\Entity]
#[ORM\Table(name: 'people')]
class Person
{
    #[ORM\Column(type: 'string', length: 2, nullable: true)]
    private ?string $country;

    #[ORM\Column(type: 'string', length: 50, nullable: true)]
    private ?string $countryName;

    public function getCountry(): ?string
    {
        return $this->country;
    }

    public function setCountry(?string $country): self
    {
        $this->country = $country;
        return $this;
    }
}
```

## Best Practices

1. Use ISO 3166-1 Alpha-2 codes (2-letter)
2. Store both code and full name
3. Sort alphabetically in select
4. Include "Select Country" option
5. Handle empty state
6. Validate country codes
7. Consider internationalization
8. Use database for dynamic lists
9. Group by region if needed
10. Consider country flags

## Common Use Cases

### Address Form
```php
<div class="form-group">
    <label for="country">Country</label>
    <select name="country" class="form-control" required>
        <option value="">Select Country</option>
        <option value="US">United States</option>
        <option value="CA">Canada</option>
        <!-- ... -->
    </select>
</div>
```

### Shipping Calculator
```php
$shippingCosts = [
    'US' => 10.00,
    'CA' => 15.00,
    'GB' => 20.00,
    'DE' => 25.00,
    'FR' => 25.00,
    'AU' => 30.00,
    'JP' => 35.00,
    'other' => 40.00,
];
```
