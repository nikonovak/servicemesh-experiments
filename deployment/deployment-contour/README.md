Description:
Demo counter app that stores current count in the memcached instance<br>
app running without service mesh just using contour

install memcached / create webtest namespace:
```
helm3 install cache bitnami/memcached -n webtest-contour --create-namespace
```

Contour: (https://github.com/bitnami/charts/tree/master/bitnami/contour, https://artifacthub.io/packages/helm/bitnami/contour)
```
helm3 repo add bitnami https://charts.bitnami.com/bitnami
helm3 repo update
helm3 install contour --namespace contour bitnami/contour --create-namespace --values contour/values.yaml
helm3 upgrade contour --namespace contour bitnami/contour --values contour/values.yaml
```

Build the container using a dockerfile:
```
docker build --tag gcr.io/ogplayground/webtest:v14 .
```

Installing the app:
```
k apply -f service-account.yaml -f gke-deployment-v1.yaml -f gke-deployment-v2.yaml -f service-v1.yaml -f service-v2.yaml -f ingress-contour.yaml
```

Test installation:
```
k port-forward svc/webtest-service-v1 8080:80
```
