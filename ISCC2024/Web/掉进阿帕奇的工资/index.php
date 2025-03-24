<?php
header("Content-Type: text/html; charset=utf-8");
error_reporting(0);
session_start();
function re_error($status,$contents){
	die("<script>alert('{$status}\\n{$contents}');history.back()</script>");
}
function show_homepage(){
    if ($_SESSION["dep"]==='manager'){
        die("<script>alert('登录成功');location.href='home_IS7oKu30kO1sJ99TFgAdN8yV43fvwb2GPiRWBtm65407xMe8.php'</script>");
    }
    else{
    	$x = $_SESSION["dep"];
        die("<script>alert('Hey $x, how dare you try！🤯');location.href='normal.php'</script>");
    }
}

if(isset($_POST['username']) and isset($_POST['password']) ){#and isset($_POST['deppartm'])
	
	$path = '/allPe0p1e/';
	
	$user = strval($_POST['username']);
	$pass = strval($_POST['password']);
	// $dep = strval($_POST['deppartm']);
	
	if($user == '' or $pass == ''){
		re_error('错误','用户名或密码或部门为空！');
	}
	$info = explode('|',file_get_contents($path.$user));
    $dep = $info[2];
    if($dep === 'tech'){//临时便捷入口
        re_error('说明','Technology Department seems to be an internal employee, but today is a blacklist candidate 😀');
    }else{
	   	if(!in_array($user,scandir($path))){
			re_error('错误',"用户 < {$user} > 不存在！");
		}
		if($info[1] === $pass){
			$info = array('deppartm'=>$dep,'username'=>$user,'password'=>$pass);

		    $_SESSION['user'] = $info['username'];
		    $_SESSION['pass'] = $info['password'];
		    $_SESSION['dep'] = $dep;
			$_SESSION['level'] = $info['level'];
        	show_homepage();
		}else{
			re_error('错误','用户名或密码错误！');
		}
    }
}

?>