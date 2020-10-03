import pandas as pd
import numpy as np
from f_ds import u_fe
from f_ds import u_fs
from f_ds import u_train_test
from f_ds import u_rfc
from f_ds import u_rfr
from f_utils import u_pickle
from sklearn.ensemble import RandomForestRegressor


csv_data = 'G:\\MyPy\\f_astar\\experiments\\results_kastar_lookup_5.csv'
pickle_df_regr = 'G:\\MyPy\\f_astar\\experiments\\df_regr.pickle'
pickle_model_regr = 'G:\\MyPy\\f_astar\\experiments\\model_regr.pickle'
pickle_train_test_regr = 'G:\\MyPy\\f_astar\\experiments\\train_text_regr' \
                        '.pickle'
csv_pred = 'G:\\MyPy\\f_astar\\experiments\\pred_5.csv'
pickle_best_model = 'G:\\MyPy\\f_astar\\experiments\\best_model.pickle'


def create_df_regr():
    df = pd.read_csv(csv_data)
    df = df[df['forward'] > df['d']]
    df = df[df['forward'] > 10]
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
    df_synthetic = u_fe.synthetic(df, columns_to_exclude={'label'})
    df = pd.concat([df, df_synthetic], axis=1)
    df = u_fs.drop_correlated_features(df, 0.99)
    u_pickle.dump(df, pickle_df_regr)


def create_model_regr(x_train, y_train):
    model = u_rfr.create_model(x_train, y_train, verbose=2)
    u_pickle.dump(model, pickle_model_regr)


def prepare_regr():
    create_df_regr()
    df_smart = u_pickle.load(pickle_df_regr)

    x = df_smart.drop(columns=['label'])
    y = df_smart['label']
    x_train, x_test, y_train, y_test = u_train_test.split(x, y,
                                                          is_classifier=False)
    u_pickle.dump((x_train, x_test, y_train, y_test), pickle_train_test_regr)
    create_model_regr(x_train, y_train)


def calc_regr(x):
    df_data = pd.read_csv(csv_data)
    model = u_pickle.load(pickle_model_regr)
    y_pred = model.predict(x)

    count = 0
    for i, (index, row) in enumerate(x.iterrows()):
        forward = int(df_data.at[index, 'forward'])
        backward = int(df_data.at[index, 'backward'])
        if y_pred[i] < 0.95:
            count += backward / forward
        else:
            count += 1
    print(count / len(x))


def calc_best(x, model):
    df_data = pd.read_csv(csv_data)
    y_pred = model.predict(x)

    count = 0
    for i, (index, row) in enumerate(x.iterrows()):
        forward = int(df_data.at[index, 'forward'])
        backward = int(df_data.at[index, 'backward'])
        if y_pred[i] < 1:
            count += backward / forward
        else:
            count += 1
    print(count / len(x))

#prepare_regr()

x_train, x_test, y_train, y_test = u_pickle.load(pickle_train_test_regr)


#calc_regr(x_train)
#calc_regr(x_test)

"""
from sklearn.model_selection import RandomizedSearchCV
# Number of trees in random forest
n_estimators = [int(x) for x in np.linspace(start = 200, stop = 2000, num = 10)]
# Number of features to consider at every split
max_features = ['auto', 'sqrt']
# Maximum number of levels in tree
max_depth = [int(x) for x in np.linspace(10, 110, num = 11)]
max_depth.append(None)
# Minimum number of samples required to split a node
min_samples_split = [2, 5, 10]
# Minimum number of samples required at each leaf node
min_samples_leaf = [1, 2, 4]
# Method of selecting samples for training each tree
bootstrap = [True, False]
# Create the random grid
random_grid = {'n_estimators': n_estimators,
               'max_features': max_features,
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf,
               'bootstrap': bootstrap}

# Use the random grid to search for best hyperparameters
# First create the base model to tune
rf = RandomForestRegressor()
# Random search of parameters, using 3 fold cross validation,
# search across 100 different combinations, and use all available cores
rf_random = RandomizedSearchCV(estimator = rf, param_distributions = random_grid, n_iter = 100, cv = 3, verbose=2, random_state=42, n_jobs = -1)
# Fit the random search model
rf_random.fit(x_train, y_train)

u_pickle.dump(rf_random, pickle_best_model)

print(rf_random.best_params_)

best_random = rf_random.best_estimator_
"""

best_random = u_pickle.load(pickle_best_model)
calc_best(x_train, best_random.best_estimator_)
calc_best(x_test, best_random.best_estimator_)

