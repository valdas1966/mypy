import os
import sys
from f_utils import u_file
from f_google import u_storage

path_json_key = 'd:\\professor\\json\\viewer.json'
json_key = u_file.read(path_json_key)
project = 'noteret'
str_bucket = 'us-central1-noteret-bf653c49-bucket'

def main():
    if not len(sys.argv) == 2:
        raise ValueError(sys.argv)
    path_dag = sys.argv[1]
    name_dag = os.path.basename(path_dag)
    u_storage.upload(json_key=json_key,
                     project=project,
                     str_bucket=str_bucket,
                     path_src=path_dag,
                     path_dest=name_dag)


if __name__ == '__main__':
    main()
