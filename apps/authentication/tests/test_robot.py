from django.test import TestCase
import subprocess

class RobotTest(TestCase):
    def test_run_robot(self):
        result = subprocess.run(['robot', 'apps/authentication/tests/robot_tests/user_tests.robot'], capture_output=True, text=True)
        print(result.stdout)
        assert result.returncode == 0  # Make sure the tests pass successfully
