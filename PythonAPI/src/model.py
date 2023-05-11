import pickle
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np
import pandas as pd
import src.preprocessing as pp
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import load_model


class ModelHandler:

    def __init__(self, model_name=None):
        if model_name is None:
            self.model = None
        else:
            self.model = self.readAndSelectModel(model_name)

    def readAndSelectModel(self, model_name):
        if model_name == "DT":
            self.model = pickle.load(open("./src/DT.pkl", "rb"))
            return self.model
        elif model_name == "N":
            self.model = load_model('./src/Neural.h5')
            return self.model
        else:
            print("Model not found")
            return None

    def train_Neural(self, X, y, path):

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42)

        # Standardize the input features using StandardScaler
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # Define the neural network model architecture
        model = Sequential()
        model.add(Dense(64, activation='relu',
                  input_shape=(X_train_scaled.shape[1],)))
        model.add(Dense(64, activation='relu'))
        # Output layer with softmax activation for multi-class classification
        model.add(Dense(len(pp.target_columns), activation='relu'))

        # Compile the model
        model.compile(loss='binary_crossentropy',
                      optimizer='adam', metrics=['accuracy'])

        # Train the model
        model.fit(X_train_scaled, y_train, epochs=10, batch_size=32, verbose=1)

        # Evaluate the model on the testing set
        loss, accuracy = model.evaluate(X_test_scaled, y_test, verbose=0)
        print(f'Test Loss: {loss:.4f}')
        print(f'Test Accuracy: {accuracy:.4f}')

        # Save the model
        model.save(path)

        self.model = model

    def train_DT_CLF(self, X, y, path):

        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42)

        # Create decision tree classifier
        clf = DecisionTreeClassifier()

        # Fit decision tree to training data
        clf.fit(X_train, y_train)

        # Predict on testing data
        y_pred = clf.predict(X_test)

        # Evaluate accuracy
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {accuracy}")

        # Save model in file
        with open(path, 'wb') as model_file:
            pickle.dump(clf, model_file)

        self.model = clf

    def train_model_from_csv(self, path):

        # Read data from csv
        data = pd.read_csv(path)

        print(data.head())

        X, y = pp.preProcessAndGetXy(data)

        # Train model
        if self.model_name is None:
            print("Model not Defined")
            return None
        if self.model_name == "N":
            self.train_Neural(X, y, "./src/Neural.h5")
        elif self.model_name == "DT":
            self.train_DT_CLF(X, y, "./src/DT.pkl")

    def predict_DT_CLF(self, X):

        if self.model is None:
            print("Model not Defined")
            return None

        scaler = StandardScaler()

        # Predict on testing data
        new_data_scaled = scaler.transform(X)

        # Make predictions on the new data
        predictions = self.model.predict(new_data_scaled)

        return np.array(predictions)
        # # convert values to binary strings
        # binary_strings = [bin(value)[2:].zfill(10) for value in y_pred]

        # # transform binary strings to arrays of 10 elements
        # y_pred = np.array([list(value)
        #                   for value in binary_strings]).astype(int)

    def predict_DT_CLF(self, X):

        if self.model is None:
            print("Model not Defined")
            return None

        # print(X)

        # Predict on testing data with no printing
        y_pred = self.model.predict(X)

        # # convert values to binary strings
        # binary_strings = [bin(value)[2:].zfill(10) for value in y_pred]

        # # transform binary strings to arrays of 10 elements
        # y_pred = np.array([list(value)
        #                   for value in binary_strings]).astype(int)

        return y_pred
