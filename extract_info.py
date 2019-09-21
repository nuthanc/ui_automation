import yaml

with open('instances_command_folder/instances.yml') as f:
    instances_data = yaml.safe_load(f)

with open('instances_command_folder/command_servers.yml') as f:
    command_data = yaml.safe_load(f)

contrail_config = instances_data['contrail_configuration']

print(
    type(instances_data['test_configuration']['router_asn']),
)

with open('output.yml','w') as f:
    yaml.dump(instances_data['test_configuration']['router_asn'],f)