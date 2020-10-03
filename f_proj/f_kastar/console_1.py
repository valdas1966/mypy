import pandas as pd
import numpy as np
from f_ds import u_fe
from f_ds import u_fs
from f_ds import u_train_test
from f_ds import u_rfc
from f_ds import u_rfr
from f_utils import u_pickle


csv_data = 'G:\\MyPy\\f_astar\\experiments\\results_kastar_lookup_5.csv'
pickle_df_class = 'G:\\MyPy\\f_astar\\experiments\\df_class.pickle'
pickle_model_class = 'G:\\MyPy\\f_astar\\experiments\\model_class.pickle'
pickle_train_test_class = 'G:\\MyPy\\f_astar\\experiments\\train_text_class' \
                          '.pickle'
csv_pred = 'G:\\MyPy\\f_astar\\experiments\\pred_5.csv'


def create_df_class():
    df = pd.read_csv(csv_data)
    df = df[df['forward'] > df['d']]
    df = df[df['forward'] > 10]
    df['label'] = np.where(df['backward'] / df['forward'] < 1, 1, 0)
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
    df_synthetic = u_fe.synthetic(df, columns_to_exclude={'label'})
    df = pd.concat([df, df_synthetic], axis=1)
    df = u_fs.drop_correlated_features(df, 0.99)
    u_pickle.dump(df, pickle_df_class)


def create_model_class(x_train, y_train):
    model = u_rfc.create_model(x_train, y_train, verbose=2)
    u_pickle.dump(model, pickle_model_class)


def prepare_class():
    create_df_class()
    df_smart = u_pickle.load(pickle_df_class)

    x = df_smart.drop(columns=['label'])
    y = df_smart['label']
    x_train, x_test, y_train, y_test = u_train_test.split(x, y,
                                                          is_classifier=False)
    u_pickle.dump((x_train, x_test, y_train, y_test), pickle_train_test_class)
    create_model_class(x_train, y_train)


def calc_class(x):
    df_data = pd.read_csv(csv_data)
    model = u_pickle.load(pickle_model_class)
    y_pred = model.predict(x)

    count = 0
    for i, (index, row) in enumerate(x.iterrows()):
        forward = int(df_data.at[index, 'forward'])
        backward = int(df_data.at[index, 'backward'])
        if y_pred[i] > 0.5:
            count += backward / forward
        else:
            count += 1
    print(count / len(x))


prepare_class()

x_train, x_test, y_train, y_test = u_pickle.load(pickle_train_test_class)

calc_class(x_train)
calc_class(x_test)

model = u_pickle.load(pickle_model_class)
y_pred = model.predict_proba(x_test)
print(u_rfc.evaluate(y_pred[:, 1], y_test))



"""
li_index = list()
li_forward = list()
li_backward = list()
li_delta = list()
li_pred = list()
for i, (index, row) in enumerate(x_test.iterrows()):
    forward = int(df_data.at[index, 'forward'])
    backward = int(df_data.at[index, 'backward'])
    li_index.append(index)
    li_forward.append(forward)
    li_backward.append(backward)
    li_delta.append(forward - backward)
    li_pred.append(y_pred[i])
df_pred = pd.DataFrame({'index': li_index, 'forward': li_forward,
                        'backward': li_backward, 'delta': li_delta,
                        'pred': li_pred})
df_pred.to_csv(csv_pred)
"""