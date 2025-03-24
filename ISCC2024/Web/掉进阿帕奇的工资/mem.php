<?php
// error_reporting(0);
// session_start();
// $ip=$_SESSION['dep'];
// if(!isset($_SESSION['user']) and "manager" !== $ip){
//     die("<script>alert('认证失败\\n请先登录！');location.href='index.php'</script>");
// }
// function re_error($status,$contents){
// 	die("<script>alert('{$status}\\n{$contents}');history.back()</script>");
// }
namespace MyNamespace;
class XorCalculator
{
    public static function calculate($a, $b)
    {
        $a =urldecode($a);
        $b =urldecode($b);
        if (ctype_digit($a) && ctype_digit($b)) {
        // 如果是，转换为整型后计算
            return (int)$a ^ (int)$b;
        }
        else{
            return $a ^ $b;
        }
        // return  ^ urldecode($b);
    }
}