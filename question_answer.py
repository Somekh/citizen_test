import pandas as pd
import time


def ask_question(df: pd.DataFrame, index) -> bool:
    print(df.loc[index, 'question'].iloc[0])
    for ch in df.loc[index]['choices'].iloc[0]:
        print(ch)
    time.sleep(0.5)
    ans = input('your_answer: ')
    return int(ans) == df.loc[index, 'correct'].iloc[0]


def ans_process(df, index, ans_bool, verbose=False):
    try:
        if ans_bool:
            if verbose:
                print('GOOD! correct_answer')
            df.loc[index, 'times_correct_answered'] += 1
        else:
            if verbose:
                print('WRONG!')
                print(f'Correct answer was {df.loc[index, "correct"].iloc[0]}')
    except:
        if verbose:
            print('Error')

    df.loc[index, 'times_answered'] += 1
    df.loc[index, 'statistics'] = df.loc[index, 'times_correct_answered'] / df.loc[index, 'times_answered']
