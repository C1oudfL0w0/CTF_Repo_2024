<?php
header("Content-Type: text/html; charset=utf-8");
error_reporting(0);
function re_error($status, $contents)
{
    die("<script>alert('{$status}\\n{$contents}');history.back()</script>");
}
// 引入随机密码生成函数
function generateRandomPassword($length = 30)
{
    $characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
    $password = '';
    for ($i = 0; $i < $length; $i++) {
        $password .= $characters[rand(0, strlen($characters) - 1)];
    }
    return $password;
}
function get_uid($directory)
{
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
if (isset($_POST['recovery-method'])) {
    $choice = strval($_POST['recovery-method']);
    $path = '/allPe0p1e/';

    if ($choice === "0") {
        $user = strval($_POST['username']);
        $pass = strval($_POST['mail']);

        if ($user == '' or $pass == '') {
            re_error('错误', '用户名或邮箱为空！');
        }

        $info = explode('|', file_get_contents($path . $user));
        if ($info[0] === $user and $info[3] === $pass) {
            if ($info[2] == "tech") {
                $newPassword = generateRandomPassword();
                $a = file_put_contents($path . $user, join('|', [$user, $newPassword, $info[2], $info[3], $info[4], $info[5], $info[6]]));
                die("<script>alert('\\经回溯您的身份不是manager\\n已为您重置基本密码信息！\\n用户名:   {$user}   \\n密码:   {$newPassword}   \\n加油吧,你还是你:   打工人！   ');location.href='index.php'</script>");
            } else {
                die("<script>alert('尊贵的manager用户，您的信息重置成功！\\n用户名:   {$user}   \\n当前身份:   {$info[2]}   ');location.href='index.php'</script>");
            }
        } else {
            re_error('错误', '身份验证信息错误！');
        }
    } elseif ($choice === "1") {
        $user = strval($_POST['username']);
        $question = $_POST['question'];
        $answer = strval($_POST['answer']);
        if ($user == '') {
            re_error('错误', '用户名为空！');
        }

        if (!isset($question)) {
            $question = '58646083598550771719223304263172';
        }
        if (empty($answer)) $answer = '';

        $info = explode('|', file_get_contents($path . $user));
        if ($info[0] === $user and $question == (int)$info[5] and $info[6] === $answer) {
            if ($info[2] == "tech") {
                if ($question === '0') {
                    $newPassword = generateRandomPassword();
                    $a = file_put_contents($path . $user, join('|', [$user, $newPassword, $info[2], $info[3], $info[4], $info[5], $info[6]]));
                    die("<script>alert('\\经回溯您的身份类型太弱不是manager\\n已为您重置基本密码信息！\\n用户名:   {$user}   \\n密码:   {$newPassword}   \\n加油吧,你还是你:   打工人！   ');location.href='index.php'</script>");
                } else {
                    // 使用随机密码生成函数
                    $newPassword = generateRandomPassword();
                    $a = file_put_contents($path . $user, join('|', [$user, $newPassword, 'manager', $info[3], $info[4], $info[5], $info[6]]));
                    die("<script>alert('尊贵的manager用户，您的信息重置成功！\\n用户名:   {$user}   \\n密码:   {$newPassword}   \\n当前身份:      manager!   ');location.href='index.php'</script>");
                }
            } else {
                die("<script>alert('尊贵的manager用户，您的信息重置成功！\\n用户名:   {$user}   \\n当前身份:   {$info[2]}   ');location.href='index.php'</script>");
            }
        } else if ($info[0] === $user and strval($question) == $info[5] and $info[6] === $answer) {
            // 使用随机密码生成函数
            $newPassword = generateRandomPassword();
            $a = file_put_contents($path . $user, join('|', [$user, $newPassword, $info[2], $info[3], $info[4], $info[5], $info[6]]));
            die("<script>alert('\\经回溯您的身份类型太弱不是manager\\n已为您重置基本密码信息！\\n用户名:   {$user}   \\n密码:   {$newPassword}   \\n加油吧,你还是你:   打工人！   ');location.href='index.php'</script>");
        } else {
            re_error('错误', "身份验证信息错误!");
        }
    }
}