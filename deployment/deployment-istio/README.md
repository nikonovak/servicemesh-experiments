kubectl create namespace istio-system
helm3 install istio-base manifests/charts/base -n istio-system
helm3 install istiod manifests/charts/istio-control/istio-discovery -n istio-system
helm3 install istio-ingress manifests/charts/gateways/istio-ingress -n istio-system
helm3 install istio-egress manifests/charts/gateways/istio-egress -n istio-system


helm3 install --namespace istio-system --set auth.strategy="anonymous" --repo https://kiali.org/helm-charts kiali-server kiali-server
istioctl dashboard kiali


kubectl create namespace webtest-istio

k apply -f deployment-istio/gke-deployment-internal.yaml

kubectl label namespace webtest-istio istio-injection=enabled --overwrite

kubectl get pod -l app=webtest

kubectl port-forward service/webtest 8080:8080
