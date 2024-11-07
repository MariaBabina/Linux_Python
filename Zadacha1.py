import subprocess

def run_command_and_check_text(command, text):
    try:
        # Выполняем команду и получаем вывод
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        # Проверяем, есть ли указанный текст в выводе команды
        return text in result.stdout
    except Exception as e:
        print(f"Ошибка: {e}")
        return False

# Пример использования
if __name__ == "__main__":
    # Запрашиваем команду и текст у пользователя
    command = input("Введите команду: ")
    text = input("Введите текст для поиска: ")

    if run_command_and_check_text(command, text):
        print("Текст найден в выводе команды!")
    else:
        print("Текст не найден или команда завершилась с ошибкой.")
