import os
from datetime import datetime
import shutil
from tqdm import tqdm

def sort_photos_by_date(base_directory):
    # Считаем общее количество файлов для сортировки
    total_files = sum(len(files) for _, _, files in os.walk(base_directory))
    
    # Создаем прогресс-бар
    with tqdm(total=total_files, desc="Сортировка файлов", ncols=100) as pbar:
        # Проходим по каждой папке камеры
        for root, dirs, files in os.walk(base_directory):
            for file_name in files:
                # Игнорируем системные файлы (если есть)
                if not file_name.endswith(".jpg"):
                    pbar.update(1)
                    continue

                # Получаем полный путь к файлу
                file_path = os.path.join(root, file_name)

                # Извлекаем временную метку из имени файла (формат: camera_id_YYYYMMDD_HHMMSS.jpg)
                try:
                    timestamp_str = file_name.split('_')[1]  # YYYYMMDD_HHMMSS
                    date_str = timestamp_str[:8]  # YYYYMMDD
                    date_obj = datetime.strptime(date_str, "%Y%m%d")
                    date_folder = date_obj.strftime("%Y-%m-%d")
                except (IndexError, ValueError):
                    print(f"Не удалось извлечь дату из имени файла: {file_name}. Пропуск.")
                    pbar.update(1)
                    continue

                # Определяем папку с датой для перемещения файла
                camera_folder = os.path.basename(root)  # Получаем имя папки камеры (например, camera_0)
                date_directory = os.path.join(base_directory, camera_folder, date_folder)

                # Создаем папку с датой, если она не существует
                if not os.path.exists(date_directory):
                    os.makedirs(date_directory)

                # Перемещаем файл в папку с датой
                new_file_path = os.path.join(date_directory, file_name)
                shutil.move(file_path, new_file_path)
                pbar.update(1)  # Обновляем прогресс-бар после перемещения файла

    print("Сортировка завершена.")

if __name__ == "__main__":
    # Задаем базовую директорию, где хранятся фотографии
    base_directory = "captured_images"
    
    # Проверяем и сортируем фотографии по папкам с датами
    sort_photos_by_date(base_directory)
