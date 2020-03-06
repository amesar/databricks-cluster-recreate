import json
import os
import utils

lib_types = { 'maven': 'maven-coordinates', 'pypi': 'pypi-package', 'jar': 'jar', 'egg': 'egg', 'whl': 'whl', 'cran': 'cran-package'  }
verbose = False

def add_command(lib_type, lib_value):
    lib_type2 = lib_types[lib_type]
    #if lib_type == 'jar' or lib_type == 'egg':
    if lib_type in [ 'jar','egg','whl' ]:
        lib = lib_value
    elif lib_type == 'cran':
        lib = lib_value['package']
    else:
        k = list(lib_value.keys())[0]  
        lib = lib_value[k]
    return "databricks libraries install --cluster-id $cluster_id --{} {}".format(lib_type2,lib)

''' Build command file '''
def build_command_file(opath2, cluster_id, cmds):
    with open(opath2, 'w') as f:
        f.write("\n# Install libraries for cluster {}\n\n".format(cluster_id))
        f.write("if [ $# -eq 0 ] ; then\n")
        f.write("  echo ERROR: Missing CLUSTER_ID\n")
        f.write("  exit 1\n")
        f.write("  fi\n")
        f.write("cluster_id=$1\n\n")
        f.write("if [ $# -gt 1 ] ; then\n")
        f.write('  PROFILE="--profile $2"\n')
        f.write("fi\n")
        for cmd in cmds:
            f.write(cmd+" $PROFILE\n")
    utils.chmod_x(opath2)

def create_path(output_dir, name, ext):
    file  = "{}.{}".format(name,ext)
    return os.path.join(output_dir,file)
    #cluster_id = cluster_id.replace(" ","_")
    #return  "{}_{}.{}".format(output_base,cluster_id,ext)

def build_files(statuses, output_dir, output_dir2, cluster_id, which):
    if not 'library_statuses' in statuses:
        if verbose: print("INFO: No libraries in cluster {}".format(which))
        return

    libraries = []
    commands = []
    for lib in statuses['library_statuses']:
        lib = lib['library']
        k = list(lib.keys())[0]  
        v = lib[k]
        libraries.append({k:v})
        commands.append(add_command(k,v))

    opath = create_path(output_dir, "libraries","json")
    with open(opath, 'w') as f:
        dct = { "cluster_id" : cluster_id, 'libraries' : libraries }
        f.write(json.dumps(dct,indent=2)+'\n')

    opath = create_path(output_dir2, "libraries","json")
    with open(opath, 'w') as f:
        f.write(json.dumps(statuses,indent=2)+'\n')

    opath = create_path(output_dir, "install_libraries","sh")
    build_command_file(opath, which, commands)
