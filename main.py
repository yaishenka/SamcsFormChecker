from tqdm import tqdm
from settings import courses, keys_tables, answer_tables, key_field_name, key_column_name, done_text, done_column_name
from google_sheets_reader import GoogleSheetsReader


def get_all_keys(table):
    all_records = GoogleSheetsReader.get_all_records(table, 0)
    keys = set()
    for record in all_records:
        keys.add(record[key_field_name].lower().strip())
    return keys


def get_all_keys_for_course(course):
    keys = set()
    for answer_table in answer_tables[course]:
        keys.update(get_all_keys(answer_table))
    return keys


def check_keys(key_table, keys):
    sheet = GoogleSheetsReader.get_worksheet(key_table, 0)
    cell_list = sheet.range('{0}1:{1}{2}'.format(key_column_name, done_column_name, sheet.row_count))
    for i in range(0, len(cell_list) - 1, 2):
        if not cell_list[i].value:
            continue
        if cell_list[i].value.lower().strip() in keys:
            cell_list[i+1].value = done_text
    sheet.update_cells(cell_list)


def process_course(course):
    keys = get_all_keys_for_course(course)
    check_keys(keys_tables[course], keys)


def main():
    for course in tqdm(courses):
        process_course(course)


if __name__ == "__main__":
    main()
