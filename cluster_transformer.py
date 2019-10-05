import sys, os, json
import api_client_factory
import lib_transformer
import utils
from cluster_directory_manager import ClusterDirectoryManager

keys = ['cluster_name', 'spark_version', 'driver_node_type_id', 'node_type_id', 'num_workers', 'autotermination_minutes', 'spark_env_vars', 'spark_conf', 'init_scripts']

class ClusterTransformer(object):
    def __init__(self, client, output_dir, use_cluster_id):
        self.client = client
        self.output_dir = output_dir
        self.use_cluster_id = use_cluster_id
        self.manifests = []
        self.duplicate_clusters = ClusterDirectoryManager()

    def process(self, cluster_id):
        try:
            self._process(cluster_id)
        except Exception as ex:
            print("WARNING: cluster_id={} ex={}".format(cluster_id,ex))
            import traceback
            traceback.print_exc()

    def _process(self, cluster_id):
        cluster = self.client.get_cluster(cluster_id)
        cluster_name = cluster['cluster_name']
        sys.stdout.write("Cluster: {:<20s} {}\n".format(cluster_id,cluster_name))
    
        dct = {}
        for k in keys:
            v = cluster.get(k,None)
            if v is not None: dct[k] = v
    
        which = cluster_id if self.use_cluster_id else cluster_name
        cluster_dir = self.duplicate_clusters.create_cluster_dir(self.output_dir, which)
        cluster_dir2 = os.path.join(cluster_dir,"from_api")
        os.makedirs(cluster_dir2) 
    
        # -- Write cluster files
    
        opath = self.create_path(cluster_dir,"cluster", which)
        with open(opath, 'w') as f:
            f.write(json.dumps(dct,indent=2)+'\n')
    
        opath = self.create_path(cluster_dir2,"cluster", which)
        with open(opath, 'w') as f:
            f.write(json.dumps(cluster,indent=2)+'\n')
    
        # -- Write lib status files
    
        status = self.client.get_cluster_status(cluster_id)
        lib_transformer.build_files(status, cluster_dir, cluster_dir2, cluster_id, which)
    
        # -- Create create_cluster.sh
    
        opath = os.path.join(cluster_dir,"create_cluster.sh")
        with open(opath, 'w') as f:
            f.write("\n# Create cluster\n\n")
            f.write("databricks clusters create --json-file cluster.json\n")
        utils.chmod_x(opath)
    
        # -- Write manifest file
    
        opath = os.path.join(cluster_dir,"manifest.json")

        with open(opath, 'w') as f:
            manifest = { 'cluster_id': cluster_id, 'cluster_name': cluster_name, 'creator_user_name': cluster['creator_user_name'], 'start_time': utils.calc_time(cluster)  }
            f.write(json.dumps(manifest,indent=2)+'\n')

        self.manifests.append(manifest)

    def create_path(self, base_dir, name, cluster_id, ext="json"):
        file =  "{}.{}".format(name,ext)
        return os.path.join(base_dir,file)

    def finish(self):
        opath = os.path.join(self.output_dir,"manifest.json")
        with open(opath, 'w') as f:
            f.write(json.dumps(self.manifests,indent=2)+'\n')
