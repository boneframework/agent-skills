---
name: person
description: "Handles Person entity management including personal information, addresses, and contact details in Bone Framework applications."
version: "1.0.0"
author: "Bone Framework Team"
tags: ["php", "bone-framework", "person", "entity", "contact", "profile"]
trigger_patterns:
  - "person"
  - "contact"
  - "profile"
  - "personal information"
  - "address"
---

# Person Skill

## When to Use
Activate this skill when working with Person entities in Bone Framework applications for storing and managing personal information, contact details, and addresses.

## Overview

The Person entity represents a person with:
- Name (first, last, middle)
- Contact information (email, phone)
- Address information
- Avatar/image
- Additional personal details

## Person Entity Structure

### Person Entity (Doctrine)
```php
#[ORM\Entity]
#[ORM\Table(name: 'people')]
class Person
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column(type: 'integer')]
    private int $id;

    #[ORM\Column(type: 'string', length: 50, nullable: true)]
    private ?string $firstName;

    #[ORM\Column(type: 'string', length: 50, nullable: true)]
    private ?string $lastName;

    #[ORM\Column(type: 'string', length: 50, nullable: true)]
    private ?string $middleName;

    #[ORM\Column(type: 'string', length: 100, nullable: true)]
    private ?string $email;

    #[ORM\Column(type: 'string', length: 20, nullable: true)]
    private ?string $phone;

    #[ORM\Column(type: 'string', length: 255, nullable: true)]
    private ?string $avatar;

    #[ORM\OneToOne(targetEntity: Address::class)]
    private ?Address $address;

    #[ORM\Column(type: 'string', length: 255, nullable: true)]
    private ?string $bio;

    #[ORM\Column(type: 'datetime')]
    private \DateTimeInterface $createdAt;

    #[ORM\Column(type: 'datetime', nullable: true)]
    private ?\DateTimeInterface $updatedAt;

    // Getters and setters...
}
```

## Common Use Cases

### Creating a Person
```php
$person = new Person();
$person->setFirstName('John');
$person->setLastName('Doe');
$person->setEmail('john.doe@example.com');
$person->setPhone('+1-555-123-4567');
$person->setBio('Software developer and open source contributor');

$em->persist($person);
$em->flush();
```

### Updating Person Information
```php
$person = $em->getRepository(Person::class)->find($id);
$person->setEmail('new.email@example.com');
$person->setPhone('+1-555-987-6543');

$em->flush();
```

### Finding People
```php
// Find by email
$person = $em->getRepository(Person::class)->findOneBy([
    'email' => 'john.doe@example.com'
]);

// Find by name
$people = $em->getRepository(Person::class)->findBy([
    'firstName' => 'John',
    'lastName' => 'Doe'
]);

// Search by name
$people = $em->createQueryBuilder()
    ->from(Person::class, 'p')
    ->where('p.firstName LIKE :name OR p.lastName LIKE :name')
    ->setParameter('name', '%' . $name . '%')
    ->getQuery()
    ->getResult();
```

## Person in User Context

### Relationship with User
```php
#[ORM\Entity]
#[ORM\Table(name: 'users')]
class User
{
    // ... other properties

    #[ORM\OneToOne(targetEntity: Person::class, inversedBy: 'user')]
    private ?Person $person;

    public function getPerson(): ?Person
    {
        return $this->person;
    }

    public function setPerson(?Person $person): self
    {
        $this->person = $person;
        return $this;
    }
}
```

### Getting User Information
```php
$user = $this->currentUser;
$person = $user->getPerson();

// Access person data
echo $person->getFirstName();
echo $person->getLastName();
echo $person->getEmail();
echo $person->getPhone();
```

## Person Service

### PersonService Class
```php
class PersonService
{
    public function createPerson(array $data): Person
    {
        $person = new Person();
        $person->setFirstName($data['firstName'] ?? null);
        $person->setLastName($data['lastName'] ?? null);
        $person->setEmail($data['email'] ?? null);
        $person->setPhone($data['phone'] ?? null);
        
        $this->em->persist($person);
        $this->em->flush();
        
        return $person;
    }

    public function updatePerson(Person $person, array $data): Person
    {
        if (isset($data['firstName'])) {
            $person->setFirstName($data['firstName']);
        }
        if (isset($data['lastName'])) {
            $person->setLastName($data['lastName']);
        }
        if (isset($data['email'])) {
            $person->setEmail($data['email']);
        }
        if (isset($data['phone'])) {
            $person->setPhone($data['phone']);
        }

        $this->em->flush();
        
        return $person;
    }

    public function getPerson(int $userId): ?Person
    {
        return $this->em->createQueryBuilder()
            ->from(Person::class, 'p')
            ->join('p.user', 'u')
            ->where('u.id = :userId')
            ->setParameter('userId', $userId)
            ->getQuery()
            ->getOneOrNullResult();
    }
}
```

## Person Form

### Form Builder
```php
class PersonForm extends Form
{
    public function init(): void
    {
        $this->addField((new Text('firstName'))
            ->setLabel('First Name')
            ->setRequired(true));
            
        $this->addField((new Text('lastName'))
            ->setLabel('Last Name')
            ->setRequired(true));
            
        $this->addField((new Text('email'))
            ->setLabel('Email')
            ->setRequired(true)
            ->addValidator(new EmailAddress()));
            
        $this->addField((new Text('phone'))
            ->setLabel('Phone')
            ->setAttribute('type', 'tel'));
            
        $this->addField((new TextArea('bio'))
            ->setLabel('Bio')
            ->setAttribute('rows', 3));
    }
}
```

## Person Controller

### Profile Controller
```php
class ProfileController extends Controller
{
    public function viewAction($request)
    {
        $person = $this->currentUser->getPerson();
        
        return $this->view->render('profile/view', [
            'person' => $person,
        ]);
    }
    
    public function editAction($request)
    {
        $person = $this->currentUser->getPerson();
        $form = new PersonForm();
        
        if ($_POST) {
            $form->populate($_POST);
            
            if ($form->isValid()) {
                $data = $form->getValues();
                
                $person->setFirstName($data['firstName']);
                $person->setLastName($data['lastName']);
                $person->setEmail($data['email']);
                $person->setPhone($data['phone']);
                $person->setBio($data['bio']);
                
                $em->flush();
                
                return $this->redirect('/profile');
            }
        }
        
        return $this->view->render('profile/edit', [
            'person' => $person,
            'form' => $form,
        ]);
    }
}
```

## Best Practices

1. **Separate Person from User**: Keep personal info separate from auth
2. **Nullable fields**: Make most fields nullable for flexibility
3. **Validation**: Validate email and phone formats
4. **Avatar storage**: Store avatar paths, not binary data
5. **Audit tracking**: Track creation/update timestamps
6. **Search optimization**: Add search indexes on name/email
7. **Contact details**: Store in structured format
8. **Internationalization**: Support multilingual names
9. **Consistent naming**: Use firstName/lastName consistently
10. **Soft deletes**: Consider active flag for deactivation

## Common Use Cases

### User Registration
```php
public function registerAction()
{
    // Create user
    $user = new User();
    $user->setEmail($email);
    $user->setPassword($password);
    
    // Create person
    $person = new Person();
    $person->setFirstName($firstName);
    $person->setLastName($lastName);
    $person->setEmail($email);
    
    $user->setPerson($person);
    
    $em->persist($user);
    $em->flush();
}
```

### Contact Form
```php
// Store contact form submissions
$person = new Person();
$person->setEmail($email);
$person->setPhone($phone);
$person->setBio($message);

$em->persist($person);
$em->flush();
```

### Importing Contacts
```php
public function importContacts($csvFile)
{
    $handle = fopen($csvFile, 'r');
    
    while (($row = fgetcsv($handle)) !== false) {
        $person = new Person();
        $person->setFirstName($row[0]);
        $person->setLastName($row[1]);
        $person->setEmail($row[2]);
        $person->setPhone($row[3]);
        
        $em->persist($person);
    }
    
    $em->flush();
    fclose($handle);
}
```
