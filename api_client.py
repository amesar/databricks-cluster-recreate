from abc import abstractmethod, ABCMeta

class ApiClient(metaclass=ABCMeta):

    @abstractmethod
    def _get_clusters(self):
        pass

    @abstractmethod
    def _get_cluster(self, cluster_id):
        pass

    def get_clusters(self):
        return self._get_clusters()['clusters']

    def get_cluster(self, cluster_id):
        return self._get_cluster(cluster_id)

    def get_lib_all_cluster_statuses(self):
        raise NotImplementedError("Not implemented")
