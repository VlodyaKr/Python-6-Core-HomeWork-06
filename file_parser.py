import sys
from pathlib import Path

ARCHIVES = []
AUDIO = []
DOCUMENTS = []
IMAGES = []
VIDEO = []
PROGRAMS = []
OTHER = []

REGISTER_EXTENSIONS = {
    'JPEG': IMAGES, 'PNG': IMAGES, 'JPG': IMAGES, 'SVG': IMAGES, 'GIF': IMAGES, 'ICO': IMAGES,
    'MP3': AUDIO, 'OGG': AUDIO, 'WAV': AUDIO, 'AMR': AUDIO, 'FLAC': AUDIO, 'WMA': AUDIO,
    'AVI': VIDEO, 'MP4': VIDEO, 'MOV': VIDEO, 'MKV': VIDEO, 'WMV': VIDEO,
    'DOC': DOCUMENTS, 'DOCX': DOCUMENTS, 'TXT': DOCUMENTS, 'PDF': DOCUMENTS, 'XLSX': DOCUMENTS, 'PPTX': DOCUMENTS, 'RTF': DOCUMENTS,
    'BAT': PROGRAMS, 'CMD': PROGRAMS, 'EXE': PROGRAMS, 'C': PROGRAMS, 'CPP': PROGRAMS, 'JS': PROGRAMS, 'PY': PROGRAMS, 'VBS': PROGRAMS,
    'ZIP': ARCHIVES, 'GZ': ARCHIVES, 'TAR': ARCHIVES
}

FOLDERS = []
EXTENSIONS = set()
UNKNOWN = set()


def get_extension(filename: str) -> str:
    # превращаем расширение файла в название папки .jpg -> JPG
    return Path(filename).suffix[1:].upper()


def scan(folder: Path) -> None:
    for item in folder.iterdir():
        # Если это папка то добавляем ее с список FOLDERS и преходим к следующему элементу папки
        if item.is_dir():
            # проверяем, чтобы папка не была той в которую мы складываем уже файлы
            if item.name not in ('archives', 'video', 'audio', 'documents', 'images', 'programs', 'OTHER'):
                FOLDERS.append(item)
                #  сканируем эту вложенную папку - рекурсия
                scan(item)
            #  перейти к следующему элементу в сканируемой папке
            continue

        #  Пошла работа с файлом
        ext = get_extension(item.name)  # взять расширение
        fullname = folder / item.name  # взять полный путь к файлу
        if not ext:  # если у файла нет расширения добавить к неизвестным
            OTHER.append(fullname)
        else:
            try:
                # взять список куда положить полный путь к файлу
                container = REGISTER_EXTENSIONS[ext]
                EXTENSIONS.add(ext)
                container.append(fullname)
            except KeyError:
                # Если мы не регистрировали расширение в REGISTER_EXTENSIONS, то добавить в другое
                UNKNOWN.add(ext)
                OTHER.append(fullname)


if __name__ == '__main__':
    folder_for_scan = sys.argv[1]
    print(f'Start in folder {folder_for_scan}')

    scan(Path(folder_for_scan))
    print(f'Images: {IMAGES}')
    print(f'Audio: {AUDIO}')
    print(f'Video: {VIDEO}')
    print(f'Documents: {DOCUMENTS}')
    print(f'Programs: {PROGRAM}')
    print(f'Archives: {ARCHIVES}')
    print(f'Others: {OTHER}')

    print(f'Types of files in folder: {EXTENSIONS}')
    print(f'Unknown files of types: {UNKNOWN}')

    print(FOLDERS[::-1])
