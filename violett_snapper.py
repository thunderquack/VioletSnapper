import cv2
import time

# Инициализация видеопотоков для двух камер
camera_0 = cv2.VideoCapture(0)
camera_1 = cv2.VideoCapture(1)

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

    cameras = list_available_cameras()
    if cameras:
        print(f"Доступные камеры: {cameras}")

    print("Запуск захвата изображений с нескольких веб-камер...")
    try:
        while True:
            # Захват кадров с каждой камеры
            capture_frame(camera_0, 0)
            capture_frame(camera_1, 1)
            time.sleep(20)  # Захват изображений каждые 20 секунд
    except KeyboardInterrupt:
        print("Захват остановлен.")
    finally:
        # Освобождаем видеопотоки
        camera_0.release()
        camera_1.release()
        cv2.destroyAllWindows()
