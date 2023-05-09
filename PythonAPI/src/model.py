import pickle
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


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
        else:
            print("Model not found")
            return None

    def train_DT_CLF(X, y):

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
        with open('../models/DT.pkl', 'wb') as model_file:
            pickle.dump(clf, model_file)

    def predict_DT_CLF(self, X):

        if self.model is None:
            print("Model not Defined")
            return None

        # Predict on testing data
        y_pred = self.model.predict(X)

        return y_pred
