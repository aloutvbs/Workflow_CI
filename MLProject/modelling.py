import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score


def load_data():
    """Load dataset hasil preprocessing."""
    X_train = pd.read_csv("dataset_preprocessing/X_train.csv")
    X_test = pd.read_csv("dataset_preprocessing/X_test.csv")
    y_train = pd.read_csv("dataset_preprocessing/y_train.csv")
    y_test = pd.read_csv("dataset_preprocessing/y_test.csv")
    return X_train, X_test, y_train, y_test


def train_model():
    # Aktifkan autolog agar parameter, metrics, dan model tercatat otomatis
    mlflow.sklearn.autolog()

    X_train, X_test, y_train, y_test = load_data()

    # Model yang sama dengan folder Membangun_model
    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42,
    )

    # Jalankan eksperimen MLflow
    with mlflow.start_run():
        # TRAIN
        model.fit(X_train, y_train.values.ravel())

        # PREDICT
        y_pred = model.predict(X_test)

        # METRICS
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        print(f"MSE: {mse}")
        print(f"R2 Score: {r2}")

        # Pastikan model tersimpan di artifacts/model (penting untuk CI & Docker)
        mlflow.sklearn.log_model(model, artifact_path="model")


if __name__ == "__main__":
    train_model()
