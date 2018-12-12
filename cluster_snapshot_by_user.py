rom __future__ import print_function

import args_utils
import api_client_factory
from cluster_transformer import ClusterTransformer

if __name__ == "__main__":
    parser = args_utils.build_parser()
    parser.add_argument("-U", "--user", dest="user", help="user name (creator_user_name)", required=True)
    args = parser.parse_args()
    print("args:",args)

    client = api_client_factory.get_api_client(args.profile, args.file_client_base_dir)
    clusters = client.get_clusters()
    transformer = ClusterTransformer(client, args.output_dir, args.use_cluster_id)
    count = 0
    for cl in clusters:
        cluster_id = cl['cluster_id']
        user = cl['creator_user_name']
        if args.user in user:
            transformer.process(cluster_id)
            count += 1
    transformer.finish()
    print("Processed {}/{} matching clusters".format(count,len(clusters)))
