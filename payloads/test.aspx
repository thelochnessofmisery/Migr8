<%@ Page Language="C#" %>
<!--
Migr8 Test ASPX Payload
Harmless reconnaissance payload for upload testing
-->
<!DOCTYPE html>
<html>
<head>
    <title>ASPX Upload Test</title>
</head>
<body>
    <h2>ASPX Upload Test Successful</h2>

    <script runat="server">
        void Page_Load(object sender, EventArgs e)
        {
            lblServerInfo.Text = Request.ServerVariables["SERVER_SOFTWARE"];
            lblFramework.Text = Environment.Version.ToString();
            lblCurrentTime.Text = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss");
            lblDirectory.Text = Server.MapPath(".");
            lblOS.Text = Environment.OSVersion.ToString();
        }
    </script>

    <p>Server: <asp:Label ID="lblServerInfo" runat="server" /></p>
    <p>.NET Framework: <asp:Label ID="lblFramework" runat="server" /></p>
    <p>Current Time: <asp:Label ID="lblCurrentTime" runat="server" /></p>
    <p>Upload Directory: <asp:Label ID="lblDirectory" runat="server" /></p>
    <p>Operating System: <asp:Label ID="lblOS" runat="server" /></p>

    <!-- Migr8 ASPX Test Payload -->
</body>
</html>
