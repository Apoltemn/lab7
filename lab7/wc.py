import argparse
import sys
import os

def count_file_stats(filename):
    filename = filename.strip('"')
    filename = os.path.abspath(filename)
    if not os.path.exists(filename):
        print(f"Ошибка: файл '{filename}' не найден.", file=sys.stderr)
        return None
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            text = file.read()
            lines = text.splitlines()
            words = text.split()
            return {
                'filename': filename,
                'lines': len(lines),
                'words': len(words),
                'chars': len(text)
            }
    except Exception as e:
        print(f"Ошибка при чтении файла '{filename}': {e}", file=sys.stderr)
        return None

def main():
    parser = argparse.ArgumentParser(description='Аналог утилиты wc для нескольких файлов')
    parser.add_argument('files', nargs='*', help='Имена файлов')
    parser.add_argument('--l', '--lines', action='store_true', help='Подсчёт строк')
    parser.add_argument('--w', '--words', action='store_true', help='Подсчёт слов')
    parser.add_argument('-c', '--chars', action='store_true', help='Подсчёт символов')
    args = parser.parse_args()

    if not args.files:
        args.files = input("Введите пути к файлам через пробел: ").strip('"').split()

    total = {'lines': 0, 'words': 0, 'chars': 0}
    valid_files = 0

    for file in args.files:
        stats = count_file_stats(file)
        if stats:
            valid_files += 1
            if not any([args.l, args.w, args.chars]):
                print(f"{stats['filename']}: Строк: {stats['lines']}, Слов: {stats['words']}, Символов: {stats['chars']}")
            else:
                if args.l: print(f"{stats['filename']}: Строк: {stats['lines']}")
                if args.w: print(f"{stats['filename']}: Слов: {stats['words']}")
                if args.chars: print(f"{stats['filename']}: Символов: {stats['chars']}")
            total['lines'] += stats['lines']
            total['words'] += stats['words']
            total['chars'] += stats['chars']

    if valid_files > 1:
        print("\nОбщий итог:")
        print(f"Строк: {total['lines']}, Слов: {total['words']}, Символов: {total['chars']}")

if __name__ == "__main__":
    main()