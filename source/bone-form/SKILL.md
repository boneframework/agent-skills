---
name: bone-form
description: "Handles form creation, validation, rendering, and file uploads in Bone Framework applications using delboy1978uk/form package with Laminas Validator integration."
version: "1.0.0"
author: "Bone Framework Team"
tags: ["php", "bone-framework", "form", "validation", "renderer", "laminas"]
trigger_patterns:
  - "form"
  - "validation"
  - "render"
  - "input"
  - "laminas"
  - "html form"
---

# Bone Form Skill

## When to Use
Activate this skill when creating HTML forms with validation, rendering, and file upload handling in Bone Framework applications using the `delboy1978uk/form` package.

## Package Information
- **Package**: `delboy1978uk/form`
- **Dependencies**: laminas/laminas-validator, laminas/laminas-filter
- **License**: MIT
- **PHP Version**: ^8.2
- **Extensions required**: ext-dom, ext-fileinfo
- **Suggested**: delboy1978uk/cdn, delboy1978uk/icon

## Architecture Overview

```
Form (AbstractForm)
├── FieldCollection (holds multiple fields)
├── FormRenderer (renders the form HTML)
└── FieldInterface (all form fields implement this)
    ├── Text (text input)
    ├── Select
    ├── Radio
    ├── CheckBox
    ├── FileUpload
    ├── TextArea
    └── FieldAbstract (base class with validators, filters, traits)
```

## Core Components

### FormInterface
Main interface for all forms:
```php
interface FormInterface
{
    public function isValid(): bool;
    public function getValues(bool $transform = false): array;
    public function populate(array $values): void;
    public function render(): string;
    public function addField(FieldInterface $field): void;
    public function getField(string $name): ?FieldInterface;
}
```

### AbstractForm
Base form class implementing FormInterface:
```php
abstract class AbstractForm implements FormInterface
{
    // Provides field collection, renderer, error handling
    // Abstract init() method for form setup
}
```

### Form
Concrete form implementation:
```php
class Form extends AbstractForm
{
    public function init(): void {}  // Override for field setup
}
```

## Field Types

### Text Fields
- **Text**: Basic text input
- **Integer**: Number input with integer validation
- **EmailAddress**: Email input with email validation
- **Password**: Password input
- **Date**: Date input
- **DateTime**: Date/time input
- **FloatingPoint**: Floating point number input
- **Hidden**: Hidden input
- **TextArea**: Multi-line text area
- **Select**: Dropdown select
- **MultiSelect**: Multiple selection dropdown
- **Radio**: Radio buttons
- **CheckBox**: Checkbox input
- **FileUpload**: File upload input
- **Submit**: Submit button

### Field Common Methods
```php
$field->setValue($value);
$field->getValue();
$field->setLabel('Label Text');
$field->getName();
$field->getId();
$field->isValid();
$field->getMessages();  // Get error messages
$field->setRequired(true);
$field->setPlaceholder('Placeholder text');
```

## Validators

### Available Validators
| Validator | Description |
|-----------|-------------|
| `NotEmpty` | Field cannot be empty |
| `MinLength` | Minimum string length |
| `MaxLength` | Maximum string length |
| `IntegerValidator` | Must be an integer |
| `FloatValidator` | Must be a float |
| `FileExtensionValidator` | File must have allowed extension |
| `MimeTypeValidator` | File must have allowed MIME type |
| `Laminas Validators` | All Laminas validators via adapter |

### Using Validators
```php
use Del\Form\Field\Text;
use Del\Form\Validator\MinLength;
use Del\Form\Validator\MaxLength;

$field = new Text('username');
$field->setRequired(true);
$field->addValidator(new MinLength(3));
$field->addValidator(new MaxLength(20));
```

### Laminas Validators
```php
use Del\Form\Validator\Adapter\ValidatorAdapterZf;
use Laminas\Validator\EmailAddress;

$field = new Text('email');
$field->addValidator(new ValidatorAdapterZf(new EmailAddress()));
```

## Filters

### Available Filters
- **FilterAdapterZf**: Adapts Laminas filters
- **StringTrim**: Trims whitespace
- **StripTags**: Removes HTML tags

### Using Filters
```php
use Del\Form\Filter\Adapter\FilterAdapterZf;
use Laminas\Filter\StringTrim;
use Laminas\Filter\StripTags;

$field = new Text('description');
$field->addFilter(new FilterAdapterZf(new StringTrim()));
$field->addFilter(new FilterAdapterZf(new StripTags()));
```

## Form Rendering

### Basic Form Rendering
```php
$form = new MyForm();
echo $form->render();
```

### Form with Error Display
```php
$form = new MyForm();
$form->setDisplayErrors(true);  // Enable error display
echo $form->render();
```

### Form Attributes
```php
$form->setId('my-form-id');
$form->setClass('form-horizontal');
$form->setMethod('post');
$form->setAction('/submit-url');
$form->setEncType('multipart/form-data');
$form->setAttribute('data-foo', 'bar');
```

## Common Tasks

### 1. Creating a Simple Form
```php
use Del\Form\Form;
use Del\Form\Field\Text;

class ContactForm extends Form
{
    public function init(): void
    {
        $this->addField((new Text('name'))
            ->setLabel('Your Name')
            ->setRequired(true)
            ->setPlaceholder('Enter your name'));
        
        $this->addField((new Text('email'))
            ->setLabel('Email Address')
            ->setRequired(true)
            ->setAttribute('type', 'email'));
        
        $this->addField((new TextArea('message'))
            ->setLabel('Your Message')
            ->setRequired(true)
            ->setAttribute('rows', 5));
        
        $this->addField((new Submit('submit'))
            ->setValue('Send Message'));
    }
}

// Usage
$form = new ContactForm();
echo $form->render();
```

### 2. Creating a Form with Validation
```php
use Del\Form\Form;
use Del\Form\Field\Text;
use Del\Form\Field\Select;
use Del\Form\Validator\MinLength;
use Del\Form\Validator\MaxLength;
use Del\Form\Validator\NotEmpty;

class RegistrationForm extends Form
{
    public function init(): void
    {
        // Username with validation
        $username = new Text('username');
        $username->setLabel('Username');
        $username->setRequired(true);
        $username->addValidator(new NotEmpty());
        $username->addValidator(new MinLength(3));
        $username->addValidator(new MaxLength(20));
        $this->addField($username);
        
        // Email with email validation
        $email = new Text('email');
        $email->setLabel('Email');
        $email->setRequired(true);
        $email->setAttribute('type', 'email');
        $this->addField($email);
        
        // Password with length requirements
        $password = new Text('password');
        $password->setLabel('Password');
        $password->setRequired(true);
        $password->setAttribute('type', 'password');
        $password->addValidator(new MinLength(8));
        $this->addField($password);
        
        // Country selection
        $country = new Select('country');
        $country->setLabel('Country');
        $country->setRequired(true);
        $country->setOptions([
            'us' => 'United States',
            'uk' => 'United Kingdom',
            'ca' => 'Canada',
        ]);
        $this->addField($country);
        
        $this->addField((new Submit('register'))->setValue('Register'));
    }
}
```

### 3. Processing Form Submission
```php
use Del\Form\Form;
use Del\Form\Exception\FormValidationException;

class UserController
{
    public function registerAction()
    {
        $form = new RegistrationForm();
        $form->setAction('/register');
        
        if ($_POST) {
            $form->populate($_POST);
            
            if ($form->isValid()) {
                $data = $form->getValues();
                // Process valid data
                $this->saveUser($data);
                return $this->redirect('/success');
            } else {
                // Form has errors, show with errors
                $form->setDisplayErrors(true);
            }
        }
        
        return $this->view->render('register', ['form' => $form]);
    }
}
```

### 4. Handling File Uploads
```php
use Del\Form\Form;
use Del\Form\Field\FileUpload;

class UploadForm extends Form
{
    public function init(): void
    {
        $file = new FileUpload('avatar');
        $file->setLabel('Profile Picture');
        $file->setRequired(true);
        $file->setUploadDirectory('/var/www/uploads');
        $file->addValidator(new FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif']));
        $this->addField($file);
        
        $this->addField((new Submit('upload'))->setValue('Upload'));
    }
}

// Processing upload
if ($form->isValid()) {
    // Files are automatically moved to upload directory
    $data = $form->getValues();
}
```

### 5. Dynamic Forms (Show/Hide Based on Selection)
```php
use Del\Form\Form;
use Del\Form\Field\Select;
use Del\Form\Field\Text;

class DynamicForm extends Form
{
    public function init(): void
    {
        $type = new Select('contact_type');
        $type->setLabel('Contact Type');
        $type->setOptions([
            'email' => 'Email',
            'phone' => 'Phone',
            'mail' => 'Mail',
        ]);
        $type->setRequired(true);
        
        // Create dynamic forms for each option
        $emailForm = new Form('email_form');
        $emailForm->init();
        $emailForm->addField((new Text('email_address'))
            ->setLabel('Email Address')
            ->setRequired(true));
        
        $phoneForm = new Form('phone_form');
        $phoneForm->init();
        $phoneForm->addField((new Text('phone_number'))
            ->setLabel('Phone Number')
            ->setRequired(true));
        
        $type->addDynamicForm($emailForm, 'email');
        $type->addDynamicForm($phoneForm, 'phone');
        
        $this->addField($type);
    }
}
```

### 6. Using HasFormFields Trait
```php
use Del\Form\Traits\HasFormFields;
use Del\Form\Field\Attributes\Field;

class UserEntity
{
    use HasFormFields;
    
    private string $name = '';
    private string $email = '';
    private int $age = 0;
    
    #[Field(rules: 'text|required')]
    private string $name = '';
    
    #[Field(rules: 'email|required')]
    private string $email = '';
    
    #[Field(rules: 'integer|required')]
    private int $age = 0;
    
    // Populate form data into entity
    public function populateFromForm(FormInterface $form): void
    {
        $this->populate($form);
    }
}
```

### 7. Custom Error Messages
```php
use Del\Form\Field\Text;

$field = new Text('email');
$field->setRequired(true);
// Set custom error message for specific validator
$field->setCustomErrorMessage('Please enter a valid email address');
```

### 8. Using FormRenderer
```php
use Del\Form\Renderer\FormRenderer;

$form = new MyForm();
$renderer = new FormRenderer();
$renderer->setDisplayErrors(true);
echo $renderer->render($form, true);
```

### 9. Collection Fields (Array Values)
```php
use Del\Form\Field\CheckBox;
use Del\Form\Field\MultiSelect;

// Multiple checkboxes
$checkbox = new CheckBox('permissions');
$checkbox->setOptions([
    'read' => 'Read',
    'write' => 'Write',
    'admin' => 'Admin',
]);
$checkbox->checkValue('read');
$checkbox->checkValue('write');
// Value will be: ['read' => true, 'write' => true]

// Multi-select
$multi = new MultiSelect('tags');
$multi->setOptions(['tag1', 'tag2', 'tag3']);
$multi->setValue(['tag1', 'tag3']);
```

### 10. Transformers (Data Conversion)
```php
use Del\Form\Field\Text;
use Del\Form\Field\TransformerInterface;

class DateTransformer implements TransformerInterface
{
    public function input($data): string
    {
        // Convert from DB format to display format
        return date('m/d/Y', strtotime($data));
    }
    
    public function output(string $value)
    {
        // Convert from display format to DB format
        return date('Y-m-d', strtotime($value));
    }
}

$field = new Text('birthday');
$field->setTransformer(new DateTransformer());
```

## Field Traits

### HasOptionsTrait
Provides `setOptions()`, `getOptions()`, `setOption()`, `getOption()` methods.

Used by: Select, MultiSelect, Radio, CheckBox

### CanRenderInlineTrait
For inline rendering of radio buttons and checkboxes.

### HasAttributesTrait
Provides `setAttribute()`, `getAttribute()`, `setAttributes()`, `getAttributes()` methods.

### HasFormFields Trait
Populates entity properties from form data using `#[Field]` attribute.

## Configuration Options

### Form Attributes
- `name`: Form name (required)
- `id`: Form ID
- `method`: HTTP method (default: post)
- `action`: Form action URL
- `enctype`: Encoding type (default: application/x-www-form-urlencoded)
- `class`: CSS classes
- Any HTML attribute via `setAttribute()`

### Field Attributes
- `name`: Field name (required)
- `id`: Field ID
- `class`: CSS classes
- `value`: Field value
- `placeholder`: Input placeholder
- `type`: Input type
- `required`: Required indicator

## Best Practices

1. **Extend AbstractForm**: Always create form classes extending AbstractForm
2. **Use init() method**: Define all fields in the init() method
3. **Set field labels**: Always provide meaningful labels for fields
4. **Use validators**: Validate all user input
5. **Set required fields**: Use `setRequired(true)` for mandatory fields
6. **Enable error display**: Call `setDisplayErrors(true)` before rendering
7. **Handle file uploads**: Set upload directory for FileUpload fields
8. **Use transformers**: For date/time conversion
9. **Group related fields**: Use dynamic forms for conditional fields
10. **Escape output**: Use `e()` helper in templates for form output

## Form Error Handling

```php
$form = new MyForm();

if ($form->isValid()) {
    $data = $form->getValues();
    // Process data
} else {
    $errors = $form->getErrorMessages();
    // $errors = ['field_name' => ['Error message'], ...]
}
```

## Full Example: User Registration

```php
<?php

namespace App\Form;

use Del\Form\Form;
use Del\Form\Field\Text;
use Del\Form\Field\Select;
use Del\Form\Field\CheckBox;
use Del\Form\Field\TextArea;
use Del\Form\Validator\MinLength;
use Del\Form\Validator\MaxLength;
use Del\Form\Validator\NotEmpty;

class UserRegistrationForm extends Form
{
    public function init(): void
    {
        $this->setId('user-registration');
        $this->setMethod('post');
        $this->setAction('/user/register');
        $this->setClass('form-horizontal');
        
        // Username
        $username = new Text('username');
        $username->setLabel('Username');
        $username->setRequired(true);
        $username->setAttribute('placeholder', 'Enter username');
        $username->addValidator(new NotEmpty());
        $username->addValidator(new MinLength(3));
        $username->addValidator(new MaxLength(20));
        $this->addField($username);
        
        // Email
        $email = new Text('email');
        $email->setLabel('Email');
        $email->setRequired(true);
        $email->setAttribute('type', 'email');
        $email->setAttribute('placeholder', 'Enter email');
        $this->addField($email);
        
        // Password
        $password = new Text('password');
        $password->setLabel('Password');
        $password->setRequired(true);
        $password->setAttribute('type', 'password');
        $password->setAttribute('placeholder', 'Enter password');
        $password->addValidator(new NotEmpty());
        $password->addValidator(new MinLength(8));
        $this->addField($password);
        
        // Confirm Password
        $confirmPassword = new Text('confirm_password');
        $confirmPassword->setLabel('Confirm Password');
        $confirmPassword->setRequired(true);
        $confirmPassword->setAttribute('type', 'password');
        $this->addField($confirmPassword);
        
        // Role selection
        $role = new Select('role');
        $role->setLabel('Role');
        $role->setRequired(true);
        $role->setOptions([
            'user' => 'User',
            'admin' => 'Administrator',
        ]);
        $this->addField($role);
        
        // Terms agreement
        $terms = new CheckBox('terms');
        $terms->setLabel('I agree to the terms and conditions');
        $terms->setRequired(true);
        $terms->setOptions(['accepted' => 'Agree']);
        $this->addField($terms);
        
        // Submit button
        $this->addField((new Submit('submit'))->setValue('Register User'));
    }
}
```
