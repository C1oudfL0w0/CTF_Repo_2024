/*
 * Generated by the Jasper component of Apache Tomcat
 * Version: Apache Tomcat/8.5.99
 * Generated at: 2024-03-12 11:06:53 UTC
 * Note: The last modified time of this file was set to
 *       the last modified time of the source file after
 *       generation to assist with modification tracking.
 */
package org.apache.jsp.teacher;

import javax.servlet.*;
import javax.servlet.http.*;
import javax.servlet.jsp.*;
import java.util.ArrayList;
import java.util.Base64;
import java.nio.charset.StandardCharsets;
import vo.Teacher;

public final class message_jsp extends org.apache.jasper.runtime.HttpJspBase
    implements org.apache.jasper.runtime.JspSourceDependent,
                 org.apache.jasper.runtime.JspSourceImports {

  private static final javax.servlet.jsp.JspFactory _jspxFactory =
          javax.servlet.jsp.JspFactory.getDefaultFactory();

  private static java.util.Map<java.lang.String,java.lang.Long> _jspx_dependants;

  private static final java.util.Set<java.lang.String> _jspx_imports_packages;

  private static final java.util.Set<java.lang.String> _jspx_imports_classes;

  static {
    _jspx_imports_packages = new java.util.LinkedHashSet<>(3);
    _jspx_imports_packages.add("javax.servlet");
    _jspx_imports_packages.add("javax.servlet.http");
    _jspx_imports_packages.add("javax.servlet.jsp");
    _jspx_imports_classes = new java.util.LinkedHashSet<>(4);
    _jspx_imports_classes.add("java.util.Base64");
    _jspx_imports_classes.add("vo.Teacher");
    _jspx_imports_classes.add("java.nio.charset.StandardCharsets");
    _jspx_imports_classes.add("java.util.ArrayList");
  }

  private volatile javax.el.ExpressionFactory _el_expressionfactory;
  private volatile org.apache.tomcat.InstanceManager _jsp_instancemanager;

  public java.util.Map<java.lang.String,java.lang.Long> getDependants() {
    return _jspx_dependants;
  }

  public java.util.Set<java.lang.String> getPackageImports() {
    return _jspx_imports_packages;
  }

  public java.util.Set<java.lang.String> getClassImports() {
    return _jspx_imports_classes;
  }

  public javax.el.ExpressionFactory _jsp_getExpressionFactory() {
    if (_el_expressionfactory == null) {
      synchronized (this) {
        if (_el_expressionfactory == null) {
          _el_expressionfactory = _jspxFactory.getJspApplicationContext(getServletConfig().getServletContext()).getExpressionFactory();
        }
      }
    }
    return _el_expressionfactory;
  }

  public org.apache.tomcat.InstanceManager _jsp_getInstanceManager() {
    if (_jsp_instancemanager == null) {
      synchronized (this) {
        if (_jsp_instancemanager == null) {
          _jsp_instancemanager = org.apache.jasper.runtime.InstanceManagerFactory.getInstanceManager(getServletConfig());
        }
      }
    }
    return _jsp_instancemanager;
  }

  public void _jspInit() {
  }

  public void _jspDestroy() {
  }

  public void _jspService(final javax.servlet.http.HttpServletRequest request, final javax.servlet.http.HttpServletResponse response)
      throws java.io.IOException, javax.servlet.ServletException {

    final java.lang.String _jspx_method = request.getMethod();
    if (!"GET".equals(_jspx_method) && !"POST".equals(_jspx_method) && !"HEAD".equals(_jspx_method) && !javax.servlet.DispatcherType.ERROR.equals(request.getDispatcherType())) {
      response.sendError(HttpServletResponse.SC_METHOD_NOT_ALLOWED, "JSPs only permit GET, POST or HEAD. Jasper also permits OPTIONS");
      return;
    }

    final javax.servlet.jsp.PageContext pageContext;
    javax.servlet.http.HttpSession session = null;
    final javax.servlet.ServletContext application;
    final javax.servlet.ServletConfig config;
    javax.servlet.jsp.JspWriter out = null;
    final java.lang.Object page = this;
    javax.servlet.jsp.JspWriter _jspx_out = null;
    javax.servlet.jsp.PageContext _jspx_page_context = null;


    try {
      response.setContentType("text/html;charset=UTF-8");
      pageContext = _jspxFactory.getPageContext(this, request, response,
      			null, true, 8192, true);
      _jspx_page_context = pageContext;
      application = pageContext.getServletContext();
      config = pageContext.getServletConfig();
      session = pageContext.getSession();
      out = pageContext.getOut();
      _jspx_out = out;

      out.write("\r\n");
      out.write("\r\n");
      out.write("\r\n");
      out.write("\r\n");
      out.write("\r\n");
      out.write("\r\n");
      out.write("<!DOCTYPE html>\r\n");
      out.write("<html>\r\n");
      out.write("<head>\r\n");
      out.write("    <link rel=\"stylesheet\" href=\"../resources/css/jquery-ui-1.10.4.custom.min.css\">\r\n");
      out.write("    <script src=\"../resources/js/jquery-1.10.2.js\"></script>\r\n");
      out.write("    <script src=\"../resources/js/jquery-ui-1.10.4.custom.min.js\"></script>\r\n");
      out.write("    <title>main</title>\r\n");
      out.write("    <link href=\"../resources/css/default.css\" rel=\"stylesheet\"/>\r\n");
      out.write("</head>\r\n");
      out.write("<body>\r\n");

    Teacher teacher = (Teacher) session.getAttribute("info");
    ArrayList<String> messages = (ArrayList<String>) session.getAttribute("message");

      out.write("\r\n");
      out.write("<div id=\"page\" class=\"container\">\r\n");
      out.write("    <div id=\"header\">\r\n");
      out.write("        <div id=\"logo\">\r\n");
      out.write("            <img src=\"../userImg/");
      out.print(teacher.getId());
      out.write(".jpeg\"/>\r\n");
      out.write("            <h1>");
      out.print(teacher.getId());
      out.write("\r\n");
      out.write("            </h1>\r\n");
      out.write("        </div>\r\n");
      out.write("        <div id=\"menu\">\r\n");
      out.write("            <ul>\r\n");
      out.write("                <li><a href=\"personal.jsp\">个人信息</a></li>\r\n");
      out.write("                <li class=\"current_page_item\"><a href=\"../one_page_student\">学生管理</a></li>\r\n");
      out.write("                <li><a href=\"../one_page_score\">成绩管理</a></li>\r\n");
      out.write("                <li class=\"current_page_item\"><a href=\"../select_message\">留言管理</a></li>\r\n");
      out.write("                <li><a onclick=\"return confirm('确认退出?');\" href=\"../exit\">退出登录</a></li>\r\n");
      out.write("            </ul>\r\n");
      out.write("        </div>\r\n");
      out.write("    </div>\r\n");
      out.write("    <div id=\"main\">\r\n");
      out.write("        <div class=\"table\">\r\n");
      out.write("            <table id=\"table\" width=\"800\" frame=\"box\" align=\"center\">\r\n");
      out.write("\r\n");
      out.write("                ");

                    for (String message : messages) {
                        byte[] decodedBytes = Base64.getDecoder().decode(message);
                        String decodedString = new String(decodedBytes, StandardCharsets.UTF_8);
                
      out.write("\r\n");
      out.write("                <tr>\r\n");
      out.write("                        <td height=\"35\">");
      out.print(decodedString);
      out.write("</td>\r\n");
      out.write("                </tr>\r\n");
      out.write("                ");

                    }
                
      out.write("\r\n");
      out.write("            </table>\r\n");
      out.write("        </div>\r\n");
      out.write("    </div>\r\n");
      out.write("</div>\r\n");
      out.write("\r\n");
      out.write("\r\n");
      out.write("<style>\r\n");
      out.write("    .ui-dialog-titlebar-close {\r\n");
      out.write("        display: none\r\n");
      out.write("    }\r\n");
      out.write("</style>\r\n");
      out.write("\r\n");
      out.write("<script>\r\n");
      out.write("    $('#add-dialog').dialog({\r\n");
      out.write("        width: 310,\r\n");
      out.write("        autoOpen: false,\r\n");
      out.write("        draggable: false,\r\n");
      out.write("        modal: true,\r\n");
      out.write("        resizable: false\r\n");
      out.write("    });\r\n");
      out.write("    $('.btn-add').click(function () {\r\n");
      out.write("        $('#add-dialog').dialog('open');\r\n");
      out.write("    });\r\n");
      out.write("</script>\r\n");
      out.write("</body>\r\n");
      out.write("</html>\r\n");
      out.write("\r\n");
    } catch (java.lang.Throwable t) {
      if (!(t instanceof javax.servlet.jsp.SkipPageException)){
        out = _jspx_out;
        if (out != null && out.getBufferSize() != 0)
          try {
            if (response.isCommitted()) {
              out.flush();
            } else {
              out.clearBuffer();
            }
          } catch (java.io.IOException e) {}
        if (_jspx_page_context != null) _jspx_page_context.handlePageException(t);
        else throw new ServletException(t);
      }
    } finally {
      _jspxFactory.releasePageContext(_jspx_page_context);
    }
  }
}
