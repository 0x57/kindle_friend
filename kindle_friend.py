import os
import sys
from collections import defaultdict
CLIPPINGS_FILE = "/Volumes/Kindle/documents/My Clippings.txt"


def extract_notes():
    notes_dict = defaultdict(set)
    with open(CLIPPINGS_FILE, 'r', encoding='utf-8-sig') as f:
        item_list = []
        for line in f:
            item_list.append(line.rstrip())
            if len(item_list) == 5:
                book_name = item_list[0].split(' (')[0]
                notes_dict[book_name].add(item_list[3])
                item_list = []
    return notes_dict


def merge_data(dist_dir, notes_dict):
    for book_name, note_set in notes_dict.items():
        book_path = os.path.join(dist_dir, book_name) + '.txt'
        if os.path.exists(book_path):
            book_note_set = set()
            with open(book_path, 'r') as f:
                for line in f:
                    if line.rstrip():
                        book_note_set.add(line.rstrip())
            note_set = note_set - book_note_set
        if note_set:
            with open(book_path, 'a') as f:
                f.write('\n\n'.join(note_set))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception('存储目录未提供！使用方法：python3 kindle_friend.py 存储目录')
    dist_dir = sys.argv[1]
    notes_dict = extract_notes()
    merge_data(dist_dir, notes_dict)
