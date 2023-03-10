import json
import os

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV
from xgboost import XGBClassifier


class XGBoostModel:
    """
    The XGBoostModel class is used to do hyperparameter tuning, model training, prediction and evaluation
    """

    def __init__(self, train_df, val_df, test_df):
        """
        Initialize the class with training, validation and test dataframes

        :param train_df: pandas.DataFrame, dataframe containing the training data
        :param val_df: pandas.DataFrame, dataframe containing the validation data
        :param test_df: pandas.DataFrame, dataframe containing the test data
        """
        self.train_df = train_df
        self.val_df = val_df
        self.test_df = test_df

    def prepare_data(self):
        """
        Prepare datasets for training, validation and test
        """
        # extract features for datasets
        X_train = self.train_df.iloc[:, :-1]
        X_val = self.val_df.iloc[:, :-1]
        X_test = self.test_df.iloc[:, :-1]

        # extract labels for datasets
        y_train = self.train_df.iloc[:, -1]
        y_val = self.val_df.iloc[:, -1]
        y_test = self.test_df.iloc[:, -1]

        return X_train, y_train, X_val, y_val, X_test, y_test

    def set_params(self, model_param: dict):
        """
        Set model parameters

        :param model_param: dict, dictionary containing the parameters for the model
        """
        # create an instance of the XGBClassifier
        self.model = XGBClassifier()

        # set the model parameters using the provided dictionary
        self.model.set_params(
            learning_rate=model_param["learning_rate"],
            max_depth=model_param["max_depth"],
            n_estimators=model_param["n_estimators"],
            gamma=model_param["gamma"],
            reg_lambda=model_param["lambda"],
            scale_pos_weight=model_param["scale_pos_weight"],
            min_child_weight=model_param["min_child_weight"],
            objective=model_param["objective"],
            tree_method=model_param["tree_method"],
        )

    def fit(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: np.ndarray,
        y_val: np.ndarray,
        file_path: str,
        file_name: str,
    ):
        """
        Fit the model on training data

        :param X_train: numpy.ndarray, features for training
        :param y_train: numpy.ndarray, labels for training
        :param X_val: numpy.ndarray, features for validation
        :param y_val: numpy.ndarray, labels for validation
        :param file_path: str, path where the eval_metrics should be saved
        :param file_name: str, name of the file to be saved
        """
        # define accuracy metric function
        def accuracy(preds, dtrain):
            """
            Calculates the accuracy of predictions made by a model

            :param preds: np.array, an array of predictions made by the model
            :param dtrain: object, the training data that is used to evaluate the accuracy of the model
            :return: tuple, a tuple containing the string 'accuracy' and the calculated accuracy score
            """
            # retrieve true labels from the training data
            labels = dtrain.get_label()

            # calculate accuracy by comparing true labels to the rounded predictions
            accuracy = accuracy_score(labels, np.round(preds))
            return "accuracy", accuracy

        # define save evaluation metrics function
        def save_eval_metrics(file_path: str, file_name: str, result):
            """
            Save the eval_metrics of a model in yaml format

            :param file_path: str, path where the eval_metrics should be saved
            :param result: object, the result returned by the fit method of a model
            """
            # open the file in write mode
            with open(os.path.join(file_path, file_name), "w") as f:
                # dump the eval_result_ attribute of the result object into the file
                json.dump(result.evals_result_, f)

        # fit the model on the training data and evaluate on validation data
        result = self.model.fit(
            X_train,
            y_train,
            eval_set=[(X_train, y_train), (X_val, y_val)],
            eval_metric=accuracy,
            verbose=0,
        )

        # save evaluation metrics to file
        save_eval_metrics(file_path, file_name, result)

    def grid_search(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: np.ndarray,
        y_val: np.ndarray,
        file_path: str,
        file_name: str,
        grid_params: dict,
    ):
        """
        Runs a grid search to tune the hyperparameters of the model

        :param X_train: numpy.ndarray, features for training
        :param y_train: numpy.ndarray, labels for training
        :param X_val: numpy.ndarray, features for validation
        :param y_val: numpy.ndarray, labels for validation
        :param file_path: str, path to save the best results
        :param file_name: str, name of the file to save the best results
        :param grid_params: str, dictionary containing the grid search parameters
        """
        # define save best parameters function
        def save_best_parameters(file_path: str, file_name: str, grid):
            """
            Save the best parameters and best score of a model in yaml format

            :param file_path: str, path where the best parameters and best score should be saved
            :param grid: object, the grid returned by the fit method of a model
            """
            # open the file in write mode
            with open(os.path.join(file_path, file_name), "w") as f:
                # dump the eval_result_ attribute of the result object into the file
                json.dump(grid.best_params_, f)

        # create an instance of the XGBClassifier
        self.model = XGBClassifier()

        # create an instance of the GridSearchCV class
        grid = GridSearchCV(
            self.model, grid_params, cv=3, scoring="accuracy", n_jobs=-1, verbose=1
        )

        # fit the GridSearchCV object on the training data
        grid = grid.fit(
            X_train, y_train, eval_set=[(X_val, y_val)], eval_metric="logloss"
        )

        # save evaluation metrics to file
        save_best_parameters(file_path, file_name, grid)

    def feature_importance(self):
        """
        Calculates the feature importance of the model
        """
        # retrieve feature importances
        feature_importance = self.model.feature_importances_

        # return feature importance
        return feature_importance

    @staticmethod
    def create_log_df(log_data: dict) -> pd.DataFrame:
        """
        Create a DataFrame from log data

        :param log_data: dict, log data
        :return: pd.DataFrame, DataFrame containing log data
        """
        # extract data from log data
        train_loss = log_data["validation_0"]["logloss"]
        val_loss = log_data["validation_1"]["logloss"]
        train_acc = log_data["validation_0"]["accuracy"]
        val_acc = log_data["validation_1"]["accuracy"]
        iteration = list(range(0, len(train_loss)))

        # define column names
        columns = ["iteration", "train_loss", "train_acc", "val_loss", "val_acc"]

        # create DataFrame from extracted data and column names
        return pd.DataFrame(
            list(zip(iteration, train_loss, train_acc, val_loss, val_acc)),
            columns=columns,
        )

    def predict(self, X_test: np.ndarray) -> np.ndarray:
        """
        Make predictions for test data

        :param X_test: numpy.ndarray, features for test
        :return: numpy.ndarray, array containing the predicted labels for test data
        """
        # make predictions on the test data using the trained model
        return self.model.predict(X_test)

    def evaluate_predictions(self, y_test: np.ndarray, y_pred: np.ndarray) -> float:
        """
        Evaluate predictions and return accuracy

        :param y_test: numpy.ndarray, true labels for test data
        :param y_pred: numpy.ndarray, predicted labels for test data
        :return: float, accuracy score
        """
        # round the predictions to the nearest integer
        predictions = [round(value) for value in y_pred]

        # return accuracy
        return accuracy_score(y_test, predictions)
