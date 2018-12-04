# databricks-cluster-recreate

Creates snapshots of a set of clusters' configuration and libraries from the REST API, and scripts to recreate the clusters.

Where's my cluster gone? These scripts aim to address the next question: how do I recreate my cluster? 

## Setup

See: [https://github.com/databricks/databricks-cli](https://github.com/databricks/databricks-cli)
```
pip install --upgrade databricks-cli
```

## Overview

The databricks-cluster-recreate scripts:
* create a directory for each cluster that matches the search criteria with the necessary JSON request files.
* Convenience shell scripts to recreate the cluster and attach its libraries. 
* The scripts use the databricks CLI.

Files in a [cluster directory](example):
* [create_cluster.sh](example/create_cluster.sh) - script using databricks CLI to create the cluster
* [cluster.json](example/cluster.json) - JSON spec used to create the cluster. Request for [clusters/create API endpoint](https://docs.databricks.com/api/latest/clusters.html#create).
* [install_libraries.sh](example/install_libraries.sh) - script using databricks CLI to attach all libraries
* [libraries.json](example/libraries.json) - Input libraries to HTTP API call (not used by install_libraries.sh)
* [from_api](example/from_api) - Original output from API get calls
  * [cluster.json](example/from_api/cluster.json) - response from [clusters/get endpoint](https://docs.databricks.com/api/latest/clusters.html#get).
  * [libraries.json](example/from_api/libraries.json) - libraries/cluster-status endpoint
response from [libraries/cluster-status endpoint](https://docs.databricks.com/api/latest/libraries.html#cluster-status).

The option `use_cluster_id` determines whether directory names are cluster IDs or cluster names. The default is to use cluster names.

Since cluster names are not unique, when duplicate names occur the resulting directory name will have `__dup_{COUNT}` appended to it. For example, `cool_cluster__dup_01` and `cool_cluster__dup_02`.


Note, that although you can apparently pass the response from cluster/get to cluster/create, the databricks-cluster-recreate databricks-cluster-recreate script extract only those fields that are required by cluster/create from the much more verbose cluster/get payload.

**Recreate Scripts**

[create_cluster.sh](example/create_cluster.sh):
```
databricks clusters create --json-file cluster.json
```

[install_libraries.sh](example/install_libraries.sh)
```
if [ $# -eq 0 ] ; then
  echo ERROR: Missing CLUSTER_ID
  exit 1
  fi
cluster_id=$1

databricks libraries install --cluster-id $cluster_id --maven-coordinates org.mlflow:mlflow-client:0.8.0
databricks libraries install --cluster-id $cluster_id --pypi-package mlflow
databricks libraries install --cluster-id $cluster_id --maven-coordinates ml.combust.mleap:mleap-spark_2.11:0.12.0
databricks libraries install --cluster-id $cluster_id --maven-coordinates ml.combust.mleap:mleap-spark-base_2.11:0.12.0
```

## Sample runs

By cluster IDs (comma-separated cluster IDs):
```
python cluster_snapshot_by_ids.py \
  --cluster_ids 1125-205205-racer181,1023-023159-prop147  \
  --output_dir out \
  --profile MY_PROFILE
```

By user (i.e. creator_user_name):
```
python cluster_snapshot_by_user.py \
  --user doe@databricks.com \
  --output_dir out \
  --profile MY_PROFILE
```

All clusters:
```
python cluster_snapshot_all.py \
  --output_dir out \
  --profile MY_PROFILE
```
