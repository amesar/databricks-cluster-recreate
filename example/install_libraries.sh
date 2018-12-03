
# Install libraries for cluster doe_mlflow

if [ $# -eq 0 ] ; then
  echo ERROR: Missing CLUSTER_ID
  exit 1
  fi
cluster_id=$1

databricks libraries install --cluster-id $cluster_id --maven-coordinates org.mlflow:mlflow-client:0.8.0
databricks libraries install --cluster-id $cluster_id --pypi-package mlflow
databricks libraries install --cluster-id $cluster_id --maven-coordinates ml.combust.mleap:mleap-spark_2.11:0.12.0
databricks libraries install --cluster-id $cluster_id --maven-coordinates ml.combust.mleap:mleap-spark-base_2.11:0.12.0
