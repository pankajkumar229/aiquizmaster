# aiquizmaster

BUILD
=====
Go to ui directory build the Dockerfile
Do to backend directory build the Dockerfile


Deployment
==========
Create a GKE cluster and point to it
Deploy nginx ingress 
   helm install my-release oci://ghcr.io/nginxinc/charts/nginx-ingress --version 0.17.1
   (higher version of helm required)
Create TLS(Instructions to generate cert here: https://github.com/datacabinet/product/tree/master/cicd/service_deployer/computerlab/keys/certs) 
   kubectl create secret tls aiquizmaster-cert -n dc-core --key privkey.pem --cert fullchain.pem --dry-run -o yaml | kubectl apply -f -

Update tags in fulldeployment.yaml for Dockerfile in case of new images
kubectl apply -f fulldeployment.yaml
