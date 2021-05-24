Description:
Demo counter app that stores current count in the memcached instance<br>
app running with linkerd servicemesh

Pre-requsites:
install linkerd: (https://linkerd.io/2.10/tasks/generate-certificates/,
  https://linkerd.io/2.10/tasks/install-helm/,
  https://linkerd.io/2.10/tasks/install-helm/#helm-upgrade-procedure)
```
brew install step
mkdir certs
cd certs
exp=$(date -v+8760H +"%Y-%m-%dT%H:%M:%SZ")

step certificate create root.linkerd.cluster.local ca.crt ca.key \
--profile root-ca --no-password --insecure

step certificate create identity.linkerd.cluster.local issuer.crt issuer.key \
--profile intermediate-ca --not-after 8760h --no-password --insecure \
--ca ca.crt --ca-key ca.key
cd ..

helm3 repo add linkerd https://helm.linkerd.io/stable

helm3 repo update

k create ns linkerd

helm3 install linkerd2 linkerd/linkerd2 \
  --set-file identityTrustAnchorsPEM=certs/ca.crt \
  --set-file identity.issuer.tls.crtPEM=certs/issuer.crt \
  --set-file identity.issuer.tls.keyPEM=certs/issuer.key \
  --set identity.issuer.crtExpiry=$exp \
  --create-namespace \
  -n linkerd2 \
  --version=2.10.1 \
  -f linkerd/values-ha.yaml \
  -f linkerd/values.yaml

helm3 upgrade linkerd2 linkerd/linkerd2 \
  --set-file identityTrustAnchorsPEM=certs/ca.crt \
  --set-file identity.issuer.tls.crtPEM=certs/issuer.crt \
  --set-file identity.issuer.tls.keyPEM=certs/issuer.key \
  --set identity.issuer.crtExpiry=$exp \
  -n linkerd2 \
  --version 2.10.2 \
  -f linkerd/values-ha.yaml \
  -f linkerd/values.yaml \
  --atomic


helm3 install linerd-viz linkerd/linkerd-viz -n linkerd2
```

install memcached / create webtest namespace:
```
helm3 install cache bitnami/memcached -n webtest --create-namespace
```

install traefik:
```
helm3 install router traefik/traefik --version=9.19.0 --namespace kube-system --values traefik/values.yaml
```
traefik can be upgraded using:
```
helm3 upgrade router traefik/traefik --version=9.19.0 --namespace kube-system --values traefik/values.yaml
```

Build the container using a dockerfile:
```
docker build --tag gcr.io/ogplayground/webtest:v14 .
```

Installing the app:
```
k apply -f gke-deployment-linkerd-v1.yaml -f gke-deployment-linkerd-v2.yaml -f ingress.yaml -f service-v1.yaml -f service-v2.yaml -f service.yaml -f traffic-split.yaml
```

Test installation:
```
k port-forward svc/webtest-service-v1 8080:80
```

Patch all deployments to use linkerd mesh add annotation to all pods:
```
linkerd.io/inject: enabled
```

Add an annotation to the ingress controller:
```
linkerd.io/inject: ingress
```

Ambassador:
```
helm3 repo add datawire https://www.getambassador.io
helm3 repo update
helm3 install ambassador --namespace ambassador datawire/ambassador --create-namespace --values ambassador/values.yaml
helm3 upgrade ambassador --namespace ambassador datawire/ambassador --values ambassador/values.yaml

Contour: (https://github.com/bitnami/charts/tree/master/bitnami/contour, https://artifacthub.io/packages/helm/bitnami/contour)
helm3 repo add bitnami https://charts.bitnami.com/bitnami
helm3 repo update
helm3 install contour --namespace contour bitnami/contour --create-namespace --values contour/values.yaml
helm3 upgrade contour --namespace contour bitnami/contour --create-namespace --values contour/values.yaml

helm3 upgrade contour --namespace contour ~/github/charts/bitnami/contour --values contour/values.yaml
(for now use local copy of the contour helm chart - it includes missing annotations)
