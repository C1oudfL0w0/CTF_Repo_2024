<?php
header('Content-Type: text/html; charset=utf-8');
highlight_file(__FILE__);

$allowedFiles = ['read.php', 'index.php'];

$ctfer = $_GET['ctfer']?? null;


if ($ctfer === null) {
    die("error 0!");
}


if (!is_numeric($ctfer)) {
    die("error 1!");
}


if ($ctfer!= 667) {
    die("error 2!");
}

//溢出
if (strpos(strval($ctfer), '7')!== false) {
    die("error 3!");
}


$file = $_GET["file"];

if ($_COOKIE['pass'] == "admin") {
    if (isset($file)) {
        // 改进的正则表达式，检查是否不存在 base|rot13|input|data|flag|file|base64 字符串
        if (preg_match("/^(?:.*(?:base|rot13|input|data|flag|file|2|5|base64|log|proc|self|env).*)$/i", $file)) {
            // 先检查文件是否在允许的列表中
            echo "prohibited prohibited!!!!";
        } else {
            echo "试试read.php";
            include($file);
        }
    }
}
?>