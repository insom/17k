# 17k
17k.uk's Scrup service.

HTTP proxy :443 to :6525:


    <VirtualHost *:80>
     ServerName 17k.co.uk
     ServerAlias 17k.uk
     ProxyPreserveHost On
     ProxyPass / http://127.0.0.1:6525/
     ProxyPassReverse / http://127.0.0.1:6525/
    </VirtualHost>

----

&copy; 2013-2016 Aaron Brady
