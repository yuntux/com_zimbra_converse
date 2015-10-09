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
 
ConverseZimlet.prototype.init = function () {
	this._makeSpaceForConverseBar();
		converse.initialize({
			prebind: false,
			bosh_service_url: "https://192.168.1.17/http-bind",
			show_controlbox_by_default:true,
		});
};

/*
Define a proxy in your Zimbra server:
* [root@beta ~]# nano /opt/zimbra/conf/nginx/templates/nginx.conf.web.https.default.template
* before the final } add:

//Make sure NOT to use conversejs for production, as the project does not want this!!
location /http-bind {
    proxy_pass https://conversejs.org/http-bind/;

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

