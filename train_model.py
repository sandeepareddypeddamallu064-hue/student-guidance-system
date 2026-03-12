import pandas as pd
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

data = {
    "gpa":[6.5,7,8,8.5,9,7.5,6.8,8.2,9.2,7.1,6.2,8.7,7.9,8.4,6.9,7.3],
    "coding":[50,120,200,300,400,150,80,250,350,100,60,320,270,310,140,180],
    "ml_skill":[0,0,1,1,1,0,0,1,1,0,0,1,1,1,0,0],
    "internship":[0,0,1,1,1,0,0,1,1,0,0,1,1,1,0,0],
    "placed":[0,0,1,1,1,0,0,1,1,0,0,1,1,1,0,0]
}

df = pd.DataFrame(data)

X = df[["gpa","coding","ml_skill","internship"]]
y = df["placed"]

model = Pipeline([
    ("scaler", StandardScaler()),
    ("classifier", LogisticRegression())
])

model.fit(X,y)

pickle.dump(model, open("model.pkl","wb"))

print("Model trained successfully")