import yaml

from freya_cli.default_packages import *

class Package():
    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version
        
class DecodedPackage():
    def __init__(self, package: Package):
        self.data = self.decode(package)
        
    def get_package_data(self, package: Package) -> dict:
        if self.is_default_package(package.name)[0]:
            return self.is_default_package(package.name)[1]
        
        # TODO
        #! get package data from database
        return {
            'name': package.name,
            'version': package.version,
            'image': None
        }
        
    def is_default_package(self, name) -> tuple[bool, dict]:
        for package in default_packages:
            if package['name'] == name:
                return (True, package)
        return (False, {})
        
    def decode(self, package: Package) -> dict:
        package_data: dict = self.get_package_data(package=package)
        
        return {
            'name': package_data['name'],
            'version': package_data['version'],
            'image': package_data['image'],
            'ports': package_data['ports'] if 'ports' in package_data else None,
            'ipv4': package_data['ipv4'] if 'ipv4' in package_data else None
        }


class PackageManager():
    def __init__(self):
        self.packages: list[Package] = []
        
    def update_package_file(self):
        try:
            with open("packages.yml", "r") as file:
                existing_packages = yaml.load(file, Loader=yaml.FullLoader) or []
        except FileNotFoundError:
            existing_packages = []

        existing_package_names = {pkg['name'] for pkg in existing_packages}

        new_packages = []
        for package in self.packages:
            if package.name not in existing_package_names:
                decoded_data = DecodedPackage(package).data
                new_packages.append(decoded_data)

        with open("packages.yml", "w") as file:
            yaml.dump(existing_packages + new_packages, file, default_flow_style=False, sort_keys=False)
        
    def add_package(self, package: Package) -> str:
        self.packages.append(package)
        self.update_package_file()
        return "Package added successfully."
        
    def remove_package(self, package_name: str) -> str:
        package_name = package_name.strip().split(":")[0]
        try:
            with open("packages.yml", "r") as file:
                packages = yaml.load(file, Loader=yaml.FullLoader)
                packages = [package for package in packages]
            
            with open("packages.yml", "w") as file:
                for package in packages:
                    if package['name'] == package_name:
                        packages.remove(package)
                yaml.dump(packages, file, default_flow_style=False, sort_keys=False)
        except FileNotFoundError:
            return "No packages installed."
        except (ValueError, TypeError):
            return "Package not found."
        return "Package removed successfully."
        
    def list_packages(self) -> None:
        try:
            with open("packages.yml", "r") as file:
                packages = yaml.load(file, Loader=yaml.FullLoader)
                for package in packages:
                    print(f"{package['name']}, version: {package['version']}")
        except FileNotFoundError:
            print("No packages installed.")
            
    def get_packages(self) -> list[Package]:
        try:
            with open("packages.yml", "r") as file:
                packages = yaml.load(file, Loader=yaml.FullLoader)
                return [package for package in packages]
        except FileNotFoundError:
            return []
        except (ValueError, TypeError):
            return []
