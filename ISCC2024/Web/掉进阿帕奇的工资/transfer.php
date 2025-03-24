<?php
// 构造基础URL
$base_url = "http://localhost/proxy_iIHcSmaXGmPDeuc3XnkXW5uVSx8yEN";
// 获取当前URL中的所有GET参数，并构造查询字符串
$query_string = '';
if (isset($_GET['dashachun']) && !empty($_GET['dashachun'])) {
    // 获取参数'dashachun'的值
    $dashachun = $_GET['dashachun'];
    // 输出获取的值
    $query_string = $dashachun;
}
// echo "<script>alert($query_string)</script>";

// 如果存在查询字符串，则将其附加到基础URL后面
$url = $base_url . '?' . $query_string;
$options = ["http" => ["ignore_errors" => true]];
$context = stream_context_create($options);
$response = @get_headers($url, 1, $context);
if ($response !== false) {
    $status_line = $response[0];  // 类似于 'HTTP/1.1 200 OK' 或 'HTTP/1.1 500 Internal Server Error'
    preg_match('{HTTP\/\S*\s(\d{3})}', $status_line, $match);
    $status = $match[1];
    if ($status === "500") {
        // 输出自定义500错误页面的内容
        echo '<div>
                            <!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN"> <html><head> 
                            <title>500 Internal Server Error</title> </head><body> 
                            <h1>Internal Server Error</h1> <p>
                            The server encountered an internal error or misconfiguration and was unable to complete your request for secret host.</p> 
                            <p>Please contact the server administrator at ISCC_Happy_Webmaster@iscc.club to inform them of the time this error occurred, and the actions you performed just before this error.</p> 
                            <p>More information about this error may be available in the server error log.</p> </body></html>
                            </div>';
    } else {
        // 如果状态码不是500，那么尝试输出内容
        $content = file_get_contents($url, false, $context);
        if ($content !== false) {
            // 安全地输出内容
            echo "<div>" . $content . "</div>";
        } else {
            // 如果获取内容失败，显示错误信息
            echo "<div>无法获取内容。</div>";
        }
    }
} else {
    // 如果连头信息都无法获取，显示无法连接服务器的错误信息
    echo "<div>无法连接到服务器。</div>";
}
// if ($content !== false) {
//     // 安全地输出内容
//     echo "<div>" . ($content) . "</div>";
// } 
// else {
//     // 如果获取内容失败，显示错误信息
//     echo "<div>无法获取内容。</div>";
// }
?>