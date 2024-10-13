import cv2
import time
import os
from tqdm import tqdm

def capture_frame(camera, camera_id, base_save_dir):
    ret, frame = camera.read()
    if ret:
        # Создаем папку для каждой камеры
        camera_save_dir = os.path.join(base_save_dir, f"camera_{camera_id}")
        if not os.path.exists(camera_save_dir):
            os.makedirs(camera_save_dir)

        # Сохранение кадра с временной меткой
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(camera_save_dir, f"{timestamp}.jpg")
        cv2.imwrite(filename, frame)
        print(f"Сохранено: {filename}")
    else:
        print(f"Не удалось захватить кадр с камеры {camera_id}")

def list_available_cameras(max_cameras=10):
    available_cameras = []
    for index in range(max_cameras):
        cap = cv2.VideoCapture(index)
        if cap.isOpened():
            available_cameras.append(index)
            cap.release()
    return available_cameras        

def countdown_timer_with_progress(seconds):
    for _ in tqdm(range(seconds), desc="До следующего кадра", ncols=100):
        time.sleep(1)

if __name__ == "__main__":
    # Базовая директория для сохранения фотографий
    base_save_directory = "captured_images"
    
    # Создаем базовую директорию, если она не существует
    if not os.path.exists(base_save_directory):
        os.makedirs(base_save_directory)

    # Получаем список доступных камер
    camera_indices = list_available_cameras()
    if not camera_indices:
        print("Камеры не обнаружены.")
        exit()

    print(f"Доступные камеры: {camera_indices}")

    # Инициализация видеопотоков для всех доступных камер
    cameras = [cv2.VideoCapture(index) for index in camera_indices]

    print("Запуск захвата изображений с нескольких веб-камер...")
    try:
        while True:
            # Захват кадров с каждой камеры
            for i, camera in enumerate(cameras):
                capture_frame(camera, camera_indices[i], base_save_directory)
            countdown_timer_with_progress(20)  # Обратный отсчет с прогресс-баром
    except KeyboardInterrupt:
        print("Захват остановлен.")
    finally:
        # Освобождаем все видеопотоки
        for camera in cameras:
            camera.release()
        cv2.destroyAllWindows()
