<?php
show_source(__FILE__);
error_reporting(0);
if (!empty($_GET['ISCC'])) {
    $str = strtolower($_GET['ISCC']);
    $blacklist = array("more", "tac",  "fopen", "cat", "file_get_contents", "file", "readfile", "SplFileObject");
    $sp_point = "iscc";
    $$sp_point = "/hint";
    foreach ($blacklist as $value) {
        if (strpos($str, $value) || preg_match('/\bexec|\bpopen|\bstrrev|\bgetallheaders|\bescapeshellcmd|\bassert|\bpassthru|\bshell_exec|\bbin2hex| \bescapeshellarg|\bpcntl_exec|\busort|\bsystem|\bflag\.txt|\bsp_point|\brequire|\bscandir|\binclude|\bhex2bin|\$[a-zA-Z]|[#!%^&*_+=\-,\.:`|<>?~\\\\]/i', $str)) {
            $str = ""; 
            break;
        }
    }
    eval($str . ";");
}
?>
<html>
<body>
<!-- base64 url md5 ? rot13 reverse base64 ?-->
</body>
</html> 