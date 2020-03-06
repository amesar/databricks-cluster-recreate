# databricks-cluster-recreate

Where have all my clusters gone? These scripts address the problem: how do I recreate my suddenly departed clusters? 

Using the Databricks REST API, this tool generates scripts to recreate your cluster(s) with their attached libraries.

## Synopsis
Create scripts
```
python cluster_snapshot_by_user.py --user doe@databricks.com
```
Recreate cluster
```
create_cluster.sh # outputs cluster ID
install_libraries.sh $CLUSTER_ID
```


## Setup

Scripts use the Databricks CLI and its configuration.
See: [https://github.com/databricks/databricks-cli](https://github.com/databricks/databricks-cli).
```
pip install --upgrade databricks-cli
```

## Overview

### What the scripts do
* Creates a directory for each cluster that matches the search criteria.
* JSON spec files to create cluster and attach libraries.
* Convenience shell scripts to recreate the cluster and attach its libraries. 
* The scripts use the databricks CLI.

### Cluster recreate scripts 

[Sample](example) cluster directory:
```
├── my_cluster
│   ├── cluster.json
│   ├── create_cluster.sh
│   ├── from_api
│   │   ├── cluster.json
│   │   └── libraries.json
│   ├── install_libraries.sh
│   ├── libraries.json
│   └── manifest.json
└── manifest.json
```

File details:
* [create_cluster.sh](example/create_cluster.sh) - script uses the Databricks CLI to create a new cluster
  * [cluster.json](example/cluster.json) - JSON spec used to create the cluster. Request for [clusters/create](https://docs.databricks.com/api/latest/clusters.html#create) API endpoint.
* [install_libraries.sh](example/install_libraries.sh) - script attaches all libraries to the cluster.
  * [libraries.json](example/libraries.json) - Informational. Not used by the CLI-based tool. Apparently the CLI does not support batch library installs as does the [libraries/install](https://docs.databricks.com/dev-tools/api/latest/libraries.html#install) endpoint.
* [from_api](example/from_api) - Original output from API get calls
  * [cluster.json](example/from_api/cluster.json) - response from [clusters/get](https://docs.databricks.com/api/latest/clusters.html#get) endpoint.
  * [libraries.json](example/from_api/libraries.json) - response from [libraries/cluster-status](https://docs.databricks.com/api/latest/libraries.html#cluster-status) endpoint.

### Cluster recreate scripts examples

[create_cluster.sh](example/create_cluster.sh)
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

### Run Options

The option `use_cluster_id` determines whether directory names are cluster IDs or cluster names. The default is to use cluster names.

Since cluster names are not unique, when duplicate names occur the resulting directory name will have `__dup_{COUNT}` appended to it. For example, `cool_cluster__dup_01` and `cool_cluster__dup_02`.

Note, that although you can apparently pass the response from cluster/get to cluster/create, the recreate script extracts only those fields that are required by cluster/create from the much more verbose cluster/get payload.


## Run 

### Generate cluster recreate scripts

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

### Recreate the cluster

```
cd out/my_cluster
create_cluster.sh # outputs cluster ID
install_libraries.sh $CLUSTER_ID # attach libraries to cluster.
```
