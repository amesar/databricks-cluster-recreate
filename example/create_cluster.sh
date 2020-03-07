
# Create cluster and install libraries

_create_cluster.sh > cluster_id.json
sleep 5 # wait for cluster to be created
cluster_id=`grep cluster_id cluster_id.json | sed -e 's/"//g' -e 's/cluster_id://' -e 's/ //g'` 
echo CLUSTER_ID: $cluster_id
PROFILE=$1
_install_libraries.sh $cluster_id $PROFILE
