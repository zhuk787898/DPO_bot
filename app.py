import multiprocessing
import subprocess
import click
import os
from pathlib import Path

# Функция для запуска процессов в новом окне консоли (только для Windows)
def run_in_new_console(command):
    subprocess.run(f'start cmd /K "{command}"', shell=True)

# Функция для запуска Telegram бот сервиса
def run_telegram_bot_service():
    run_in_new_console("python bot/bot.py")

# Функция для запуска видео обработки сервиса
def run_video_processing_service():
    run_in_new_console("uvicorn video_processor.processor:app --host 127.0.0.1 --port 8001")

# Функция для запуска генерации презентации сервиса
def run_presentation_generation_service():
    run_in_new_console("uvicorn presentation_generator.generator:app --host 127.0.0.1 --port 8002")

# Создание процессов для каждого сервиса
telegram_bot_process = multiprocessing.Process(target=run_telegram_bot_service)
video_processing_process = multiprocessing.Process(target=run_video_processing_service)
presentation_generation_process = multiprocessing.Process(target=run_presentation_generation_service)

@click.group()
def main():
    pass

@main.command()
def start_all():
    """Запуск всех сервисов"""
    if not telegram_bot_process.is_alive():
        telegram_bot_process.start()
    if not video_processing_process.is_alive():
        video_processing_process.start()
    if not presentation_generation_process.is_alive():
        presentation_generation_process.start()


@main.command()
def stop_all():
    """Остановка всех сервисов"""
    if telegram_bot_process.is_alive():
        telegram_bot_process.terminate()
    if video_processing_process.is_alive():
        video_processing_process.terminate()
    if presentation_generation_process.is_alive():
        presentation_generation_process.terminate()

@main.command()
def start_tg():
    """Запуск Telegram бот сервиса"""
    if not telegram_bot_process.is_alive():
        telegram_bot_process.start()


@main.command()
def stop_tg():
    """Остановка Telegram бот сервиса"""
    if telegram_bot_process.is_alive():
        telegram_bot_process.terminate()


@main.command()
def start_video():
    """Запуск сервиса обработки видео"""
    if not video_processing_process.is_alive():
        video_processing_process.start()

@main.command()
def stop_video():
    """Остановка сервиса обработки видео"""
    if video_processing_process.is_alive():
        video_processing_process.terminate()

@main.command()
def start_presentation():
    """Запуск сервиса генерации презентаций"""
    if not presentation_generation_process.is_alive():
        presentation_generation_process.start()

@main.command()
def stop_presentation():
    """Остановка сервиса генерации презентаций"""
    if presentation_generation_process.is_alive():
        presentation_generation_process.terminate()

if __name__ == "__main__":
    main()
