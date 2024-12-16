import unittest
from unittest.mock import patch, mock_open
from freya_cli.composer import assign_ip_addresses, compose, run_compose, stop_compose, restart_compose, default_packages

class TestComposer(unittest.TestCase):

    @patch('freya_cli.composer.PackageManager')
    def test_assign_ip_addresses(self, MockPackageManager):
        packages = [
            {"name": "package1", "image": "image1"}, # no ip
            {"name": "package2", "image": "image2"}, # no ip
            {"name": "package4", "image": "image4", "ipv4": "192.168.168.2"}, # already reserved
            {"name": "package3", "image": "image3", "ipv4": "192.168.168.168"}, # custom ip
        ]
        
        assign_ip_addresses(packages)
        self.assertEqual(packages[0]["ipv4"], f"192.168.168.{len(default_packages) + 2}") # no ip
        self.assertEqual(packages[1]["ipv4"], f"192.168.168.{len(default_packages) + 3}") # no ip
        self.assertEqual(packages[2]["ipv4"], f"192.168.168.{len(default_packages) + 4}") # already reserved
        self.assertEqual(packages[3]["ipv4"], "192.168.168.168") # custom ip

    @patch('freya_cli.composer.PackageManager')
    @patch('builtins.open', new_callable=mock_open, create=True)
    @patch('yaml.dump')
    def test_compose(self, mock_yaml_dump, mock_open, MockPackageManager):
        # Mocking the default packages
        mock_package_manager = MockPackageManager.return_value
        mock_package_manager.get_packages.return_value = [
            {"name": "package1", "image": "image1", "ports": [80, 443]}, # ports no ip
            {"name": "package2", "image": "image2"}, # no ports no ip
            {"name": "package3", "image": "image3", "ipv4": "192.168.168.168"}, # no ports, assigned ip
            {"name": "package4", "image": "image4", "ports": [4321], "ipv4": "192.168.168.169"}, # port, assigned ip
            {"name": "package5", "image": "image5", "ipv4": ""}, # no ip
            {"name": "package6", "image": "image6"} # test whole package
        ]

        compose(mock_package_manager.get_packages())

        # Verify the file was written
        mock_open.assert_any_call("docker-compose.yml", "w")
        mock_yaml_dump.assert_called_once()

        # Validate the content written to the yaml
        compose_file = mock_yaml_dump.call_args[0][0]
        
        self.assertIn('services', compose_file)
        self.assertIn('package1', compose_file['services'])
        self.assertIn('package2', compose_file['services'])
        self.assertIn('package3', compose_file['services'])
        self.assertIn('package4', compose_file['services'])
        self.assertIn('package5', compose_file['services'])
        self.assertEqual(compose_file['services']['package1']['image'], 'image1')
        self.assertEqual(compose_file['services']['package2']['image'], 'image2')
        self.assertEqual(compose_file['services']['package1']['networks']['freya']['ipv4_address'], f"192.168.168.{len(default_packages) + 2}") # auto assigned ip
        self.assertEqual(compose_file['services']['package2']['networks']['freya']['ipv4_address'], f"192.168.168.{len(default_packages) + 3}") # auto assigned ip
        self.assertEqual(compose_file['services']['package3']['networks']['freya']['ipv4_address'], "192.168.168.168") # assigned ip
        self.assertEqual(compose_file['services']['package4']['networks']['freya']['ipv4_address'], "192.168.168.169") # assigned ip
        self.assertEqual(compose_file['services']['package5']['networks']['freya']['ipv4_address'], f"192.168.168.{len(default_packages) + 4}") # auto assigned ip
        self.assertEqual(compose_file['services']['package1']['ports'], ['80:80', '443:443']) # two ports
        self.assertEqual(compose_file['services']['package4']['ports'], ['4321:4321']) # port
        self.assertEqual(compose_file['services']['package6'], {'image': 'image6', 'ports': [], 'networks': {'freya': {'ipv4_address': f"192.168.168.{len(default_packages) + 5}"}}}) # whole package])
        
        

    @patch('subprocess.run')
    @patch('freya_cli.composer.compose')
    def test_run_compose(self, mock_compose, mock_subprocess_run):
        run_compose()
        mock_compose.assert_called_once()
        mock_subprocess_run.assert_called_once_with(["docker", "compose", "-p", "freya", "-f", "docker-compose.yml", "up", "-d", "--build"])

    @patch('subprocess.run')
    def test_stop_compose(self, mock_subprocess_run):
        stop_compose()
        mock_subprocess_run.assert_called_once_with(["docker", "compose", "-p", "freya", "down"])

    @patch('freya_cli.composer.stop_compose')
    @patch('freya_cli.composer.run_compose')
    def test_restart_compose(self, mock_run_compose, mock_stop_compose):
        restart_compose()
        mock_stop_compose.assert_called_once()
        mock_run_compose.assert_called_once()

if __name__ == '__main__':
    unittest.main()
