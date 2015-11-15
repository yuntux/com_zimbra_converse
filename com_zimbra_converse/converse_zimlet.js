function com_zimbra_converse_HandlerObject() {


   
}
com_zimbra_converse_HandlerObject.prototype = new ZmZimletBase();
com_zimbra_converse_HandlerObject.prototype.constructor = com_zimbra_converse_HandlerObject;

/**
 * Simplify handler object
 *
 */
var ConverseZimlet = com_zimbra_converse_HandlerObject;

/**
 * Initializes the Zimlet.
 */
 
/*bosh_service_url points to your Zimbra server!
 * */ 

ConverseZimlet.prototype.getCookie= function() {
        var jspUrl = this.getResource("get_cookie.jsp");
        var response = AjxRpc.invoke(null, jspUrl, null, null, true);
        var authtoken = response.text;
        return authtoken;
};


ConverseZimlet.prototype.init = function () {
        //http://community.zimbra.com/collaboration/f/1893/t/1120603
        var username = this.getUsername();
        var auth_token = this.getCookie();
        this._makeSpaceForConverseBar();
                converse.initialize({
                        auto_login:true,
                        jid:username,
                        password:"zimbra_auth_token++"+auth_token,
                        prebind: false,
                        //Be sure it's httpS because we send the ZM_AUTH_TOKEN !
                        bosh_service_url: "https://mailt.fontaineconsultants.net/http-bind",
                        show_controlbox_by_default:true,
                });
};

/*
Define a proxy in your Zimbra server:
* [root@beta ~]# nano /opt/zimbra/conf/nginx/templates/nginx.conf.web.https.default.template
* before the final } add:

//Be sure httpS binding and XMPP lisetner are encrypted in production !
location /http-bind {
    proxy_pass http://mailt.fontaineconsultants.net:5280/http-bind/;

}

*/

/**
 * Makes a div for converse in the skin
 */
ConverseZimlet.prototype._makeSpaceForConverseBar =
function () {
	var newDiv = document.getElementById("z_shell").appendChild(document.createElement('div'));
	newDiv.style.display = "block";
	newDiv.style.zIndex = 9000;
	newDiv.id = "conversejs";
	appCtxt.getAppViewMgr().fitAll();
};

