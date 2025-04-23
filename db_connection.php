<?php
$servername = 'localhost';   // Ensure this ends with a semicolon
$username = 'quocthinh';
$password = 'quocthinh';
$dbname = 'tracker';

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die('Connection failed: ' . $conn->connect_error); // Properly concatenating the error message
} ; 
?>
