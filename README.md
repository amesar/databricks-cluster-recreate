# databricks-cluster-recreate

Where have all my Databricks clusters gone? These scripts solve the problem: how do I recreate my suddenly departed clusters? 

This tool generates scripts (using the Databricks CLI) that recreate your clusters along with their attached libraries.

## Synopsis
Create recreate scripts:
```
python cluster_snapshot_by_user.py --user doe@databricks.com
```
Recreate cluster:
```
create_cluster.sh
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
* Creates a JSON spec file to create cluster 
* Convenience shell scripts to recreate the cluster and attach its libraries. 
* The scripts use the Databricks CLI.

### Cluster recreate scripts 

[Sample](example) directory with recreate scripts:
```
├── my_cluster
│   ├── _create_cluster.sh
│   ├── _install_libraries.sh
│   ├── cluster.json
│   ├── create_cluster.sh
│   ├── from_api
│   │   ├── cluster.json
│   │   └── libraries.json
│   ├── libraries.json
│   └── manifest.json
└── manifest.json
```

File details:
* [create_cluster.sh](example/create_cluster.sh) - Calls _create_cluster.sh and _install_libraries.sh.
* [_create_cluster.sh](example/_create_cluster.sh) - Creates a new cluster.
  * [cluster.json](example/cluster.json) - JSON spec used to create the cluster. Request for [clusters/create](https://docs.databricks.com/api/latest/clusters.html#create) API endpoint.
* [_install_libraries.sh](example/_install_libraries.sh) - Attaches all libraries to the cluster.
  * [libraries.json](example/libraries.json) - Informational. Not used by the CLI-based tool. Apparently the CLI does not support batch library installs as does the [libraries/install](https://docs.databricks.com/dev-tools/api/latest/libraries.html#install) endpoint.
* [from_api](example/from_api) - Original output from API get calls
  * [cluster.json](example/from_api/cluster.json) - Response from the [clusters/get](https://docs.databricks.com/api/latest/clusters.html#get) endpoint.
  * [libraries.json](example/from_api/libraries.json) - Response from the [libraries/cluster-status](https://docs.databricks.com/api/latest/libraries.html#cluster-status) endpoint.

### Cluster recreate scripts examples

[create_cluster.sh](example/create_cluster.sh)
```
_create_cluster.sh > cluster_id.json
sleep 5 # wait for cluster to be created
cluster_id=`grep cluster_id cluster_id.json | sed -e 's/"//g' -e 's/cluster_id://' -e 's/ //g'` 
echo CLUSTER_ID: $cluster_id
PROFILE=$1
_install_libraries.sh $cluster_id $PROFILE
```

[_create_cluster.sh](example/_create_cluster.sh)
```
if [ $# -gt 0 ] ; then
  PROFILE="--profile $1"
fi
databricks clusters create --json-file cluster.json $PROFILE
```

[_install_libraries.sh](example/_install_libraries.sh)
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

### Common Run Options

|Name | Required | Default | Description|
|---|---|---|---|
| profile | no | none | From `~/.databricks.cfg`  |
| output_dir | no | . | Output folder for recreate scripts  |
| use_cluster_id | no | False | Use cluster ID or cluster name for the folder to contain a cluster's recreate scripts  |



Since cluster names are not unique, if you use `--use_cluster_id no`, when duplicate names occur the resulting directory names will have `__dup_{COUNT}` appended to them. 
For example, there could be two clusters named `cool_cluster`. 
Therefore there will be two cluster directories called `cool_cluster__dup_01` and `cool_cluster__dup_02`.


## Run - Generate cluster recreate scripts

There are several different ways to build recreate scripts by using different search criteria.
`By user` is the most common one.

### By User 

Works off of the [creator_user_name](https://docs.databricks.com/dev-tools/api/latest/clusters.html#get) JSON attribute.

Options:

|Name | Required | Default | Description|
|---|---|---|---|
| user | yes | N/A | Databricks user name |
| exclude | no | False | Exclude job clusters |

Example:
```
python cluster_snapshot_by_user.py \
  --user doe@databricks.com \
  --output_dir out \
  --profile MY_PROFILE \
  --exclude job
```

### By Cluster IDs

Options:

|Name | Required | Default | Description|
|---|---|---|---|
| cluster_ids | yes | N/A | comma-separated list of cluster IDs |

Example:
```
python cluster_snapshot_by_ids.py \
  --cluster_ids 1125-205205-racer181,1023-023159-prop147  \
  --output_dir out \
  --profile MY_PROFILE
```

### All clusters

Could take a while though ;)
```
python cluster_snapshot_all.py \
  --output_dir out \
  --profile MY_PROFILE
```

## Run - Recreate the cluster

```
cd out/my_cluster
create_cluster.sh 
```
```
CLUSTER_ID: 0306-234717-muss25
```
