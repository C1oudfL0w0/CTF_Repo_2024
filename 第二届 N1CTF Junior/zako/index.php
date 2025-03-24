<?php

//something hide here
highlight_string(shell_exec("cat ".__FILE__." | grep -v preg_match | grep -v highlight"));


$cmd = $_REQUEST["__secret.xswl.io"];
if (strlen($cmd) > 70) {
    die("no, > 70");
}
if (preg_match("/('|`|\n|\t|\\\$|~|@|#|;|&|\\||-|_|\\=|\\*|!|\\%|\\\^|index|execute)/is", $cmd)){
    die("你就不能绕一下喵");
}

system("./execute.sh '".$cmd."'");

?>