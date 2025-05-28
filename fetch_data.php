<?php
// Enable error reporting 
ini_set('display_errors', 1);
error_reporting(E_ALL);

// Load config
require 'config.php'; 

$conn = new mysqli($host, $user, $pass, $dbname); 

// Check connection 
if ($conn->connect_error) {
    die('Connection failed: ' . $conn->connect_error); 
}

$query = 'SELECT * FROM notion_data'; 
$result = $conn->query($query);  
$data = [];

while ($row = $result->fetch_assoc()) {
    $data[] = $row; 
}

header('Content-Type: application/json'); 
echo json_encode($data); 
?>
