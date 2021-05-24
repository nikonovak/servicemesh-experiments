Install certificate manager (https://cert-manager.io/docs/configuration/acme/dns01/google/#set-up-a-service-account, 
  https://cert-manager.io/docs/installation/kubernetes/#installing-with-helm):
```
kubectl create namespace cert-manager
helm3 repo add jetstack https://charts.jetstack.io
helm3 repo update
helm3 install \
  cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --version v1.3.1 \
  --set installCRDs=true
```

Create custom role:
....

Create service account
.....

Generate key
.....

Create secret from the key
```
kubectl create secret generic dns01-solver --from-file=key.json -n cert-manager
```

Create necessary cert-manager resources
```
k apply -f cert-manager/letsencrypt-staging.yaml
k apply -f cert/mycert.yaml
```

View logs:
```
kubectl -n cert-manager logs -f --tail 20 $(kubectl -n cert-manager get pod -l app=cert-manager -o jsonpath='{.items[0].metadata.name}')

```

View certificates:
```
kubectl get certificates
```
