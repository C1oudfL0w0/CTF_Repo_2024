<?php
require 'waf.php';
require 'mem.php';

use MyNamespace\XorCalculator;

if (isset($_POST['calculate'])) {
    $basicSalary = $_POST['basicSalary'];
    $performanceCoefficient = $_POST['performanceCoefficient'];
    if (waf($basicSalary, $performanceCoefficient)) {
        $cmd = XorCalculator::calculate($basicSalary, $performanceCoefficient);
        echo $cmd;
        if (is_string($cmd)) {
            ob_start(); // 开始输出缓冲
            system($cmd); // 执行$cmd中的代码
            $output = ob_get_clean(); // 获取输出缓冲区的内容，并清除缓冲区
            echo $output;
        }
    } else {
        // 参数包含禁止的字符，可能是恶意的输入
        echo "检测到非法字符！";
    }
} else {
    echo "预测可能结果";
}