import subprocess

class CIHandler:
    @staticmethod
    def run_tests():
        """Запуск тестов через CI/CD"""
        subprocess.run(["pytest", "-v", "tests/"])
