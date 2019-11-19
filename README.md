# databricks-cluster-recreate

Where's my cluster gone? These scripts address the problem: how do I recreate my cluster? 

Creates snapshots of a set of clusters configurations and their libraries. Using the Databricks REST API generates scripts to recreate the clusters.

## Setup

Scripts use the Databricks CLI and its configuration.
See: [https://github.com/databricks/databricks-cli](https://github.com/databricks/databricks-cli).
```
pip install --upgrade databricks-cli
```

## Overview

The databricks-cluster-recreate scripts:
* Creates a directory for each cluster that matches the search criteria.
* JSON spec files to create cluster and attach libraries.
* Convenience shell scripts to recreate the cluster and attach its libraries. 
* The scripts use the databricks CLI.

Files in a [cluster directory](example):
* [create_cluster.sh](example/create_cluster.sh) - script using databricks CLI to create the cluster
* [cluster.json](example/cluster.json) - JSON spec used to create the cluster. Request for [clusters/create API endpoint](https://docs.databricks.com/api/latest/clusters.html#create).
* [install_libraries.sh](example/install_libraries.sh) - script using databricks CLI to attach all libraries
* [libraries.json](example/libraries.json) - Input libraries to HTTP API call (not used by install_libraries.sh)
* [from_api](example/from_api) - Original output from API get calls
  * [cluster.json](example/from_api/cluster.json) - response from [clusters/get](https://docs.databricks.com/api/latest/clusters.html#get) endpoint.
  * [libraries.json](example/from_api/libraries.json) - response from [libraries/cluster-status](https://docs.databricks.com/api/latest/libraries.html#cluster-status) endpoint.

The option `use_cluster_id` determines whether directory names are cluster IDs or cluster names. The default is to use cluster names.

Since cluster names are not unique, when duplicate names occur the resulting directory name will have `__dup_{COUNT}` appended to it. For example, `cool_cluster__dup_01` and `cool_cluster__dup_02`.


Note, that although you can apparently pass the response from cluster/get to cluster/create, the databricks-cluster-recreate databricks-cluster-recreate script extracts only those fields that are required by cluster/create from the much more verbose cluster/get payload.

**Recreate Scripts**

[create_cluster.sh](example/create_cluster.sh):
```
if [ $# -gt 0 ] ; then
  PROFILE="--profile $1"
fi
databricks clusters create --json-file cluster.json $PROFILE
```

[install_libraries.sh](example/install_libraries.sh)
```
if [ $# -eq 0 ] ; then
  echo ERROR: Missing CLUSTER_ID
  exit 1
  fi
cluster_id=$1
if [ $# -gt 1 ] ; then
  PROFILE="--profile $2"
fi

databricks libraries install --cluster-id $cluster_id --pypi-package mlflow $PROFILE
databricks libraries install --cluster-id $cluster_id --maven-coordinates org.mlflow:mlflow-client:1.3.0 $PROFILE
databricks libraries install --cluster-id $cluster_id --maven-coordinates ml.combust.mleap:mleap-spark_2.11:0.12.0 $PROFILE
```

## Generate cluster recreate scripts

There are three different ways to create recreate scripts. `By user` is the most common one.

By user (i.e. `creator_user_name` JSON attribute)
```
python cluster_snapshot_by_user.py \
  --user doe@databricks.com \
  --output_dir out \
  --profile MY_PROFILE \
  --exclude job
```

By cluster IDs (comma-separated cluster IDs)
```
python cluster_snapshot_by_ids.py \
  --cluster_ids 1125-205205-racer181,1023-023159-prop147  \
  --output_dir out \
  --profile MY_PROFILE
```

All clusters
```
python cluster_snapshot_all.py \
  --output_dir out \
  --profile MY_PROFILE
```

## Sample to recreate a cluster

```
cd out/my_cluster
create_cluster.sh # outputs cluster ID
install_libraries.sh $CLUSTER_ID # attach libraries to cluster.
```
