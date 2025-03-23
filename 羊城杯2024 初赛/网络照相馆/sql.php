<?php
$servername = "localhost";
$username = "ctfer";
$password = "ctfer";

// 创建连接
$conn = new mysqli($servername, $username, $password,"data");

// 检测连接
if ($conn->connect_error) {
    die("连接失败: " . $conn->connect_error);
}

?>