# THIS IS A PROOF OF CONCEPT - NOT FOR PRODUCTION

Lots of people want this? Then development continues, or it will die slowly again

    Get another proxy on your zimbra server:
    Define a proxy in your Zimbra server:
    * [root@beta ~]# nano /opt/zimbra/conf/nginx/templates/nginx.conf.web.https.default.template
    * before the final } add:
    //Make sure NOT to use conversejs.org for production, as the project does not want this!!
    location /http-bind {
    proxy_pass https://conversejs.org/http-bind/;
    su zimbra
    zmproxyctl restart
    
Copy paste the https://github.com/barrydegraaff/com_zimbra_converse/tree/master/com_zimbra_converse to /opt/zimbra/zimlets-deployed/_dev/com_zimbra_converse

And configure your server in:

    /opt/zimbra/zimlets-deployed/_dev/com_zimbra_converse/converse_zimlet.js
    
Like this, shoot me a comment info@barrydegraaff.tk
