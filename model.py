import pandas as pd
import pickle
from sklearn.pipeline import FeatureUnion
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

from textutils import normalize

# ---------- Load data ----------
data = pd.read_csv("cyberbullying.csv").dropna(subset=["text", "label"])
data["text"] = data["text"].astype(str).map(normalize)
data = data[data["text"].str.len() > 0].reset_index(drop=True)
if "source" not in data.columns:
    data["source"] = "custom"

# Hand-written examples are the most reliable ones, so they count 3x
data["weight"] = data["source"].map(lambda s: 3.0 if s == "custom" else 1.0)

X, y, w = data["text"], data["label"].astype(int), data["weight"]


def make_vectorizer():
    # words + 2-word phrases AND character patterns (handles spelling mistakes, slang, missing spaces)
    return FeatureUnion([
        ("word", TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True)),
        ("char", TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 5), sublinear_tf=True, min_df=2)),
    ])


def make_model():
    return LogisticRegression(C=8, class_weight="balanced", max_iter=3000)


# ---------- Check accuracy on data the model has not seen ----------
X_tr, X_te, y_tr, y_te, w_tr, w_te, s_tr, s_te = train_test_split(
    X, y, w, data["source"], test_size=0.2, random_state=42, stratify=y)
v_chk = make_vectorizer()
m_chk = make_model().fit(v_chk.fit_transform(X_tr), y_tr, sample_weight=w_tr)
pred = m_chk.predict(v_chk.transform(X_te))
print("Overall test accuracy:", round(accuracy_score(y_te, pred), 3))
print(classification_report(y_te, pred, target_names=["Normal", "Cyberbullying"]))

# ---------- Train final model on ALL data ----------
vectorizer = make_vectorizer()
model = make_model().fit(vectorizer.fit_transform(X), y, sample_weight=w)

pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))
print("Model trained and saved!")
