import multiprocessing
import subprocess
import uvicorn

# Функция для запуска Telegram бот сервиса
def run_telegram_bot_service():
    subprocess.run(["python", "bot/bot.py"])

# Функция для запуска видео обработки сервиса
def run_video_processing_service():
    uvicorn.run("video_processor.processor:app", host="127.0.0.1", port=8001)


# Функция для запуска генерации презентации сервиса
def run_presentation_generation_service():
    uvicorn.run("presentation_generator.generator:app", host="127.0.0.1", port=8002)

if __name__ == "__main__":
    # Создаем процессы для каждого сервиса
    telegram_bot_process = multiprocessing.Process(target=run_telegram_bot_service)
    video_processing_process = multiprocessing.Process(target=run_video_processing_service)
    presentation_generation_process = multiprocessing.Process(target=run_presentation_generation_service)

    # Запускаем процессы
    telegram_bot_process.start()
    video_processing_process.start()
    presentation_generation_process.start()

    # Ждем завершения процессов
    telegram_bot_process.join()
    video_processing_process.join()
    presentation_generation_process.join()
