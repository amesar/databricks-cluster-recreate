from __future__ import print_function
from api_client import ApiClient
from databricks_cli.sdk import api_client
import cred_utils

class HttpApiClient(ApiClient):

    def __init__(self, profile=None):
        (host,token) = cred_utils.get_credentials(profile)
        print("Host:",host)
        self.db_api = api_client.ApiClient(None, None, host, token)

    def get_cluster(self, cluster_id):
        return self.db_api.perform_query("GET", "/clusters/get?cluster_id={}".format(cluster_id))

    def _get_clusters(self):
        return self.db_api.perform_query("GET", "/clusters/list")

    def get_cluster_status(self, cluster_id):
        return self._get_cluster_status(cluster_id)

    def _get_cluster_status(self, cluster_id):
        ''' Optimization for caching API content for FileApiClient usage '''
        return self.db_api.perform_query("GET", "/libraries/cluster-status?cluster_id={}".format(cluster_id))

    def get_lib_all_cluster_statuses(self):
        ''' This doesn't return all the cluster statuses as expected '''
        return self.db_api.perform_query("GET", "/libraries/all-cluster-statuses")
