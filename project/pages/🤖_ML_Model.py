import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import streamlit as st

#load data
combined_data = pd.read_csv('data/combined_data.csv')

combined_data['Price_Increase'] = (combined_data['Close'].shift(-1) > combined_data['Close']).astype(int)

#drop last row
combined_data = combined_data.iloc[:-1]

#filtering
key_columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'Price_Increase']
filtered_data = combined_data[key_columns]
filtered_data = filtered_data.apply(pd.to_numeric, errors='coerce')
filtered_data = filtered_data.fillna(filtered_data.mean())

if filtered_data.shape[0] < 2:
    st.error("Not enough data to train the model.")
else:

    X = filtered_data.drop(columns=['Price_Increase'])
    y = filtered_data['Price_Increase']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LogisticRegression(max_iter=1000)

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    classification_rep = classification_report(y_test, y_pred, zero_division=0)


    if y_pred.mean() > 0.5:
        price_increase_message = "The model predicts that prices will increase."
    else:
        price_increase_message = "The model predicts that prices will not increase."

    #streamlit time
    
    st.title("Stock Price Prediction")
    st.write(f"Accuracy: {accuracy}")

    #precision recall, yada yada yada
    st.text("Classification Report:")
    st.code(classification_rep)

    #df
    st.write("Combined Data:")
    st.write(combined_data.head())

    #feature importance
    st.write("Feature Importance:")
    feature_importance = pd.Series(model.coef_[0], index=X.columns)
    st.bar_chart(feature_importance)

    # to increase or not to increase
    st.write(price_increase_message)