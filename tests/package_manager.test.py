import unittest
import yaml
import os
from freya_cli.package_manager import Package, PackageManager

class TestPackageManager(unittest.TestCase):
    def setUp(self):
        self.package_manager = PackageManager()
        self.test_package = Package(name="test_package", version="1.0.0")
        self.test_package_file = "packages.yml"

        if os.path.exists(self.test_package_file):
            os.remove(self.test_package_file)

    def tearDown(self):
        if os.path.exists(self.test_package_file):
            os.remove(self.test_package_file)

    def test_add_package(self):
        result = self.package_manager.add_package(self.test_package)
        self.assertEqual(result, "Package added successfully.")
        
        with open(self.test_package_file, "r") as file:
            packages = yaml.load(file, Loader=yaml.FullLoader)
            self.assertEqual(len(packages), 1)
            self.assertEqual(packages[0]['name'], "test_package")
            self.assertEqual(packages[0]['version'], "1.0.0")

    def test_remove_package(self):
        self.package_manager.add_package(self.test_package)
        result = self.package_manager.remove_package("test_package")
        self.assertEqual(result, "Package removed successfully.")
        
        with open(self.test_package_file, "r") as file:
            packages = yaml.load(file, Loader=yaml.FullLoader)
            self.assertEqual(len(packages), 0)

    def test_list_packages(self):
        self.package_manager.add_package(self.test_package)
        with open(self.test_package_file, "r") as file:
            packages = yaml.load(file, Loader=yaml.FullLoader)
            self.assertEqual(len(packages), 1)
            self.assertEqual(packages[0]['name'], "test_package")
            self.assertEqual(packages[0]['version'], "1.0.0")

    def test_get_packages(self):
        self.package_manager.add_package(self.test_package)
        packages = self.package_manager.get_packages()
        self.assertEqual(len(packages), 1)
        self.assertEqual(packages[0]['name'], "test_package")
        self.assertEqual(packages[0]['version'], "1.0.0")

if __name__ == "__main__":
    unittest.main()
