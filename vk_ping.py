import vk_api
import random
from settings import keys_tables, key_field_name, key_column_name, done_text, done_column_name, group_prefix, invalid_text, student_column_name
from vk_settings import token_config, peer_id_config, head_boy_config
from google_sheets_reader import GoogleSheetsReader


def get_stat(key_table):
    result = {}
    current_group = None
    sheet = GoogleSheetsReader.get_worksheet(key_table, 0)
    cell_list = sheet.range('{0}3:{1}{2}'.format(student_column_name, done_column_name, sheet.row_count))
    for i in range(0, len(cell_list) - 1, 3):
        if group_prefix in cell_list[i].value:
            current_group = cell_list[i].value
            result[current_group] = []
            continue
        if cell_list[i + 2].value not in (done_text, invalid_text):
            result[current_group].append(cell_list[i + 1].value)
    return result


def get_stat_by_head_boy(course):
    real_result = {}
    stat = get_stat(keys_tables[course])
    groups = head_boy_config[course].keys()

    for group in groups:
        real_result[group] = []

    for group, ids in stat.items():
        for real_group in groups:
            if real_group in group:
                real_result[real_group].extend(ids)
                break

    return real_result


def get_pretty_text(course):
    stat = get_stat_by_head_boy(course)
    head_boys_to_group = head_boy_config[course]
    groups = sorted(head_boys_to_group.keys())
    text = 'Привет всем! Статистика заполнения формы:'
    for group in groups:
        if not stat[group]:
            continue

        text += f"\n{head_boys_to_group[group]} в твоей группе ({group}) осталось {len(stat[group])} айдишников: "
        text += ' '.join(stat[group])
    return text


def send_message_to_group(course):
    text = get_pretty_text(course)
    vk_session = vk_api.VkApi(token=token_config[4])
    vk = vk_session.get_api()
    vk.messages.send(message=text, peer_id=peer_id_config[course], random_id=random.randint(0, 2 ** 30))


send_message_to_group(4)
