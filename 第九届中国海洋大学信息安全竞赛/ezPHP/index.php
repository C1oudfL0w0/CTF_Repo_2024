<?php
include "flag.php";
highlight_file(__FILE__);
error_reporting(0);

$a = 'O.U.C';

$query = $_SERVER['QUERY_STRING'];
parse_str($query);
if (preg_match('/_|%5f|\.|%2E/i',$query)){
    die('听说你是黑客');
}

echo '你知道b等于什么能绕过这个弱类型吗（〃｀ 3′〃）'.'<br>';
if (md5($a)==md5($_GET['b'])&&$a!=$_GET['b']){
    echo "哎呦，不错喔".'<br>';
    $O_U_C=$_GET['O_U_C'];
    if (!is_array($O_U_C)&&$O_U_C!=='100'&&preg_match('/^100$/',$O_U_C)){
        echo 'but'.'如果我寄出===阁下又该如何应对๑乛◡乛๑'.'<br>';
        if (md5($_POST['md51'])===md5($_POST['md52'])&&$_POST['md51']!=$_POST['md52']){
            echo '好，那么好'.'<br>';
            if ($_COOKIE["md5"]===md5($secret.urldecode($_GET['md5']))){
                echo '还是被你解出来了'.' ྀི ྀིɞ ྀི ིྀ ིྀ'.$flag;
            }else{
                echo '告诉你secret的md5值也无妨，反正哈希是不可逆的๑乛◡乛๑，除非你能箨斩攻击我'.md5($secret.'ouc').'<br>';
            }
        }else{
            echo '不过如此';
        }
    }else{
        die("不行嘛(´ｪ｀)");
    }
}else{
    echo '嗨害嗨  (๑ᵒ̴̶̷͈᷄ᗨᵒ̴̶̷͈᷅)';
} 