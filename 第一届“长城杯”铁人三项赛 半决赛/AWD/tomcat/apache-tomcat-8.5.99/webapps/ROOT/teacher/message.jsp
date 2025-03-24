<%@ page import="java.util.ArrayList" %>
<%@ page import="java.util.Base64" %>
<%@ page import="java.nio.charset.StandardCharsets" %>
<%@ page import="vo.Teacher" %>

<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="../resources/css/jquery-ui-1.10.4.custom.min.css">
    <script src="../resources/js/jquery-1.10.2.js"></script>
    <script src="../resources/js/jquery-ui-1.10.4.custom.min.js"></script>
    <title>main</title>
    <link href="../resources/css/default.css" rel="stylesheet"/>
</head>
<body>
<%
    Teacher teacher = (Teacher) session.getAttribute("info");
    ArrayList<String> messages = (ArrayList<String>) session.getAttribute("message");
%>
<div id="page" class="container">
    <div id="header">
        <div id="logo">
            <img src="../userImg/<%=teacher.getId()%>.jpeg"/>
            <h1><%=teacher.getId()%>
            </h1>
        </div>
        <div id="menu">
            <ul>
                <li><a href="personal.jsp">个人信息</a></li>
                <li class="current_page_item"><a href="../one_page_student">学生管理</a></li>
                <li><a href="../one_page_score">成绩管理</a></li>
                <li class="current_page_item"><a href="../select_message">留言管理</a></li>
                <li><a onclick="return confirm('确认退出?');" href="../exit">退出登录</a></li>
            </ul>
        </div>
    </div>
    <div id="main">
        <div class="table">
            <table id="table" width="800" frame="box" align="center">

                <%
                    for (String message : messages) {
                        byte[] decodedBytes = Base64.getDecoder().decode(message);
                        String decodedString = new String(decodedBytes, StandardCharsets.UTF_8);
                %>
                <tr>
                        <td height="35"><%=decodedString%></td>
                </tr>
                <%
                    }
                %>
            </table>
        </div>
    </div>
</div>


<style>
    .ui-dialog-titlebar-close {
        display: none
    }
</style>

<script>
    $('#add-dialog').dialog({
        width: 310,
        autoOpen: false,
        draggable: false,
        modal: true,
        resizable: false
    });
    $('.btn-add').click(function () {
        $('#add-dialog').dialog('open');
    });
</script>
</body>
</html>

