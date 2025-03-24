<?php
highlight_file(__FILE__);
// flag.php
if (isset($_POST['f'])) {
    echo hash_file('md5', $_POST['f']);
}
?>