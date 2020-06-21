import pandas as pd
import numpy as np
import pickle


def pickle_dump(obj, path):
    with open(path, mode='wb') as f:
        pickle.dump(obj, f)


def pickle_load(path):
    with open(path, mode='rb') as f:
        data = pickle.load(f)
        return data


def keyerror(row, i):
    try:
        row[i]
        return row[i]
    except KeyError:
        return 40000


def lkeyerror(row, i):
    try:
        row[i]
        return row[i]
    except KeyError:
        return None


def pkeyerror(dis, key):
    try:
        dis.pop(key)
        return dis.pop(key)
    except KeyError:
        return dis


def xkeyerror(row, i):
    try:
        row[i]
        return row[i]
    except KeyError:
        return 0.


def ckeyerror(df, i):
    try:
        df[i]
        return 1.
    except KeyError:
        return 0.


def scope(df, max_dist):
    df_temp = df.copy()
    df_temp = df_temp.where(df_temp < max_dist)
    df_temp.insert(0, 'count', df_temp.count(axis=1))
    df_temp = df_temp.fillna(40000)
    df_temp = df_temp.sort_values('count')
    df_temp = df_temp.reset_index()
    return df_temp


def distance(df):
    df_x = pd.DataFrame()
    df_y = pd.DataFrame()
    df_x = df_x.append([df['x']]*len(df), ignore_index=True)
    df_y = df_y.append([df['y']]*len(df), ignore_index=True)
    df_xt = df_x.T
    df_yt = df_y.T
    df_temp = (df_x-df_xt)**2+(df_y-df_yt)**2
    df_temp = df_temp.where(df_temp > 0.000000001)
    df_temp = np.sqrt(df_temp)
    df_temp = df_temp.fillna(40000)
    return df_temp


pd.set_option('display.max_rows', 150)
df = pd.read_csv('input_0.csv')
df_dist = distance(df)
dis = {}
max_dist = 400
while len(df_dist) != 0:
    print(len(dis))
    print(max_dist)
    df_45 = scope(df_dist, max_dist)
    print(dis)
    print(df_45)
    print(df_dist)
    # print(df_45)
    if df_45['count'][0] == 2:
        for index, row in df_45.iterrows():
            if not row['count'] == 2:
                max_dist -= 1
                break
            # print(str(row['index']))
            e = ckeyerror(df_dist, int(row['index']))
            if e != 0.:
                list_temp = []
                for i in range(len(df)):
                    a = keyerror(row, i)
                    if a < max_dist:
                        list_temp += [i]
                if len(list_temp) < 2:
                    max_dist -= 1
                    print('list_errorrrrrrrrrrrrr')
                    break
                b = xkeyerror(dis, list_temp[0])
                d = xkeyerror(dis, list_temp[1])
                if b == 0.:
                    dis[int(row['index'])] = list_temp[1]
                    dis[list_temp[0]] = int(row['index'])
                    df_dist = df_dist.drop(index=[int(row['index'])])
                    df_dist = df_dist.drop(columns=list_temp[1], axis=1)
                    df_dist = df_dist.drop(index=list_temp[0])
                    df_dist = df_dist.drop(columns=int(row['index']), axis=1)
                    break
                elif b != 0. and d == 0.:
                    c = list_temp[1]
                    list_temp[1] = list_temp[0]
                    list_temp[0] = c
                    dis[int(row['index'])] = list_temp[1]
                    dis[list_temp[0]] = int(row['index'])
                    df_dist = df_dist.drop(index=[int(row['index'])])
                    df_dist = df_dist.drop(columns=list_temp[1], axis=1)
                    df_dist = df_dist.drop(index=list_temp[0])
                    df_dist = df_dist.drop(columns=int(row['index']), axis=1)
                    break

    elif df_45['count'][0] == 1:
        for index, row in df_45.iterrows():
            for i in range(len(df)):
                a = keyerror(row, i)
                if a < max_dist:
                    print('A*30')
                    dis[int(row['index'])] = i
                    df_dist = df_dist.drop(index=[int(row['index'])])
                    df_dist = df_dist.drop(columns=i, axis=1)
                    break
            max_dist += 1
            break
    elif df_45['count'][0] == 0:
        max_dist += 1
    else:
        print(len(dis))
        max_dist -= 0.1


df_index = df_45.iloc[:, 0: 2]
df_value = df_45.iloc[:, 2:]
print(dis)
pickle_dump(dis, './dis.pickle')

# dis = pickle_load('./dis.pickle')
# print(dis)

dis_list = []
key_1 = None
while dis:
    key = key_1
    if not key:
        key = next(iter(dis))
    dis_list += [key]
    print(key)
    key_1 = lkeyerror(dis, key)
    pkeyerror(dis, key)
dis_list = list(dict.fromkeys(dis_list))

with open('solution_yours_0.csv', 'w') as f:
    f.write('index'+'\n')
    for ans in dis_list:
        f.write(str(ans)+'\n')
