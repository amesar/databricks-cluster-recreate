from __future__ import print_function

from file_api_client import FileApiClient
from http_api_client import HttpApiClient

def get_api_client(profile, file_client_base_dir):
    client =  FileApiClient(file_client_base_dir) if file_client_base_dir is not None else HttpApiClient(profile)
    print("api_client:",type(client).__name__)
    return client
