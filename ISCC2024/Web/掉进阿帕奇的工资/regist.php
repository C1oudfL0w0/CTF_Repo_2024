<?php
header("Content-Type: text/html; charset=utf-8");
error_reporting(0);
function re_error($status,$contents){
	die("<script>alert('{$status}\\n{$contents}');history.back()</script>");
}
// ini_set('display_errors', 1);
// error_reporting(E_ALL);
function get_uid($directory){
    // 使用 scandir() 函数列出指定目录中的所有文件和子目录
    $files = scandir($directory);

    // 初始化文件个数为 0
    $fileCount = 0;

    // 循环检查每个文件或目录
    foreach ($files as $file) {
        // 排除当前目录和上级目录
        if ($file !== '.' && $file !== '..') {
            // 使用 is_file() 函数检查是否为文件
            if (is_file($directory . $file)) {
                // 是文件则增加文件个数
                $fileCount++;
            }
        }
    }
    return $fileCount;
}

if(isset($_POST['username']) and isset($_POST['password']) and isset($_POST['repassword']) and isset($_POST['mail'])){
	
	$path = '/allPe0p1e/';

	$user = strval($_POST['username']);
	$pass = strval($_POST['password']);
	$repass = strval($_POST['repassword']);

    $job = 'tech';#strval($_POST['job']);
    $mail = strval($_POST['mail']);
    $phone = strval($_POST['phone']);
    $question = strval($_POST['question']);
    $answer = strval($_POST['answer']);
    if($answer===''){
        $question=0;
    }
    else{
        $question=(int)($question);
    }
	
	if($user == '' or $pass == '' or $repass == ''){
		re_error('错误','用户名或密码为空！');
	}
	
	if($pass !== $repass){
		re_error('错误','两次密码不相同！');
	}
	
	foreach([$user,$pass,$repass] as $v){
		if(preg_match('/[^a-zA-Z0-9]/imx',$v)){
			re_error('错误','只允许使用大小写字母以及数字！');
		}
	}
	
	if(in_array($user,scandir($path))){
		re_error('错误',"用户 < {$user} > 已存在！");
	}

    $uid = get_uid($path) + 1;

	$a = file_put_contents($path.$user,join('|',[$user,$pass,$job,$mail,$phone,$question,$answer]));

	die("<script>alert('注册成功！\\n用户名:   {$user}   \\n密码:   {$pass}   ');location.href='index.php'</script>");
}

?>