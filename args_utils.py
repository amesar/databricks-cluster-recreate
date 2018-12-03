''' Command line arguments '''

from argparse import ArgumentParser

def build_parser():
  parser = ArgumentParser()
  parser.add_argument("-u", "--url", dest="url", help="API URL", required=True)
  parser.add_argument("-t", "--token", dest="token", help="API token", required=True)
  parser.add_argument("-o", "--output_dir", dest="output_dir", help="output_dir", default=".")
  parser.add_argument("-n", "--use_cluster_name", dest="use_cluster_name", help="use_cluster_name", default=False)
  return parser
