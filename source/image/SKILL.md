---
name: image
description: "Handles image processing in Bone Framework applications using delboy1978uk/image package for PHP GD-based image manipulation."
version: "1.0.0"
author: "Bone Framework Team"
tags: ["php", "bone-framework", "image", "gd", "manipulation", "resize", "crop"]
trigger_patterns:
  - "image"
  - "gd"
  - "image processing"
  - "resize"
  - "crop"
  - "php image"
---

# Image Skill

## When to Use
Activate this skill when working with image processing in Bone Framework applications using the `delboy1978uk/image` package for GD-based image manipulation.

## Package Information
- **Package**: `delboy1978uk/image`
- **License**: MIT
- **PHP Version**: ^8.2
- **Dependencies**: ext-gd
- **Supported Formats**: PNG, JPG, GIF, WebP

## Overview

The Image class provides:
- Support for multiple image formats (PNG, JPG, GIF, WebP)
- GD library-based image manipulation
- Methods for resizing, cropping, scaling
- Base64 output for direct HTML embedding
- Memory management with `destroy()`

## Installation

```bash
composer require delboy1978uk/image
```

## Basic Usage

### Creating/Loading an Image
```php
use Del\Image;

// Load existing image
$image = new Image('path/to/image.jpg');

// Or use static factory
$image = Image::load('path/to/image.png');
```

### Image Properties
```php
echo $image->getWidth();   // Get width in pixels
echo $image->getHeight();  // Get height in pixels
echo $image->getHeader();  // Get MIME type (e.g., 'image/jpeg')
```

## Image Manipulation Methods

### Resize
```php
// Resize to exact dimensions
$image->resize(800, 600);

// Resize to width (maintains aspect ratio)
$image->resizeToWidth(800);

// Resize to height (maintains aspect ratio)
$image->resizeToHeight(600);

// Scale by percentage
$image->scale(50); // Scale to 50%
```

### Crop
```php
// Crop to exact dimensions
$image->crop(200, 200);

// Crop with trim option
$image->crop(200, 200, 'center');  // center, left, right
```

### Resize and Crop (Fit)
```php
// Resize and crop to fit dimensions
$image->resizeAndCrop(200, 200);
```

## Saving Images

### Save to File
```php
$image->save('path/to/new-image.jpg');

// With custom permissions and compression
$image->save('path/to/image.jpg', 0755, 90);
```

### Output to Browser
```php
// Output as image
$image->output();

// Output as base64 for HTML img tag
echo '<img src="' . $image->outputBase64Src() . '">';
```

### Get Base64 Source
```php
$base64Src = $image->outputBase64Src();
// Returns: 'data:image/jpeg;base64,/9j/4AAQ...'

// In HTML
echo '<img src="' . $base64Src . '" alt="Image">';
```

## Complete Example

### Profile Avatar Upload
```php
use Del\Image;

class AvatarController extends Controller
{
    public function uploadAction($request)
    {
        $file = $request->getFiles()['avatar'];
        
        // Create image instance
        $image = new Image($file['tmp_name']);
        
        // Resize to 300x300 square
        $image->resizeAndCrop(300, 300);
        
        // Generate filename
        $filename = 'avatar_' . $this->currentUser->getId() . '.jpg';
        $savePath = 'data/uploads/avatars/' . $filename;
        
        // Save image
        $image->save($savePath, 0755, 85);
        
        // Update user record
        $user = $this->currentUser;
        $user->setAvatar($filename);
        $em->flush();
        
        // Free memory
        $image->destroy();
        
        return $this->jsonResponse(['avatarUrl' => '/uploads/avatars/' . $filename]);
    }
}
```

### Thumbnail Generation
```php
public function generateThumbnails($originalPath, $width, $height)
{
    $image = new Image($originalPath);
    
    // Create thumbnail with center crop
    $image->resizeAndCrop($width, $height);
    
    $thumbPath = pathinfo($originalPath, PATHINFO_DIRNAME) . 
                 '/thumb_' . pathinfo($originalPath, PATHINFO_FILENAME) . '.jpg';
    
    $image->save($thumbPath, null, 75);
    
    $image->destroy();
    
    return $thumbPath;
}
```

## Image Strategy Pattern

The Image class uses strategy pattern for different formats:

```php
// Internal strategies
- GifStrategy for GIF images
- JpegStrategy for JPEG images
- PngStrategy for PNG images
- WebPStrategy for WebP images
```

### Custom Strategy
```php
$image->setImageStrategy(new CustomStrategy());
```

## Memory Management

### Proper Cleanup
```php
$image = new Image('path/to/image.jpg');

// ... do work ...

// Always destroy to free memory
$image->destroy();
```

## Error Handling

### Exceptions
```php
try {
    $image = new Image('nonexistent.jpg');
} catch (Del\Image\Exception\NotFoundException $e) {
    // File not found
}

try {
    $image->output();
} catch (Del\Image\Exception\NothingLoadedException $e) {
    // No image loaded
}
```

## Best Practices

1. **Always destroy**: Call `destroy()` when done to free GD resources
2. **Validate input**: Check file is actually an image
3. **Use appropriate quality**: Higher quality = larger files
4. **Cache processed images**: Don't re-process on every request
5. **Use appropriate sizes**: Don't create larger images than needed
6. **Handle transparency**: Preserve transparency for PNG/GIF
7. **WebP support**: Consider using WebP for better compression
8. **Directory permissions**: Ensure write permissions
9. **File naming**: Use unique names to avoid conflicts
10. **Cleanup old files**: Remove unused image files

## Common Use Cases

### Image Resizing
```php
$image = new Image($path);
$image->resizeToWidth(800);
$image->save($path);
```

### Profile Picture Processing
```php
$image = new Image($upload['tmp_name']);
$image->resizeAndCrop(200, 200);
$image->save('data/uploads/profile_' . $userId . '.jpg');
$image->destroy();
```

### Thumbnail Generation
```php
$image = new Image($original);
$image->resizeToWidth(150);
$image->save('data/thumbs/' . $filename . '_thumb.jpg');
```

### Watermark Application
```php
$base = new Image($original);
$watermark = new Image('watermark.png');

// Position watermark
// ... custom positioning code ...

$base->save($path);
$base->destroy();
```
