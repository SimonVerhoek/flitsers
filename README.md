# FLITSERDATA.NL

## Development
As the Docker database wants to retrieve data from the remote database, set up a tunnel to your local machine:
```shell
ssh <server-name> -L <db_port:host_ip:db_port> -N
```
Now, you can run the Docker Compose setup. After initialization, you can close the tunnel.
  
For development, you can leave out the `cronjobs` service. 


## Refresh SSL certificate
On the server, run `$ certbot`
