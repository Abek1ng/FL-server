import os
import pickle
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

class GlobalModel:
    def __init__(self, model_path="global_model.pkl"):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.updates = []
        self.model_path = model_path

        # Load or initialize the model
        if os.path.exists(self.model_path):
            self.load_model()
        else:
            self.train_initial_model("data/server_data.csv")

    def train_initial_model(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Dataset not found at {file_path}")

        data = pd.read_csv(file_path)
        X = data.drop(columns="Outcome")
        y = data["Outcome"]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)

    def receive_update(self, serialized_data):
        try:
            update = pickle.loads(serialized_data)
            self.updates.append(update)
            if len(self.updates) >= 3:
                self.aggregate_updates()
        except Exception as e:
            raise ValueError(f"Invalid update data: {e}")

    def aggregate_updates(self):
        # Example: Averaging feature importances
        aggregated_importances = sum(self.updates) / len(self.updates)
        self.model.feature_importances_ = aggregated_importances
        self.updates = []

    def send_model(self):
        if not hasattr(self.model, "feature_importances_"):
            raise ValueError("Global model is not trained yet.")
        return pickle.dumps(self.model.feature_importances_)

    def load_model(self):
        with open(self.model_path, "rb") as f:
            self.model = pickle.load(f)

    def save_model(self):
        with open(self.model_path, "wb") as f:
            pickle.dump(self.model, f)
