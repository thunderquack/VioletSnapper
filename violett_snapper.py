import cv2
import time

def capture_frame(camera, camera_id):
    ret, frame = camera.read()
    if ret:
        # Сохранение кадра с временной меткой и идентификатором камеры
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"camera_{camera_id}_{timestamp}.jpg"
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

if __name__ == "__main__":
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
                capture_frame(camera, camera_indices[i])
            time.sleep(20)  # Захват изображений каждые 20 секунд
    except KeyboardInterrupt:
        print("Захват остановлен.")
    finally:
        # Освобождаем все видеопотоки
        for camera in cameras:
            camera.release()
        cv2.destroyAllWindows()
