import yaml
import subprocess

from freya_cli.package_manager import PackageManager
from freya_cli.default_packages import default_packages

package_manager = PackageManager()

def assign_ip_addresses(packages):
    """Assign IP addresses to packages if not already assigned."""
    base_ip = [192, 168, 168, 2]
    taken_ips = {package["ipv4"] for package in default_packages if "ipv4" in package}
    taken_ips.update(package["ipv4"] for package in packages if "ipv4" in package)
    
    for package in packages:
        if "ipv4" not in package:
            while True:
                ip_address = ".".join(map(str, base_ip))
                if ip_address not in taken_ips:
                    package["ipv4"] = ip_address
                    taken_ips.add(ip_address)
                    break
                base_ip[3] += 1
                if base_ip[3] > 254:
                    base_ip[3] = 1
                    base_ip[2] += 1
                    if base_ip[2] > 254:
                        raise ValueError("Ran out of IP addresses in the subnet")

def compose() -> str:
    """Generate a docker-compose.yml file."""
    
    packages = package_manager.get_packages()
    
    with open("docker-compose.yml", "w") as file:
        compose_file = {
            'version': '3',
            'services': {},
            'networks': {
                'freya': {
                    'driver': 'bridge',
                    'ipam': {
                        'config': [
                            {
                                'subnet': '192.168.168.0/24'
                            }
                        ]
                    }
                }
            }
        }

        assign_ip_addresses(packages)

        for package in packages:
            service_name = package["name"]
            compose_file["services"][service_name] = {
                "image": package["image"],
                "ports": [f"{port}:{port}" for port in package["ports"] if port] if "ports" in package else [],
                #"restart": "always",
                "networks": {
                    "freya": {
                        "ipv4_address": package["ipv4"]
                    }
                }
            }

        yaml.dump(compose_file, file, default_flow_style=False, sort_keys=False)
        
def run_compose():
    """Run docker-compose."""
    compose()
    subprocess.run(["docker-compose", "-p", "freya", "up", "-d"])

def stop_compose():
    """Stop docker-compose."""
    subprocess.run(["docker-compose", "-p", "freya", "down"])
    
def restart_compose():
    """Restart docker-compose."""
    stop_compose()
    run_compose()