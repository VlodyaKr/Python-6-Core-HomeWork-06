from pathlib import Path
import shutil
import sys
import file_parser as parser
from normalize import normalize


def handle_media(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / (normalize(filename.stem) + filename.suffix))


def handle_other(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / (normalize(filename.stem) + filename.suffix))


def handle_archive(filename: Path, target_folder: Path):
    # Создаем папку для архивов
    target_folder.mkdir(exist_ok=True, parents=True)
    #  Создаем папку куда распаковываем архив
    # Берем суффикс у файла и убираем replace(filename.suffix, '')
    folder_for_file = target_folder / \
        normalize(filename.name.replace(filename.suffix, ''))
    #  создаем папку для архива с именем файла

    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(str(filename.resolve()),
                              str(folder_for_file.resolve()))
    except shutil.ReadError:
        print(f'Обман - это не архив {filename}!')
        folder_for_file.rmdir()
        return None
    filename.unlink()


def handle_folder(folder: Path):
    try:
        folder.rmdir()
    except OSError:
        print(f'Не удалось удалить папку {folder}')


def main(folder: Path):
    parser.scan(folder)

    for file in parser.IMAGES:
        handle_media(file, folder / 'images' / parser.get_extension(file))
    for file in parser.AUDIO:
        handle_media(file, folder / 'audio' / parser.get_extension(file))
    for file in parser.VIDEO:
        handle_media(file, folder / 'video' / parser.get_extension(file))
    for file in parser.DOCUMENTS:
        handle_media(file, folder / 'documents' / parser.get_extension(file))

    for file in parser.OTHER:
        if parser.get_extension(file) == normalize(parser.get_extension(file)):
            handle_other(file, folder / 'OTHER' / parser.get_extension(file))
        else:
            handle_other(file, folder / 'BAD EXTENSIONS')

    for file in parser.ARCHIVES:
        handle_archive(file, folder / 'archives')

    # Выполняем реверс списка для того, чтобы все папки удалить.
    for folder in parser.FOLDERS[::-1]:
        handle_folder(folder)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('''
        Ви не зазначили обов'язковий параметр Source - папку для обробки
        Формат запуску:
        py main.py Source [NOEXT]
        ''')
        exit(0)
    if sys.argv[1]:
        folder_for_scan = Path(sys.argv[1])
        print(f'Start in folder {folder_for_scan.resolve()}')
        main(folder_for_scan.resolve())


# cat.jpg  cat.JPG
