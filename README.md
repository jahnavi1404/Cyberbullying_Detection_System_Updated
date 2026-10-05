# Cyberbullying Detection System

Flask web app that classifies a message as Cyberbullying or Normal.

## Files
- cyberbullying.csv  training data (text, label, source). 1 = cyberbullying, 0 = normal
- textutils.py       text cleaning + high-risk patterns (stalking, threats, blackmail, self-harm encouragement)
- model.py           trains the model, prints accuracy, saves model.pkl and vectorizer.pkl
- detector.py        classify() = rules + machine learning model
- app.py             Flask web app (browser UI + /predict API)
- client.py          tests the API
- test_cases.py      70 sample messages to check the whole system
- requirements.txt   packages to install

## Run
1. pip install -r requirements.txt
2. python model.py        (train; do this again every time you edit cyberbullying.csv)
3. python test_cases.py   (optional check, should print 70/70 correct)
4. python app.py          then open http://127.0.0.1:5000
5. python client.py       (optional, in a second terminal while the app runs)

## Improving it
If a message is classified wrongly, add it to cyberbullying.csv as:
    "your message",1,custom      (bullying)
    "your message",0,custom      (normal)
then run python model.py again and restart app.py.
Add 5-10 similar wordings, not just one, so the model learns the pattern.

## Data
Rows with source=custom are hand-written. Rows with source=public come from the
Davidson et al. hate speech and offensive language dataset (MIT licence),
cleaned of usernames and links.
