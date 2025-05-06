import argparse
import zipfile
import os
import sys

def list_zip_contents(zip_path):
    try:
        with zipfile.ZipFile(zip_path, 'r') as archive:
            print(f"\nСодержимое архива '{zip_path}':")
            print("-" * 50)
            print("  Дата модификации    Размер    Имя файла")
            print("-" * 50)
            for file in archive.infolist():
                print(f"  {file.date_time[2]:02d}.{file.date_time[1]:02d}.{file.date_time[0]}  "
                      f"{file.file_size:>8} байт  {file.filename}")
    except zipfile.BadZipFile:
        print(f"Ошибка: файл '{zip_path}' не является ZIP-архивом или повреждён!", file=sys.stderr)
        return False
    return True

def extract_zip(zip_path, output_dir):
    try:
        with zipfile.ZipFile(zip_path, 'r') as archive:
            archive.extractall(output_dir)
            print(f"\nАрхив успешно распакован в: {os.path.abspath(output_dir)}")
            return True
    except zipfile.BadZipFile:
        print(f"Ошибка: файл '{zip_path}' не является ZIP-архивом!", file=sys.stderr)
    except PermissionError:
        print(f"Ошибка: нет доступа к папке '{output_dir}'!", file=sys.stderr)
    except Exception as e:
        print(f"Неизвестная ошибка: {e}", file=sys.stderr)
    return False

def create_zip(zip_path, files_to_add):
    missing_files = [f for f in files_to_add if not os.path.exists(f)]
    if missing_files:
        print(f"Ошибка: файлы не найдены - {', '.join(missing_files)}", file=sys.stderr)
        return False

    try:
        with zipfile.ZipFile(zip_path, 'w') as archive:
            for file in files_to_add:
                archive.write(file, os.path.basename(file))
            print(f"\nАрхив создан: {os.path.abspath(zip_path)}")
            print(f"Добавлено файлов: {len(files_to_add)}")
            return True
    except Exception as e:
        print(f"Ошибка при создании архива: {e}", file=sys.stderr)
        return False

def main():
    parser = argparse.ArgumentParser(
        description='Утилита для работы с ZIP-архивами. Поддерживает несколько файлов.',
        epilog='Примеры:\n'
               '  Просмотр:    zip_tool.py -l archive.zip\n'
               '  Распаковка:  zip_tool.py -u archive.zip -o output_dir\n'
               '  Упаковка:    zip_tool.py -p new.zip file1.txt file2.txt'
    )
    
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('-l', '--list', metavar='ZIP_FILE', help='Просмотреть содержимое архива')
    group.add_argument('-u', '--extract', metavar='ZIP_FILE', help='Распаковать архив')
    group.add_argument('-p', '--pack', metavar='ZIP_FILE', help='Создать новый архив')
    
    parser.add_argument('-o', '--output', default='.', help='Папка для распаковки (по умолчанию текущая)')
    parser.add_argument('files', nargs='*', help='Файлы для добавления в архив (для режима -p)')
    
    args = parser.parse_args()

    # Режим просмотра
    if args.list:
        if not list_zip_contents(args.list):
            sys.exit(1)
    
    # Режим распаковки
    elif args.extract:
        if not zipfile.is_zipfile(args.extract):
            print(f"Ошибка: '{args.extract}' не является ZIP-архивом!", file=sys.stderr)
            sys.exit(1)
        if not extract_zip(args.extract, args.output):
            sys.exit(1)
    
    # Режим упаковки
    elif args.pack:
        if not args.files:
            print("Ошибка: не указаны файлы для архивации!", file=sys.stderr)
            sys.exit(1)
        if not create_zip(args.pack, args.files):
            sys.exit(1)
    
    # Интерактивный режим
    else:
        print("\n" + "="*50)
        print("  Режимы работы ZIP-утилиты")
        print("="*50)
        print("1. Просмотреть содержимое архива")
        print("2. Распаковать архив")
        print("3. Создать новый архив")
        print("4. Выход")
        
        while True:
            choice = input("\nВыберите действие (1-4): ").strip()
            
            if choice == '1':
                zip_path = input("Введите путь к архиву: ").strip('"')
                if not os.path.exists(zip_path):
                    print("Ошибка: файл не существует!", file=sys.stderr)
                    continue
                list_zip_contents(zip_path)
            
            elif choice == '2':
                zip_path = input("Введите путь к архиву: ").strip('"')
                if not os.path.exists(zip_path):
                    print("Ошибка: файл не существует!", file=sys.stderr)
                    continue
                output_dir = input("Введите папку для распаковки (по умолчанию .): ").strip('"') or '.'
                extract_zip(zip_path, output_dir)
            
            elif choice == '3':
                zip_path = input("Введите имя нового архива: ").strip('"')
                files = input("Введите пути к файлам через пробел: ").strip('"').split()
                if not files:
                    print("Ошибка: не указаны файлы!", file=sys.stderr)
                    continue
                create_zip(zip_path, files)
            
            elif choice == '4':
                break
            
            else:
                print("Неверный выбор! Введите число от 1 до 4.")

if __name__ == "__main__":
    main()