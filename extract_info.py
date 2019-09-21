import yaml

with open('instances_command_folder/instances.yml') as f:
    instances_data = yaml.safe_load(f)

with open('instances_command_folder/command_servers.yml') as f:
    command_data = yaml.safe_load(f)
# Dump to yaml file
# with open('output.yml','w') as f:
#     yaml.dump(instances_data['test_configuration']['router_asn'],f)
contrail_config = instances_data['contrail_configuration']

for node, value in instances_data['instances'].items():
    if 'control' in value['roles']:
        print("Control nodes:",node)
    if 'vrouter' in value['roles']:
        print("Compute nodes:",node)
    if 'k8s_master' in value['roles']:
        print("Kube master:",node)
    if 'kubemanager' in value['roles']:
        print("kubemanager:",node)
    if 'k8s_node' in value['roles']:
        print("k8s_node:",node)

print(
   type(instances_data['instances'])
)

