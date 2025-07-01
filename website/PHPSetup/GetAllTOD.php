<?php
// Set the content type header to indicate that the response is JSON.
// This is crucial for clients to correctly interpret the data.
header('Content-Type: application/json');

// Define the relative path to the JSON file.
// __DIR__ is a "magic constant" in PHP that gives the directory of the current file.
// In this case, it's the path to the 'api' directory.
$jsonPath = __DIR__ . '/Data/tod.json';

// Check if the file actually exists to prevent errors.
if (!file_exists($jsonPath)) {
    // If the file is not found, send a 500 Internal Server Error status code.
    // This is more appropriate than a 404, as the endpoint exists but the server
    // is misconfigured or missing a required data file.
    http_response_code(500);
    // Provide a helpful JSON error message.
    echo json_encode(['error' => 'Server data file is missing.']);
    // Stop the script execution.
    exit;
}

// Read the entire content of the file into a string.
// This is the direct equivalent of C#'s File.ReadAllText().
$fullJson = file_get_contents($jsonPath);

// Check if the file could be read. file_get_contents returns false on failure.
if ($fullJson === false) {
    http_response_code(500);
    echo json_encode(['error' => 'Failed to read server data file.']);
    exit;
}

// Send a 200 OK status code (this is the default, but it's good to be explicit).
http_response_code(200);

// Echo the raw JSON string as the response body.
echo $fullJson;

?>