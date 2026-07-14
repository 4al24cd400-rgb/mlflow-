import mlflow
import mlflow.sklearn
import pandas as pd
import joblib
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import ConfusionMatrixDisplay, accuracy_score
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt

#load dataset
df = pd.read_csv("WA_Fn-UseC_-Telco-Customer-Churn.csv")

x=df[['customerID', 'gender', 'SeniorCitizen', 
      'Partner', 'Dependents', 'tenure', 
      'PhoneService', 'MultipleLines', 
      'InternetService', 'OnlineSecurity', 
      'OnlineBackup', 'DeviceProtection', 
      'TechSupport', 'StreamingTV', 'StreamingMovies', 
      'Contract', 'PaperlessBilling', 'PaymentMethod', 
      'MonthlyCharges', 'TotalCharges']]

x = x.drop(columns=['customerID'])
x = pd.get_dummies(x, drop_first=False)
x['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
x = x.dropna()
y = df.loc[x.index, 'Churn'].map({'Yes': 1, 'No': 0})

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

#create experiment
mlflow.set_experiment("churn_prediction")

#train multiple models
depths = [10, 15, 20, 25, None]
for depth in depths:
    with mlflow.start_run():
        #create model
        model = RandomForestClassifier(n_estimators=1000,max_depth=20,min_samples_split=2,min_samples_leaf=1,max_features='sqrt',bootstrap=True,random_state=42,n_jobs=-1)
        
        #train model
        model.fit(x_train, y_train)
        
        #predict
        preditctions = model.predict(x_test)
        
        #evaluate
        accuracy = accuracy_score(y_test, preditctions)

        #log parameters and metrics
        mlflow.log_param("max_depth", depth)
        mlflow.log_metric("accuracy", accuracy)
        
        disp=ConfusionMatrixDisplay.from_predictions(y_test, preditctions)
        plt.savefig(f"confusion_matrix.png")
        plt.close()

        #log artifacts
        mlflow.log_artifact("confusion_matrix.png")

        #log model
        mlflow.sklearn.log_model(model, "RandomForestClassifier")

        print(f"Depth: {depth} Accuracy= {accuracy:.4f}")
    
print("Completed Successfully")  
    