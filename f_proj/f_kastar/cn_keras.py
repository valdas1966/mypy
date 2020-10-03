import pandas as pd
import numpy as np
from f_ds import u_fe
from f_ds import u_fs
from f_ds import u_train_test
from f_utils import u_pickle
from f_ds import u_keras


csv_data = 'D:\\MyPy\\f_astar\\experiments\\results_kastar_lookup_5.csv'
pickle_df_keras = 'D:\\MyPy\\f_astar\\experiments\\df_keras.pickle'
pickle_model_keras = 'D:\\MyPy\\f_astar\\experiments\\model_keras.pickle'
pickle_train_test_keras = 'D:\\MyPy\\f_astar\\experiments\\train_test_keras.pickle'
csv_pred = 'D:\\MyPy\\f_astar\\experiments\\pred_5.csv'


def create_df_keras():
    df = pd.read_csv(csv_data)
    df = df[df['forward'] > df['d']]
    df['label'] = df['backward'] / df['forward']
    cols_select = ['rows', 'cols', 'row_start', 'col_start', 'row_goal_near']
    cols_select += ['col_goal_near', 'row_goal_far', 'col_goal_far']
    cols_select += ['distance_start_goal_near', 'distance_start_goal_far']
    cols_select += ['distance_between_goals', 'f_goal_near', 'closed']
    cols_select += ['nearest_closed_up', 'nearest_closed_right']
    cols_select += ['nearest_closed_down', 'nearest_closed_left', 'label']
    df = df[cols_select]
    df['nearest_closed_up'].replace(float('Infinity'), -1, inplace=True)
    df['nearest_closed_right'].replace(float('Infinity'), -1, inplace=True)
    df['nearest_closed_down'].replace(float('Infinity'), -1, inplace=True)
    df['nearest_closed_left'].replace(float('Infinity'), -1, inplace=True)
    u_pickle.dump(df, pickle_df_keras)


def create_model_keras(df):
    x = df.drop(columns=['label'])
    y = df['label']

    x_train, x_test, y_train, y_test = u_train_test.split(x, y,
                                                          is_classifier=False)
    u_pickle.dump((x_train, x_test, y_train, y_test), pickle_train_test_keras)
    model = u_keras.create_model(x_train, y_train,
                                 layers=[17, 34, 68, 34, 17], dim=17)
    u_pickle.dump(model, pickle_model_keras)

#create_df_keras()

#df = u_pickle.load(pickle_df_keras)
#create_model_keras(df)

df_data = pd.read_csv(csv_data)
x_train, x_test, y_train, y_test = u_pickle.load(pickle_train_test_keras)
model = u_pickle.load(pickle_model_keras)
y_pred = model.predict(x_train)
print(y_pred[:10])

count = 0
for i, (index, row) in enumerate(x_train.iterrows()):
    forward = int(df_data.at[index, 'forward'])
    backward = int(df_data.at[index, 'backward'])
    if y_pred[i] < 1:
        count += backward / forward
    else:
        count += 1
print(count / len(x_train))
