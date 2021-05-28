import glob
import os
# import tensorflow as tf
import pandas as pd
import numpy as np
import chess 
from sklearn.utils import shuffle

path_fischer = "ChessProject/Dataset/CSV_FISCHER"
path_morphy = "ChessProject/Dataset/CSV_MORPHY"
path_capablanca = "ChessProject/Dataset/CSV_CAPABLANCA" 

# glob: thư viện cho phép đọc các file có tên giống nhau 

files_fischer = glob.glob(path_fischer + "/*.csv")
files_morphy = glob.glob(path_morphy + "/*.csv")
files_capablanca = glob.glob(path_capablanca + "/*.csv")

li = []

for filename in files_fischer:
    df = pd.read_csv(filename, index_col=None, header=0)
    li.append(df)

train = pd.concat(li, axis=0, ignore_index=True)

'''
    Tạo một data frame mới từ data frame đã có:
        64 cột đầu: Mô tả vị trí bàn cờ 
        65-66: mô tả vị trí nước đi 
        67: True, False 
'''

data_length = len(train)

train = train.replace('None', 0.0)
train = train.replace('P', 1.0)
train = train.replace('p',-1.0)
train = train.replace('N', 3.0)
train = train.replace('n',-3.0)
train = train.replace('B', 3.5)
train = train.replace('b',-3.5)
train = train.replace('R', 5.0)
train = train.replace('r',-5.0)
train = train.replace('Q', 9.0)
train = train.replace('q',-9.0)
train = train.replace('K', 10.0)
train = train.replace('k',-10.0)

board_state = list(train.iloc[:, 0:63].columns)
move_from = list(train.iloc[:, 64:128].columns)
move_to = list(train.iloc[:, 128:192])


board_s = train[board_state]
move_f = train[move_from]
move_t = train[move_to]
Y = train['good_move']


# print(move_t.head())
# print(move_f.head())

move_f = move_f.idxmax(axis=1)
move_t = move_t.idxmax(axis=1)

print(move_t.head())
print(move_f.head())

from_dict = {'from_a1':  0.0, 'from_b1':  1.0, 'from_c1':  2.0, 'from_d1':  3.0, 'from_e1':  4.0, 'from_f1':  5.0, 'from_g1':  6.0, 'from_h1':  7.0,
             'from_a2':  8.0, 'from_b2':  9.0, 'from_c2': 10.0, 'from_d2': 11.0, 'from_e2': 12.0, 'from_f2': 13.0, 'from_g2': 14.0, 'from_h2': 15.0,
             'from_a3': 16.0, 'from_b3': 17.0, 'from_c3': 18.0, 'from_d3': 19.0, 'from_e3': 20.0, 'from_f3': 21.0, 'from_g3': 22.0, 'from_h3': 23.0,
             'from_a4': 24.0, 'from_b4': 25.0, 'from_c4': 26.0, 'from_d4': 27.0, 'from_e4': 28.0, 'from_f4': 29.0, 'from_g4': 30.0, 'from_h4': 31.0,
             'from_a5': 32.0, 'from_b5': 33.0, 'from_c5': 34.0, 'from_d5': 35.0, 'from_e5': 36.0, 'from_f5': 37.0, 'from_g5': 38.0, 'from_h5': 39.0,
             'from_a6': 40.0, 'from_b6': 41.0, 'from_c6': 42.0, 'from_d6': 43.0, 'from_e6': 44.0, 'from_f6': 45.0, 'from_g6': 46.0, 'from_h6': 47.0,
             'from_a7': 48.0, 'from_b7': 49.0, 'from_c7': 50.0, 'from_d7': 51.0, 'from_e7': 52.0, 'from_f7': 53.0, 'from_g7': 54.0, 'from_h7': 55.0,
             'from_a8': 56.0, 'from_b8': 57.0, 'from_c8': 58.0, 'from_d8': 59.0, 'from_e8': 60.0, 'from_f8': 61.0, 'from_g8': 62.0, 'from_h8': 63.0,}

to_dict = {'to_a1':  0.0, 'to_b1':  1.0, 'to_c1':  2.0, 'to_d1':  3.0, 'to_e1':  4.0, 'to_f1':  5.0, 'to_g1':  6.0, 'to_h1':  7.0,
           'to_a2':  8.0, 'to_b2':  9.0, 'to_c2': 10.0, 'to_d2': 11.0, 'to_e2': 12.0, 'to_f2': 13.0, 'to_g2': 14.0, 'to_h2': 15.0,
           'to_a3': 16.0, 'to_b3': 17.0, 'to_c3': 18.0, 'to_d3': 19.0, 'to_e3': 20.0, 'to_f3': 21.0, 'to_g3': 22.0, 'to_h3': 23.0,
           'to_a4': 24.0, 'to_b4': 25.0, 'to_c4': 26.0, 'to_d4': 27.0, 'to_e4': 28.0, 'to_f4': 29.0, 'to_g4': 30.0, 'to_h4': 31.0,
           'to_a5': 32.0, 'to_b5': 33.0, 'to_c5': 34.0, 'to_d5': 35.0, 'to_e5': 36.0, 'to_f5': 37.0, 'to_g5': 38.0, 'to_h5': 39.0,
           'to_a6': 40.0, 'to_b6': 41.0, 'to_c6': 42.0, 'to_d6': 43.0, 'to_e6': 44.0, 'to_f6': 45.0, 'to_g6': 46.0, 'to_h6': 47.0,
           'to_a7': 48.0, 'to_b7': 49.0, 'to_c7': 50.0, 'to_d7': 51.0, 'to_e7': 52.0, 'to_f7': 53.0, 'to_g7': 54.0, 'to_h7': 55.0,
           'to_a8': 56.0, 'to_b8': 57.0, 'to_c8': 58.0, 'to_d8': 59.0, 'to_e8': 60.0, 'to_f8': 61.0, 'to_g8': 62.0, 'to_h8': 63.0,}

move_f = move_f.map(from_dict)
move_t = move_t.map(to_dict)

final = [board_s, move_f, move_t, Y]

final_df = pd.concat(final, axis= 1)

print(train.shape)
print(final_df.shape)

final_df.to_csv('ChessProject/Transformed_dataset/Fischer.csv', index= False)