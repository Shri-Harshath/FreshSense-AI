import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

def train():
    df = pd.read_csv("spoilage_data.csv")
    
    # Features (X) and Target (y)
    X = df[["temperature_c", "humidity_pct", "gas_ppm", "hours_elapsed"]]
    y = df["freshness_score"]
    
    # 80/20 train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42
    )
    
    # Train Random Forest Regressor
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=12,
        random_state=42
    )
    model.fit(X_train, y_train)
    
    # Evaluate
    predictions = model.predict(X_test)
    r2 = r2_score(y_test, predictions)
    mae = mean_absolute_error(y_test, predictions)
    
    print("\n--- Training Evaluation ---")
    print(f"R-squared Score: {r2:.4f} (Goal > 0.90)")
    print(f"Mean Absolute Error: {mae:.2f} points on 0-100 scale")
    
    # Feature importances
    for feature, importance in zip(X.columns, model.feature_importances_):
        print(f"Feature '{feature}': {importance * 100:.1f}% weight")
    
    # Save the trained model artifact
    joblib.dump(model, "freshness_model.pkl")
    print("\nSaved model artifact to 'freshness_model.pkl'")

if __name__ == "__main__":
    train()
