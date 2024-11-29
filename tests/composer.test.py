import unittest
from unittest.mock import patch, mock_open, MagicMock
import yaml
from freya_cli.composer import assign_ip_addresses, compose, run_compose, stop_compose, restart_compose

class TestComposer(unittest.TestCase):

    @patch('freya_cli.composer.PackageManager')
    def test_assign_ip_addresses(self, MockPackageManager):
        packages = [
            {"name": "package1", "image": "image1"},
            {"name": "package2", "image": "image2", "ipv4": "192.168.168.3"}
        ]
        default_packages = [
            {"name": "default_package", "image": "default_image", "ipv4": "192.168.168.2"}
        ]
        assign_ip_addresses(packages)
        self.assertEqual(packages[0]["ipv4"], "192.168.168.4")
        self.assertEqual(packages[1]["ipv4"], "192.168.168.3")

    @patch('freya_cli.composer.PackageManager')
    @patch('builtins.open', new_callable=mock_open)
    @patch('yaml.dump')
    def test_compose(self, mock_yaml_dump, mock_open, MockPackageManager):
        mock_package_manager = MockPackageManager.return_value
        mock_package_manager.get_packages.return_value = [
            {"name": "package1", "image": "image1", "ports": [80, 443]},
            {"name": "package2", "image": "image2", "ipv4": "192.168.168.3"}
        ]
        
        compose()
        
        mock_open.assert_called_once_with("docker-compose.yml", "w")
        mock_yaml_dump.assert_called_once()
        compose_file = mock_yaml_dump.call_args[0][0]
        
        self.assertIn('services', compose_file)
        self.assertIn('networks', compose_file)
        self.assertIn('freya', compose_file['networks'])
        self.assertIn('package1', compose_file['services'])
        self.assertIn('package2', compose_file['services'])
        self.assertEqual(compose_file['services']['package1']['image'], 'image1')
        self.assertEqual(compose_file['services']['package2']['image'], 'image2')

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