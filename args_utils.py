''' Command line arguments '''

from argparse import ArgumentParser

def build_parser():
  parser = ArgumentParser()
  parser.add_argument("-f", "--file_client_base_dir", dest="file_client_base_dir", help="file_client", required=False)
  parser.add_argument("-p", "--profile", dest="profile", help="profile", required=False)
  parser.add_argument("-o", "--output_dir", dest="output_dir", help="output_dir", default=".")
  parser.add_argument("-n", "--use_cluster_id", dest="use_cluster_id", help="use_cluster_id", default=False)
  return parser
