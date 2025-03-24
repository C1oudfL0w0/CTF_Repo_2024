<?php
error_reporting(0);
session_start();
$ip=$_SESSION['dep'];
if(!isset($_SESSION['user']) and "manager" !== $ip){
    die("<script>alert('认证失败\\n请先登录！');location.href='index.php'</script>");
}
function re_error($status,$contents){
	die("<script>alert('{$status}\\n{$contents}');history.back()</script>");
}
?>