from freya_cli.package_manager import Package

def compose(packages: list[Package]):
    """Generate a docker-compose.yml file."""
    
    with open("docker-compose.yml", "w") as file:
        compose_file = {
            'version': '3',
            'services': {}
        }

        for package in packages:
            service_name = package['name']
            compose_file['services'][service_name] = {
                'image': package['image'],
                'ports': package.get('ports', []),
                'volumes': package.get('volumes', []),
                'environment': package.get('environment', [])
            }

        #yaml.dump(compose_file, file, default_flow_style=False)
        
def run_compose():
    """Run docker-compose."""
    pass

def stop_compose():
    """Stop docker-compose."""
    pass