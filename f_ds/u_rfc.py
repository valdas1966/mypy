import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from f_utils import u_int


def create_model(x_train, y_train, verbose=0):
    """
    =======================================================================
     Description: Return Random Forest Model learned by X and Y Train.
    =======================================================================
     Arguments:
    -----------------------------------------------------------------------
        1. x_train : DataFrame (Train Features).
        2. y_train : Series (Label).
        3. verbose : int (Level of Verbose).
    =======================================================================
     Return: Random Forest Model.
    =======================================================================
    """
    rf = RandomForestClassifier(n_estimators=1000, random_state=42,
                                n_jobs=-1, verbose=verbose)
    return rf.fit(x_train, y_train)


def predict_proba(model, x_test):
    """
    =======================================================================
     Description: Return Probability for Positive-Label for each row.
    =======================================================================
     Arguments:
    -----------------------------------------------------------------------
        1. model : Random Forest Classifier Model.
        2. x_test : DataFrame (Test Features).
    =======================================================================
     Return: Numpy Array (probability for positive label).
    =======================================================================
    """
    return model.predict_proba(x_test)[:, 1]


def evaluate(y_pred, y_test):
    """
    =======================================================================
     Description: Return DataFrame with Evaluation Results.
    -----------------------------------------------------------------------
        1. Proba (from what probability to check the y_pred against
                     the y_test [0.1, 0.2, ... , 0.9, 1.0]).
    -----------------------------------------------------------------------
        2. Count (amount of rows with probability equals or higher than
                    a given Proba).
    -----------------------------------------------------------------------
        3. Percent (percent of Count relatively to amount of all rows).
    -----------------------------------------------------------------------
        4. Precision (precision for this proba).
    -----------------------------------------------------------------------
        5. Recall (recall for this proba).
    =======================================================================
     Arguments:
    -----------------------------------------------------------------------
        1. y_pred : Numpy Array (with proba that the predicted label is 1).
        2. y_test : Series (with real labels).
    =======================================================================
     Return: DataFrame (with the evaluation results listed above).
    =======================================================================
    """
    y_test = list(y_test)
    results = {'Proba': list(), 'Count': list(), 'Percent': list(),
               'Precision': list(), 'Recall': list(), 'TP': list(),
               'FP': list(), 'TN': list(), 'FN': list()}
    count_all = len(y_test)
    count_true_all = len([x for x in y_test if x == 1])
    for proba in np.arange(0.1, 1.1, 0.1):
        count_proba = 0
        count_true = 0
        tp = 0
        tn = 0
        fp = 0
        fn = 0
        for i in range(len(y_pred)):
            if y_pred[i] >= proba:
                count_proba += 1
                if y_test[i]:
                    count_true += 1
                    tp += 1
                else:
                    fp += 1
            else:
                if y_test[i]:
                    fn += 1
                else:
                    tn += 1
        results['Proba'].append(proba)
        results['Count'].append(count_proba)
        percent_proba = u_int.to_percent(count_proba, count_all)
        precision = u_int.to_percent(count_true, count_proba)
        recall = u_int.to_percent(count_true, count_true_all)
        tp = u_int.to_percent(tp, count_proba)
        tn = u_int.to_percent(tn, count_all - count_proba)
        fp = u_int.to_percent(fp, count_proba)
        fn = u_int.to_percent(fn, count_all - count_proba)
        results['Percent'].append(percent_proba)
        results['Precision'].append(precision)
        results['Recall'].append(recall)
        results['TP'].append(tp)
        results['TN'].append(tn)
        results['FP'].append(fp)
        results['FN'].append(fn)

    df = pd.DataFrame(results)
    return df[['Proba', 'Count', 'Percent', 'Precision', 'Recall', 'TP',
               'FP', 'TN', 'FN']]
