
# Create cluster

if [ $# -gt 0 ] ; then
  PROFILE="--profile $1"
fi
databricks clusters create --json-file cluster.json $PROFILE
