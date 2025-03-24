<?php
error_reporting(0);
// mine
// $db_host = '127.0.0.1';
// $db_username = 'root';
// $db_password = '1q2w3e4r5t!@#';
// $db_name = 'mysql';

$db_host = $_POST["db_host"];
$db_username = $_POST["db_username"];
$db_password = $_POST["db_password"];
$db_name = $_POST["db_name"];
if(isset($db_host)){
    try {
        $dsn = "mysql:host=$db_host;dbname=$db_name";
        $pdo = new PDO($dsn, $db_username, $db_password);
        $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        $_SESSION['dsn']=$dsn;
        $_SESSION['db_username']=$db_username;
        $_SESSION['db_password']=$db_password;
    } catch (Exception $e) {
       die($e->getMessage());
    }
}
if(!isset($_SESSION['dsn'])){
    die("<script>alert('请先连接数据库');window.location.href='index.php'</script>");
}
?>