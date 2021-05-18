Description:
Demo counter app that stores current count in the memcached instance

Pre-requsites:
install memcached / create webtest namespace
```
helm3 install cache bitnami/memcached -n webtest --create-namespace
```

Build the container using a dockerfile:
```
docker build --tag gcr.io/ogplayground/webtest:v14 .
```

Installing the app:
```
k apply -f gke-deployment-internal.yaml -f service.yaml
```

Test installation:
```
k port-forward svc/webtest-service 8080:80
```
