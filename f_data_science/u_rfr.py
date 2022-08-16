from sklearn.ensemble import RandomForestRegressor


def create_model(x_train, y_train, verbose=0):
    """
    =======================================================================
     Description: Return Random Forest Model learned by X and Y Train.
    =======================================================================
     Arguments:
    -----------------------------------------------------------------------
        1. x_train : DataFrame (Train Features).
        2. y_train : Series (Label).
        3. verbose : int (Level of Verbosity).
    =======================================================================
     Return: Random Forest Model.
    =======================================================================
    """
    rf = RandomForestRegressor(n_estimators=1000, random_state=42, n_jobs=-1,
                               verbose=verbose)
    return rf.fit(x_train, y_train)


def predict(model, x_test):
    """
    =======================================================================
     Description: Return Prediction for each row.
    =======================================================================
     Arguments:
    -----------------------------------------------------------------------
        1. model : Random Forest Regressor Model.
        2. x_test : DataFrame (Test Features).
    =======================================================================
     Return: Numpy Array (probability for positive label).
    =======================================================================
    """
    return model.predict(x_test)
