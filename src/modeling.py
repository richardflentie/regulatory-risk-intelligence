"""
modeling.py
"""

"""
modeling.py

Trains a baseline logistic regression model
on monthly enforcement risk features.
"""

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score



def train_baseline_model(df: pd.DataFrame):
    df = df.copy()

    # Convert month to datetime
    df["month"] = pd.to_datetime(df["month"])

    # Time-based split (no leakage)
    cutoff = df["month"].quantile(0.8)
    train = df[df["month"] <= cutoff]
    test = df[df["month"] > cutoff]

    features = ["events_last_6m", "peer_events_last_6m"]
    target = "y_next_6m"

    X_train = train[features]
    y_train = train[target]

    X_test = test[features]
    y_test = test[target]

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    probs = model.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, probs)

    return model, auc, test, probs, features