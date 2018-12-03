
from __future__ import print_function

import sys, json
import requests
from api_client import ApiClient

class HttpApiClient(ApiClient):

    def __init__(self, base_url, token):
        self.base_url = base_url
        self.token = token

    def raw_get(self, resource):
        """ Executes an HTTP GET call
        :param resource: Relative path name of resource such as jobs/get?job_id=1776.
        """
        url = self.base_url + '/' + resource
        rsp = requests.get(url, headers= {'Authorization': 'Bearer '+self.token})
        if rsp.status_code == 404:
            return None
        return rsp.text

    def get(self, path):
        return json.loads(self.raw_get(path))

    def get_cluster(self, cluster_id):
        return self.get("clusters/get?cluster_id={}".format(cluster_id))

    def _get_clusters(self):
        return json.loads(self.raw_get_clusters())

    def raw_get_clusters(self):
        ''' Optimization for caching API content for FileApiClient usage '''
        return self.raw_get("clusters/list")

    def get_cluster_status(self, cluster_id):
        return json.loads(self._get_cluster_status(cluster_id))

    def _get_cluster_status(self, cluster_id):
        ''' Optimization for caching API content for FileApiClient usage '''
        return self.raw_get("libraries/cluster-status?cluster_id={}".format(cluster_id))

    def get_lib_all_cluster_statuses(self):
        ''' This doesn't return all the cluster statuses as expected '''
        return self.get("libraries/all-cluster-statuses")
