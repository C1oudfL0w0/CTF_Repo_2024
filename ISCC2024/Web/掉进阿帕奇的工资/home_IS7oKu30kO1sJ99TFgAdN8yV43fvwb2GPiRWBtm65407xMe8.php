<?php
error_reporting(0);
session_start();
function re_error($status,$contents){
	die("<script>alert('{$status}\\n{$contents}');history.back()</script>");
}

function show($params){
	header("Content-Type: text/json");
	die(json_encode($params));
}

$ip=$_SESSION['dep'];
if(!isset($_SESSION['user']) and "manager" !== $ip){
    die("<script>alert('认证失败\\n请先登录！');location.href='index.php'</script>");
}

// $path = '/allPe0p1e/';

// $_SESSION['money'] = @end(explode('|',file_get_contents($path.$_SESSION['user'])));


// include "./profile.php";
// ini_set('open_basedir','/var/www/html/');


?>