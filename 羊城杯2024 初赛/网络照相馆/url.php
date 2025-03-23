<?php
//error_reporting(0);
include_once 'function.php';
include_once 'sql.php';

$baseDir = "data/";

if(isset($_POST['url']))
{
    $url = $_POST['url'];
    $parse = parse_url($url);
    if(!isset($parse['host']))
    {
        die("url错误！");
    }
    $data = curl($url);
    $filename = $baseDir .  get_filename(8);
    file_put_contents($filename , $data);
    if (check($conn, $filename, $url)){
        file_put_contents($filename , $data);
        $sql = "INSERT INTO `data`(`url`,`filename`) VALUES (?, ?)";
        if($stmt = mysqli_prepare($conn, $sql)){
            mysqli_stmt_bind_param($stmt, "ss", $url, $filename);
            mysqli_stmt_execute($stmt);
        }
    }
    else{
        unlink($filename);
    }
    echo $data;
}
?>