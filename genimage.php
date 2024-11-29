<?php
header("Content-Type: application/json");

// Check if the request is POST
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(["error" => "Only POST requests are allowed"]);
    exit;
}

// Get JSON input
$input = json_decode(file_get_contents('php://input'), true);

// Validate input
if (!isset($input['name'], $input['namePosition'], $input['course'], $input['coursePosition'], $input['date'])) {
    http_response_code(400);
    echo json_encode(["error" => "Missing required fields: name, namePosition, course, coursePosition, date"]);
    exit;
}

$name = $input['name'];
$namePosition = $input['namePosition'];
$course = $input['course'];
$coursePosition = $input['coursePosition'];
$date = $input['date'];

// Load the certificate template
$templatePath = __DIR__ . '/assets/certificate-template.png';
if (!file_exists($templatePath)) {
    http_response_code(500);
    echo json_encode(["error" => "Certificate template not found"]);
    exit;
}

$image = imagecreatefrompng($templatePath);

// Allocate colors
$black = imagecolorallocate($image, 0, 0, 0);

// Configure fonts
$fontPath = __DIR__ . '/assets/arial.ttf'; // Replace with your TTF font path
if (!file_exists($fontPath)) {
    http_response_code(500);
    echo json_encode(["error" => "Font file not found"]);
    exit;
}

// Add name to the image
imagettftext(
    $image, 
    40,  // Font size
    0,   // Angle
    $namePosition['x'], 
    $namePosition['y'], 
    $black, 
    $fontPath, 
    $name
);

// Add course to the image
imagettftext(
    $image, 
    30, 
    0, 
    $coursePosition['x'], 
    $coursePosition['y'], 
    $black, 
    $fontPath, 
    "Course: $course"
);

// Add date to the image (fixed position)
imagettftext(
    $image, 
    20, 
    0, 
    imagesx($image) / 2, 
    imagesy($image) - 50, 
    $black, 
    $fontPath, 
    "Date: $date"
);

// Output the image
header('Content-Type: image/png');
imagepng($image);

// Clean up
imagedestroy($image);
?>
