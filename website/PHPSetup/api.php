<?php
// Set the content type for all responses from this API router.
header('Content-Type: application/json');

// Get the requested path from the query string set by .htaccess
$requestUri = trim($_GET['request'] ?? '', '/');

// Simple routing logic.
switch ($requestUri) {
    case 'tod/all':
        // Handle the GET request for all TODOs
        if ($_SERVER['REQUEST_METHOD'] === 'GET') {
            getAllTodItems();
        } else {
            // Method not allowed for this route
            http_response_code(405);
            echo json_encode(['error' => 'Method Not Allowed']);
        }
        break;

    default:
        // Route not found
        http_response_code(404);
        echo json_encode(['error' => 'Endpoint Not Found']);
        break;
}

/**
 * The function that contains the logic from the simple version.
 */
function getAllTodItems() {
    $jsonPath = __DIR__ . '/Data/tod.json';

    if (!file_exists($jsonPath)) {
        http_response_code(500);
        echo json_encode(['error' => 'Server data file is missing.']);
        exit;
    }

    $fullJson = file_get_contents($jsonPath);

    if ($fullJson === false) {
        http_response_code(500);
        echo json_encode(['error' => 'Failed to read server data file.']);
        exit;
    }
    
    // Status is 200 OK by default on success
    echo $fullJson;
}

?>