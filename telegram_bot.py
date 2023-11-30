import telebot
import pandas as pd
import sqlite3
from source_prepare import get_question_index
from question_answer import ans_process
from telebot.types import ReplyKeyboardMarkup

df = pd.read_parquet('df_cur.parquet')
bot = telebot.TeleBot('6581539013:AAEW5fTz4znVaUljEYPOkoyb9IZ9jgOTOBQ')


@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('sq3_db.sql')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, '
                'name varchar(50), '
                'pass varchar(50))')
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id,
                     f'Привет {message.from_user.first_name} ! Предлагаю изучить'
                     f' тесты по грузинскому языку для получения граданства Грузии')


index = get_question_index(df)


def on_click(message):
    global index, df
    try:
        ans = int(message.text)
    except:
        ans = 5

    check_ans = (ans == df.loc[index, "correct"].iloc[0])
    if check_ans:
        bot.send_message(message.chat.id, 'Correct')
    else:
        bot.send_message(message.chat.id, f'False, correct answer is {df.loc[index, "correct"].iloc[0]}')
    ans_process(df, index, check_ans)
    bot.send_message(
        message.chat.id, f'stats {df.loc[index, "times_correct_answered"].iloc[0]} '
                         f'/ {df.loc[index, "times_answered"].iloc[0]}'
                         f' \n total answers {df.times_answered.sum()}')

    df.to_parquet('df_cur.parquet')
    df = pd.read_parquet('df_cur.parquet')

    index = get_question_index(df)
    bot.register_next_step_handler(message, main)


@bot.message_handler(commands=['question'])
def main(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    bot.send_message(message.chat.id, df.loc[index, 'question'].iloc[0])
    markup.add('next_question')
    for i, ch in enumerate(df.loc[index]['choices'].iloc[0][:-1]):
        markup.add(str(i + 1))
        bot.send_message(message.chat.id, df.loc[index, 'choices'].iloc[0][i])
    markup.add(str(len(df.loc[index]['choices'].iloc[0])))
    bot.send_message(message.chat.id, df.loc[index, 'choices'].iloc[0][-1], reply_markup=markup)
    bot.register_next_step_handler(message, on_click)


bot.polling(none_stop=True)
