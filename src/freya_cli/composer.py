import yaml
import subprocess

from freya_cli.package_manager import PackageManager
from freya_cli.default_packages import default_packages

package_manager = PackageManager()

def assign_ip_addresses(packages) -> None:
    """Assign IP addresses to packages if not already assigned."""
    base_ip = [192, 168, 168, 2]
    taken_ips = {package["ipv4"] for package in default_packages if "ipv4" in package and package["ipv4"]}
    default_ips = taken_ips.copy()
    taken_ips.update(package["ipv4"] for package in packages if "ipv4" in package and package["ipv4"])
    
    def generate_ip(package):
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
    
    for package in packages:
        if not package.get("ipv4") or package["ipv4"] in default_ips:
            generate_ip(package)

def generate_service(package) -> dict:
    base = {
        "image": package["image"],
        "networks": {
            "freya": {
                "ipv4_address": package["ipv4"]
            }
        }
    }
    if package.get("ports"):
        for port in package["ports"]:
            base["ports"] = []
            if isinstance(port, tuple):
                base["ports"].append(f"{port[0]}:{port[1]}")
            else:
                base["ports"].append(f"{port}:{port}")

    ignore_list = ["name", "version", "ports", "ipv4"]
    for key in package:
        if key in ignore_list: continue
        if key in base: continue
        base[key] = package[key]
            
    return base
    

def compose(packages: list = []) -> None:
    """Generate a docker-compose.yml file."""
    
    if packages == []:
        packages = package_manager.get_packages()
    
    with open("docker-compose.yml", "w") as file:
        compose_file = {
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
            compose_file["services"][service_name] = generate_service(package)

        yaml.dump(compose_file, file, default_flow_style=False, sort_keys=False)
        
def run_compose() -> None:
    """Run docker-compose."""
    compose()
    subprocess.run(["docker", "compose", "-p", "freya", "-f", "docker-compose.yml", "up", "-d", "--build"])

def stop_compose() -> None:
    """Stop docker-compose."""
    subprocess.run(["docker", "compose", "-p", "freya", "down"])
    
def restart_compose() -> None:
    """Restart docker-compose."""
    stop_compose()
    run_compose()