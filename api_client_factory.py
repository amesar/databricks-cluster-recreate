
from __future__ import print_function

from file_api_client import FileApiClient
from http_api_client import HttpApiClient

def get_api_client(url, token):
    client =  HttpApiClient(url,token) if url.startswith("http") else FileApiClient(url)
    print("api_client:",type(client))
    return client
