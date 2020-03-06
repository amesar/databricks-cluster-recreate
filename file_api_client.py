import json
from api_client import ApiClient

class FileApiClient(ApiClient):

    def __init__(self, base_dir):
        self.base_dir = base_dir

    def raw_read(self, resource):
        path = self.base_dir+"/"+resource
        with open(path, 'r') as f:
            return f.read()

    def read(self, resource):
        return json.loads(self.raw_read(resource))

    def _get_clusters(self):
        return self.read("clusters.json")

    def raw_get_clusters(self):
        return self._read("clusters.json")

    def _get_cluster(self, cluster_id):
        clusters = self.get_clusters()
        clusters = self.to_map(clusters)
        return clusters[cluster_id]

    def get_cluster_status(self, cluster_id):
        path = "lib_statuses/{}.json".format(cluster_id)
        return self.read(path)

    def raw_get_cluster_status(self, cluster_id):
        path = "lib_statuses/{}.json".format(cluster_id)
        return self.raw_read(path)

    def get_lib_all_cluster_statuses(self):
        return self.read("all-cluster-statuses.json")

    def to_map(self, clusters):
        dct = {}
        for cl in clusters:
            cid = cl['cluster_id']
            dct[cid] = cl
        return dct
