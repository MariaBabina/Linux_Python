import paramiko
import pytest
import zlib
from datetime import datetime
import yaml

with open("config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)

SSH_HOST = config["ssh_host"]
SSH_USER = config["ssh_user"]
SSH_PASSWORD = config["ssh_password"]

def ssh_run_command(command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()
        return output, error
    finally:
        client.close()

@pytest.fixture(autouse=True)
def log_statistics():
    yield
    with open("stat.txt", "a") as stat_file:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("/proc/loadavg", "r") as loadavg_file:
            loadavg = loadavg_file.read().strip()
        stat_file.write(f"{current_time}, {loadavg}\n")

def test_list_files_in_archive():
    output, error = ssh_run_command("7z l example_archive.7z")
    assert not error, f"Error in command: {error}"
    assert "example_file.txt" in output  # проверка на наличие файла в архиве

def test_extract_with_paths():
    ssh_run_command("7z x example_archive.7z -oextracted_files")
    output, error = ssh_run_command("ls extracted_files")
    assert not error, f"Error in command: {error}"
    assert "extracted_file.txt" in output  # проверка на успешное разархивирование файла

def test_crc32_hash():
    filename = "testfile.txt"  # файл, который должен быть на сервере
    output, error = ssh_run_command(f"crc32 {filename}")
    assert not error, f"Error in command: {error}"

    with open(filename, "rb") as f:
        data = f.read()
    expected_crc32 = format(zlib.crc32(data) & 0xFFFFFFFF, '08x')
    
    assert expected_crc32 in output
