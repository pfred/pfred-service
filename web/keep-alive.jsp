<%@ page language="java" import="java.util.*" pageEncoding="ISO-8859-1"%>

<%
        String path = request.getContextPath();
        String basePath = request.getScheme() + "://" + request.getServerName() + ":" + request.getServerPort() + path + "/";
%>

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
    <head>
        <base href="<%=basePath%>">

        <title>PFRED Service Keep-alive Page</title>
        <meta http-equiv="pragma" content="no-cache">
        <meta http-equiv="cache-control" content="no-cache">
        <meta http-equiv="expires" content="0">
    </head>

    <body>
        This is the PFRED XFire Web Service keep-alive page.
        <br>
        <table>
            <tr><td>Server Info</td><td><%=basePath%></td></tr>
            <tr><td>Version Number</td><td>1.0</td></tr>
            <tr><td>Release Date</td><td>June 20, 2011</td></tr>
        </table>
        <p><a href="<%=basePath%>services/PFREDService?wsdl">View WSDL</a></p>
    </body>
</html>
