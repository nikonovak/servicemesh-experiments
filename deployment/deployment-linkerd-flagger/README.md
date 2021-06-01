kubectl create namespace webtest-istio-linkerd
kubectl create serviceaccount webtest-service-account --namespace webtest-istio-linkerd

kubectl annotate namespace webtest-linkerd-flagger linkerd.io/inject=enabled

helm3 install cache bitnami/memcached




