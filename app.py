import multiprocessing
import subprocess
import click
import platform

# Функция для запуска процессов в новом окне консоли (только для Windows)
def run_in_new_console(command):
    if platform.system() == "Windows":
        subprocess.run(f'start cmd /K "{command}"', shell=True)
    else:
        raise NotImplementedError("Эта функция поддерживается только на Windows.")

# Функция для запуска Telegram бот сервиса
def run_telegram_bot_service():
    run_in_new_console("python bot/bot.py")

# Функция для запуска видео обработки сервиса
def run_video_processing_service():
    run_in_new_console("uvicorn video_processor.processor:app --host 127.0.0.1 --port 8001")

# Функция для запуска генерации презентации сервиса
def run_presentation_generation_service():
    run_in_new_console("uvicorn presentation_generator.generator:app --host 127.0.0.1 --port 8002")

@click.group()
def main():
    pass

@main.command()
def start_all():
    """Запуск всех сервисов"""
    telegram_bot_process = multiprocessing.Process(target=run_telegram_bot_service)
    video_processing_process = multiprocessing.Process(target=run_video_processing_service)
    presentation_generation_process = multiprocessing.Process(target=run_presentation_generation_service)

    telegram_bot_process.start()
    video_processing_process.start()
    presentation_generation_process.start()

    telegram_bot_process.join()
    video_processing_process.join()
    presentation_generation_process.join()

@main.command()
def stop_all():
    """Остановка всех сервисов"""
    for process in multiprocessing.active_children():
        process.terminate()

@main.command()
def start_tg():
    """Запуск Telegram бот сервиса"""
    telegram_bot_process = multiprocessing.Process(target=run_telegram_bot_service)
    telegram_bot_process.start()
    telegram_bot_process.join()

@main.command()
def stop_tg():
    """Остановка Telegram бот сервиса"""
    for process in multiprocessing.active_children():
        if process.name == "Process-1":  # Название процесса по умолчанию для первого создаваемого процесса
            process.terminate()
            process.join(timeout=5)
            if not process.is_alive():
                print("Сервис Telegram бота успешно остановлен.")
            else:
                print("Не удалось остановить сервис Telegram бота.")
                print("Попробуйте остановить сервис вручную.")

@main.command()
def start_video():
    """Запуск сервиса обработки видео"""
    video_processing_process = multiprocessing.Process(target=run_video_processing_service)
    video_processing_process.start()
    video_processing_process.join()

@main.command()
def stop_video():
    """Остановка сервиса обработки видео"""
    for process in multiprocessing.active_children():
        if process.name == "Process-2":  # Название процесса по умолчанию для второго создаваемого процесса
            process.terminate()

@main.command()
def start_presentation():
    """Запуск сервиса генерации презентаций"""
    presentation_generation_process = multiprocessing.Process(target=run_presentation_generation_service)
    presentation_generation_process.start()
    presentation_generation_process.join()

@main.command()
def stop_presentation():
    """Остановка сервиса генерации презентаций"""
    for process in multiprocessing.active_children():
        if process.name == "Process-3":  # Название процесса по умолчанию для третьего создаваемого процесса
            process.terminate()

if __name__ == "__main__":
    main()
