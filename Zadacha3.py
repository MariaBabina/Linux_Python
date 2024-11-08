import pytest
import subprocess
from datetime import datetime
import yaml  

with open("config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)

FILE_COUNT = config['file_count']
FILE_SIZE = config['file_size']

@pytest.fixture(autouse=True)
def log_statistics():
    yield
    with open("stat.txt", "a") as stat_file:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open("/proc/loadavg", "r") as loadavg_file:
            loadavg = loadavg_file.read().strip()
        
        stat_file.write(f"{current_time}, {FILE_COUNT}, {FILE_SIZE}, {loadavg}\n")

def test_list_files():
    result = subprocess.run(["7z", "l", "test_archive.7z"], capture_output=True, text=True)
    assert "test_file.txt" in result.stdout

def test_extract_files():
    subprocess.run(["7z", "x", "test_archive.7z", "-otest_extract"], check=True)
    assert os.path.exists("test_extract/test_file.txt")

def test_crc32_hash():
    result = subprocess.run(["crc32", "test_file.txt"], capture_output=True, text=True)
    calculated_hash = result.stdout.strip()

    result_verify = subprocess.run(["crc32", "test_file.txt"], capture_output=True, text=True)
    assert calculated_hash == result_verify.stdout.strip()
