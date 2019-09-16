import yaml

with open('instances_command_folder/instances.yml') as f:
    instances_data = yaml.safe_load(f)

with open('instances_command_folder/command_servers.yml') as f:
    command_data = yaml.safe_load(f)

contrail_config = instances_data['contrail_configuration']

for i, (k, v) in enumerate(contrail_config.items()):
    print(k)
    print(str(v))
    print(type(str(v)))
print(
    "https://"+command_data['command_servers']['server1']['ip']
)