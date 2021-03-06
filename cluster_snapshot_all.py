import args_utils
import api_client_factory
from cluster_transformer import ClusterTransformer

if __name__ == "__main__":
    parser = args_utils.build_parser()
    args = parser.parse_args()
    print("Arguments:")
    for arg in vars(args):
        print(f"  {arg}: {getattr(args, arg)}")

    client = api_client_factory.get_api_client(args.profile, args.file_client_base_dir)
    transformer = ClusterTransformer(client, args.output_dir, args.use_cluster_id)
    clusters = client.get_clusters()
    for cl in clusters:
        cluster_id = cl['cluster_id']
        transformer.process(cluster_id)
    transformer.finish()
    print("Processed {} clusters".format(len(clusters)))

