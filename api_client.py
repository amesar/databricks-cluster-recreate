
from __future__ import print_function

class ApiClient(object):

    def _get_clusters(self):
        raise NotImplementedError("Not implemented")

    def get_clusters(self):
        return self._get_clusters()['clusters']

    def get_cluster(self, cluster_id):
        return self._get_cluster(cluster_id)

    def get_lib_all_cluster_statuses(self):
        raise NotImplementedError("Not implemented")
