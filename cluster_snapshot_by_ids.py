import api_client_factory
import args_utils
from cluster_transformer import ClusterTransformer

if __name__ == "__main__":
    parser = args_utils.build_parser()
    parser.add_argument("-c", "--cluster_ids", dest="cluster_ids", help="Cluster IDs (comma separated)", required=True)
    args = parser.parse_args()
    print("Arguments:")
    for arg in vars(args):
        print(f"  {arg}: {getattr(args, arg)}")
    cluster_ids = args.cluster_ids.split(",")

    client = api_client_factory.get_api_client(args.profile, args.file_client_base_dir)
    transformer = ClusterTransformer(client, args.output_dir, args.use_cluster_id)
    for cluster_id in cluster_ids:
        transformer.process(cluster_id)
    transformer.finish()
    print("Processed {} clusters".format(len(cluster_ids)))
