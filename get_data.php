<?php
ini_set('display_errors', 1);
error_reporting(E_ALL);

include 'db_connection.php' ; 
$sql = 'SELECT Date, Formula FROM notion_data ORDER BY Date'; 
$result = $conn->query($sql) ;

$data = [] ; 
while ($row = $result->fetch_assoc()){
    $data[] = $row ; 
}

header('Content-Type: application/json') ; 
echo json_encode($data)  ; 

// close connection 
$conn->close() ; 
exit ; 
?>