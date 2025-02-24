import os
import sys
import numpy as np
import pandas as pd
import pickle
import dill
from src.exception import CustomerException
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)
        
        os.makedirs(dir_path, exist_ok=True)
        
        with open(file_path, 'wb') as file:
            pickle.dump(obj, file)
    
    except Exception as e:
        raise CustomerException(e, sys)


def evaluate_models(X_train, y_train, X_test, y_test, models, params):
    try:
        report={}
        
        for i in range(len(list(models))):
            model = list(models.values())[i]
            param = params[list(models.keys())[i]]
            
            gs = GridSearchCV(model,param,cv=3)
            gs.fit(X_train,y_train)
            
            model.set_params(**gs.best_params_)
            model.fit(X_train, y_train)
            
            y_train_pred = model.predict(X_train)
            
            y_test_pred = model.predict(X_test)
            
            train_model_score = r2_score(y_train, y_train_pred)
            
            test_model_score = r2_score(y_test, y_test_pred)
            
            report[list(models.keys())[i]] = test_model_score
        
        return report
    except Exception as e:
        raise CustomerException(e, sys)

def load_object(file_path):
    try:
        with open(file_path, 'rb') as file:
            return dill.load(file)
    
    except Exception as e:
        raise CustomerException(e, sys)