<%@ page language="java" contentType="text/html; charset=UTF-8" import="
javax.servlet.http.Cookie,
java.io.PrintWriter
" %>
<%
Cookie cookies[] = request.getCookies();
String authTokenStr = "";
if(cookies != null) {
        int i = 0;
        do
        {
                if(i >= cookies.length)
                break;
                if(cookies[i].getName().equals("ZM_AUTH_TOKEN"))
                {
                        authTokenStr = cookies[i].getValue();
                        break;
                }
                        i++;
        }
        while(true);
}
PrintWriter pw = response.getWriter();
pw.print(authTokenStr);
pw.flush();
pw.close();
%>
