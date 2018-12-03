
import os 

class ClusterDirectoryManager(object):
    '''
    if using cluster by names, you might run into duplicates.
    We account for this by adding __dup_{count} to each duplicate cluster directory name.
    '''

    def __init__(self):
        self.duplicate_clusters = {}
    
    def create_cluster_dir(self, base_dir, cluster_id):
        cluster_id = cluster_id.replace(" ","_")
        dir = os.path.join(base_dir,cluster_id,)
        if os.path.isdir(dir):
            original_dir = dir
            if dir in self.duplicate_clusters:
                count = self.duplicate_clusters[dir]
            else:
                count = 1
                new_dir = "{}__dup_0".format(dir)
                os.rename(dir,new_dir)
            dir = "{}__dup_{}".format(dir,count)
            count += 1
            self.duplicate_clusters[original_dir] = count
        os.makedirs(dir)
        return dir
