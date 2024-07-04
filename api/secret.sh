kubectl create secret generic db-credentials -n NAMESPACE  \
  --from-literal=DB_USER= \
  --from-literal=DB_PASSWORD= \
  --from-literal=DB_NAME= \
  --from-literal=DB_HOST= "private ip"
