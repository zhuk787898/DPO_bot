from fastapi import FastAPI, File, UploadFile
import cv2
import os

import cv2

def extract_frames(video_path):
    frames = []
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError("Unable to open video file")

    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_count += 1
        if frame_count % 30 == 0:
            frames.append(frame)

    cap.release()
    return frames


app = FastAPI()

@app.post("/process/")
async def process_video(file: UploadFile = File(...)):
    file_location = f"temp_{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())

    # Обработка видео и извлечение информации (например, распознавание объектов)
    # Получаем каждый 30-ый кадр
    frames = extract_frames(file_location)
    
    output_folder = f"C:\DPO\ishodniki\{file.filename}"
    os.makedirs(output_folder, exist_ok=True)

    # Сохраняем каждый кадр в папку
    for i, frame in enumerate(frames):
        frame_path = os.path.join(output_folder, f"frame_{i}.jpg")
        cv2.imwrite(frame_path, frame)    


    os.remove(file_location)

    return {"photos_folder_path": output_folder}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
