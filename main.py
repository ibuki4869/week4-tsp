import pandas as pd
"""
最初のコード
"""


def keyerror(group_df_x, i, j):
    try:
        group_df_x.get_group((i, j))
        return group_df_x.get_group((i, j))
    except KeyError:
        return []


def distance(infile, outfile):
    df = pd.read_csv(infile)
    df_x = pd.DataFrame(
        {"x_int": df['x'], "x": df['x'], 'y_int': df['y'], "y": df['y']})
    df_x['x_int'] = df_x['x_int']*0.01
    df_x['y_int'] = df_x['y_int']*0.01
    df_x['x_int'] = df_x['x_int'].astype(int)
    df_x['y_int'] = df_x['y_int'].astype(int)
    df_x = df_x.sort_values(['x_int', 'y_int'])
    group_df_x = df_x.groupby(['x_int', 'y_int'])
    x_max = df_x['x_int'].max()
    y_max = df_x['y_int'].max()
    index_list = []
    for i in range(x_max+1):
        index_sub = []
        for j in range(1, y_max+1):
            df_sub = keyerror(group_df_x, i, j)
            if len(df_sub) != 0:
                df_sub = df_sub.sort_values('y')
                index_sub += list(df_sub.index)
        if i % 2 == 0:
            index_list += index_sub
        else:
            index_list += reversed(index_sub)
    index_sub = []
    for k in range(x_max+1):
        df_sub = keyerror(group_df_x, k, 0)
        if not len(df_sub) == 0:
            df_sub = df_sub.sort_values('x')
            index_sub += list(df_sub.index)
    index_list += reversed(index_sub)
    index_list = [str(int(o)) for o in index_list]
    with open(outfile, 'w') as f:
        f.write('index'+'\n')
        for ans in index_list:
            f.write(ans+'\n')


if __name__ == '__main__':
    distance('input_0.csv', 'solution_yours_0.csv')
    distance('input_1.csv', 'solution_yours_1.csv')
    distance('input_2.csv', 'solution_yours_2.csv')
    distance('input_3.csv', 'solution_yours_3.csv')
    distance('input_4.csv', 'solution_yours_4.csv')
    distance('input_5.csv', 'solution_yours_5.csv')
    distance('input_6.csv', 'solution_yours_6.csv')
