Installing istio (https://istio.io/latest/docs/setup/install/helm/):

curl -L https://istio.io/downloadIstio | ISTIO_VERSION=1.9.2 TARGET_ARCH=x86_64 sh -
cd istio-1.9.2
kubectl create namespace istio-system
helm3 install istio-base manifests/charts/base -n istio-system
helm3 install istiod manifests/charts/istio-control/istio-discovery -n istio-system
helm3 install istio-ingress manifests/charts/gateways/istio-ingress -n istio-system
helm3 install istio-egress manifests/charts/gateways/istio-egress -n istio-system
helm3 install --namespace istio-system --set auth.strategy="anonymous" --repo https://kiali.org/helm-charts kiali-server kiali-server

install optinal prometheus and grafana
kns istio-system
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.10/samples/addons/prometheus.yaml
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.10/samples/addons/grafana.yaml

kubectl create namespace webtest-istio-flagger
kubectl create serviceaccount webtest-service-account --namespace webtest-istio-flagger

k apply -f gke-deployment-internal.yaml

kubectl label namespace webtest-istio istio-injection=enabled --overwrite

kubectl get ns -L istio-injection

kubectl get pod -l app=webtest

kubectl port-forward service/webtest 8080:8080

deploy cache
helm3 install cache bitnami/memcached

deploy app and service
k apply -f service.yaml -f gke-deployment-release1.yaml -f gke-deployment-release2.yaml -f virtualservice.yaml -f webtest-gateway.yaml -f destination-rules.yaml


Oberving traffic:
istioctl dashboard kiali


Upgrades: (https://istio.io/latest/docs/setup/upgrade/canary/)
