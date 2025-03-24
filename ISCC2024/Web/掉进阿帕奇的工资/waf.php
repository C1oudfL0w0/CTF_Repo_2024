<?php

function waf($param1, $param2)
{
    $validCombinations = [
        ["%00%00", "%6c%73"],
        ["%00%00%00%01%00%00%00%00%00%00%00", "%63%61%74%21%44%6f%63%66%69%6c%65"]
    ];
    if (preg_match("/flag|system|php|cat|sort|shell|\.| |\'|\`|echo|\;|\(|\"/i", $param1) or preg_match("/flag|system|php|cat|sort|shell|\.| |\'|\`|echo|\;|\(|\"/i", $param2)) {
        return false;
    } else {
        if (strpos($param1, '%') !== false or strpos($param2, '%') !== false) {
            foreach ($validCombinations as $combination) {
                if (($param1 === $combination[0] && $param2 === $combination[1]) ||
                    ($param1 === $combination[1] && $param2 === $combination[0])
                ) {
                    return true;
                }
            }
            return false;
        }
        return true;
    }
}