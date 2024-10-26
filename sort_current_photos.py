import os
from datetime import datetime
import shutil
from tqdm import tqdm

def sort_photos_by_date(base_directory):
    # Считаем общее количество файлов для сортировки (только второго уровня)
    total_files = sum(len(files) for camera_folder in os.listdir(base_directory) 
                      if os.path.isdir(os.path.join(base_directory, camera_folder)) 
                      for files in [os.listdir(os.path.join(base_directory, camera_folder))])

    # Создаем прогресс-бар
    with tqdm(total=total_files, desc="Сортировка файлов", ncols=100) as pbar:
        # Проходим по каждой папке камеры (второй уровень)
        for camera_folder in os.listdir(base_directory):
            camera_folder_path = os.path.join(base_directory, camera_folder)
            if not os.path.isdir(camera_folder_path):
                continue
            
            # Проверяем файлы только в этой папке, игнорируя третий уровень
            for file_name in os.listdir(camera_folder_path):
                file_path = os.path.join(camera_folder_path, file_name)
                
                # Игнорируем файлы, которые не являются изображениями JPG
                if not file_name.endswith(".jpg") or not os.path.isfile(file_path):
                    pbar.update(1)
                    continue

                # Извлекаем дату из имени файла (формат: YYYYMMDD_HHMMSS.jpg)
                try:
                    date_str = file_name.split('_')[0]  # YYYYMMDD
                    date_obj = datetime.strptime(date_str, "%Y%m%d")
                    date_folder = date_obj.strftime("%Y-%m-%d")
                except (IndexError, ValueError):
                    print(f"Не удалось извлечь дату из имени файла: {file_name}. Пропуск.")
                    pbar.update(1)
                    continue

                # Определяем папку с датой для перемещения файла
                date_directory = os.path.join(camera_folder_path, date_folder)

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
