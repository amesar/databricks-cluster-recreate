# databricks-cluster-recreate

Creates snapshots of cluster configuration and attached libraries from REST API, and scripts to recreate the cluster with the libraries.

Where's my cluster gone? These scripts aim to answer the next question: how do I recreate my cluster? 

## Setup

See: [https://github.com/databricks/databricks-cli](https://github.com/databricks/databricks-cli)
```
pip install --upgrade databricks-cli
```

## Sample runs

By Cluster IDs
```
python cluster_snapshot_by_ids.py \
  --cluster_ids 1125-205205-racer181,1023-023159-prop147  \
  --output_dir out \
  --use_cluster_name True \
  --profile MY_PROFILE
```

By User (creator_user_name):
```
python cluster_snapshot_by_user.py \
  --user doe@databricks.com \
  --output_dir out \
  --use_cluster_name True \
  --profile MY_PROFILE
```

All clusters:
```
python cluster_snapshot_all.py \
  --output_dir out \
  --use_cluster_name True \
  --profile MY_PROFILE
```
