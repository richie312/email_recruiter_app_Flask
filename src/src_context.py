import os
src_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = src_dir[:-4]
data_dir = os.path.join(root_dir,os.path.join("test","data"))
config_dir = os.path.join(root_dir,"config")
#ToDo Delete this path post integration.
egp_current_dir = os.path.join(root_dir,"src\egp_sas_new")