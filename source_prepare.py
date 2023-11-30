import re
import pandas as pd


def txt_to_dict(txt: str):
    # Откройте файл для чтения
    with open(txt, 'r', encoding='utf-8') as file:
        lines = file.read().splitlines()

    # Создайте словарь для хранения данных
    data = {}
    current_question = None
    current_choices = []
    correct_answer = None

    # Итерируйтесь по строкам и заполняйте словарь
    for line in lines:
        line = line.strip()
        if line:
            if re.match(r'\d+\.', line):
                if current_question is not None:
                    data[current_question] = {'choices': current_choices, 'correct': correct_answer}
                current_question = line
                current_choices = []
            elif line.startswith("სწორი პასუხია: "):
                correct_answer = line.split(": ")[1]
            else:
                if ('ა. ' not in line) and ('ბ. ' not in line) and ('გ. ' not in line) and ('დ. ' not in line) and (
                        current_question is not None):
                    current_question += '\n' + line
                else:
                    current_choices.append(line)

    # Добавьте последний элемент в словарь
    if current_question is not None:
        data[current_question] = {'choices': current_choices, 'correct': correct_answer}

    return data


def replace_in_string(list_of_s):
    mapping = {'ა. ': '1.',
               'ბ. ': '2.',
               'გ. ': '3.',
               'დ. ': '4.'}
    ans = []
    for s in list_of_s:
        for key, value in mapping.items():
            s = s.replace(key, str(value))
        ans.append(s)
    return ans


def dict_to_df(dictionary: dict):
    df = pd.DataFrame.from_dict(dictionary, orient='index')
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'question'}, inplace=True)
    df.correct = df.correct.replace({'ა': 1,
                                     'ბ': 2,
                                     'გ': 3,
                                     'დ': 4})

    df.index += 1
    df['choices'] = df.choices.apply(replace_in_string)
    df['statistics'] = 0
    df['times_answered'] = 0
    df['times_correct_answered'] = 0
    return df


def get_question_index(df: pd.DataFrame):
    if (df['times_answered'] < 3).any():
        return df[df['times_answered'] < 3].sample().index
    elif df.times_answered.sum() % 20 == 0:
        return df.sample().index
    else:
        return df.sort_values('statistics').head().sample().index
