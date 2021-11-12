<?php
$value = filter_input(INPUT_POST, 'value');
if (!empty($value)){
$host = "localhost";
$dbusername = "root";
$dbpassword = "";
$dbname = "water";
// Create connection
$conn = new mysqli ($host, $dbusername, $dbpassword, $dbname);


if (mysqli_connect_error()){
die('Connect Error ('. mysqli_connect_errno() .') '
. mysqli_connect_error());
}
else{
$sql = "INSERT INTO water (value)
values ('$value')";
if ($conn->query($sql)){
echo "New record is inserted sucessfully";
}
else{
echo "Error: ". $sql ."
". $conn->error;
}
$conn->close();
}
}
else{
echo "value should not be empty";
die();
}
?>