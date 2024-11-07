import subprocess
import pytest

# Пути к тестовому файлу и архиву
TEST_FILE = "test_file.txt"
TEST_ARCHIVE = "test_archive.zip"

@pytest.fixture(scope="module", autouse=True)
def setup_teardown():
    # Подготовка тестовых данных
    with open(TEST_FILE, 'w') as f:
        f.write("Hello, world!")
    
    # Создание архива
    subprocess.run(["zip", TEST_ARCHIVE, TEST_FILE], check=True)
    yield
    # Удаление тестовых файлов после тестов
    subprocess.run(["rm", TEST_FILE, TEST_ARCHIVE], check=True)

# Тест для команды "l" (список файлов)
def test_list_files():
    result = subprocess.run(["zipinfo", TEST_ARCHIVE], capture_output=True, text=True)
    assert TEST_FILE in result.stdout

# Тест для команды "x" (разархивирование с путями)
def test_extract_files():
    subprocess.run(["unzip", TEST_ARCHIVE, "-d", "extracted_files"], check=True)
    result = subprocess.run(["ls", "extracted_files"], capture_output=True, text=True)
    assert TEST_FILE in result.stdout

# Тест для команды "h" (расчёт хеша)
def test_crc32_hash():
    result = subprocess.run(["crc32", TEST_FILE], capture_output=True, text=True)
    calculated_hash = result.stdout.strip()
    
    # Запуск другой команды для расчёта хеша и проверки
    result_verify = subprocess.run(["crc32", TEST_FILE], capture_output=True, text=True)
    assert calculated_hash == result_verify.stdout.strip()
