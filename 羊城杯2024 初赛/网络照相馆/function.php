<?php

function curl($url){
    $curl = curl_init();
    curl_setopt($curl, CURLOPT_URL, $url);
    curl_setopt($curl, CURLOPT_HEADER, 0);
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1);
    $tmpInfo = curl_exec($curl);
    curl_close($curl);
    return $tmpInfo; 
}

function get_filename($len){
    $chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
    $var_size = strlen($chars);
    $res = '';
    for( $x = 0; $x < $len; $x++ ) {
        $random_str= $chars[ rand( 0, $var_size - 1 ) ];
        $res .= $random_str;
    }
    $res = date("Y-m-d"). '_' . $res . '.txt';
    return $res;
}

function check($conn , $filename, $url){
    $sql = "SELECT filename from data where url = '$url'";
    $result = $conn->query($sql);
    if ($result) {
        $row = mysqli_fetch_all($result);
        foreach ( $row as $value){
            if( hash_file('md5', $filename) === hash_file('md5', $value[0])){
                return false;
            }
        }
    }
    return true;
}

// $filenames = [];
// for ($i = 0; $i < 5000; $i++) {
//     $filenames[] = get_filename(8);
// }

// $file = fopen("filenames.txt", "w");
// foreach ($filenames as $filename) {
//     fwrite($file, $filename . "\n");
// }
// fclose($file);
