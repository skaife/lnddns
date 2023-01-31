# lnddns
Dynamic DNS application for use with Linode.


This makes a call to the https://api.ipify.org service to get the current public IP address of the machine it is running on.  It then connects to Linodes name server and updates the configured A document to reflect the current public IP.  As multiple servers can be entered into the .conf file to update multiple DNS entries.  This application would ideally be set as a service that triggers on a schedule to automatically keep the dns server up to date.
