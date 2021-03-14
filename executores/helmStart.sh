helm install calc-prometheus prometheus-community/prometheus --values ../yaml-tools/prometheus-values.yaml
helm install calc-grafana grafana/grafana --values ../yaml-tools/grafana-values.yaml
kubectl get all
pause