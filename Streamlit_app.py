
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

# Title
st.title("PCOS Prediction App")

# Sidebar navigation
menu = st.sidebar.radio("Navigation", ["Home", "PCOS Prediction", "Quiz", "Health Recipes", "Personalized Meal Plan", "Games", "Mood Tracker"])

if menu == "Home":
    st.write("## Hey there! What’s up? Click on any of the features in the dashboard to get started.")
    st.write("Use this tool to predict PCOS risk, take a quiz to assess symptoms, and explore healthy recipes!")

elif menu == "PCOS Prediction":
    # Upload dataset
    uploaded_file = st.file_uploader("Upload your PCOS dataset (CSV)", type=["csv"])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        df.columns = df.columns.str.strip()
        
        pcos_column = None
        for col in df.columns:
            if "PCOS" in col:
                pcos_column = col
                break
        
        if pcos_column is None:
            st.error("Error: No 'PCOS' column found in the dataset. Please check your file.")
        else:
            label_encoders = {}
            for col in df.select_dtypes(include=['object']).columns:
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col])
                label_encoders[col] = le
            
            df.fillna(df.mean(), inplace=True)
            
            X = df.drop(columns=[pcos_column])
            y = df[pcos_column]
            
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            
            y_pred = model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            st.write(f"### Model Accuracy: {accuracy:.2f}")
            
            feature_importances = model.feature_importances_
            features = X.columns
            plt.figure(figsize=(10, 5))
            plt.barh(features, feature_importances, color='skyblue')
            plt.xlabel("Importance")
            plt.ylabel("Features")
            plt.title("Feature Importance in PCOS Prediction")
            st.pyplot(plt)
            
            st.write("### Enter Details for Prediction")
            user_input = {}
            for col in X.columns:
                user_input[col] = st.number_input(f"{col}", value=float(df[col].mean()))
            
            if st.button("Predict"):
                input_df = pd.DataFrame([user_input])
                prediction = model.predict(input_df)[0]
                result = "PCOS Detected" if prediction == 1 else "No PCOS Detected"
                st.write(f"### Prediction: {result}")

elif menu == "Quiz":
    st.write("### PCOS Awareness Quiz")
    questions = {
        "What is a common symptom of PCOS?": ["Weight gain", "Hair loss", "Irregular periods", "All of the above"],
        "Which hormone is often elevated in PCOS?": ["Estrogen", "Progesterone", "Insulin", "Testosterone"],
        "Which lifestyle change can help manage PCOS?": ["Exercise", "Balanced diet", "Stress reduction", "All of the above"]
    }
    
    for question, options in questions.items():
        answer = st.radio(question, options)
        if answer == options[-1]:
            st.write("✅ Correct!")
        else:
            st.write("❌ Incorrect, try again!")

elif menu == "Health Recipes":
    st.write("### Healthy Recipes for PCOS")
    recipes = {
        "Green Smoothie": "- 1 cup spinach\n- 1 banana\n- 1/2 cup Greek yogurt\n- 1 cup almond milk\n- Blend and enjoy!",
        "Oatmeal with Chia Seeds": "- 1/2 cup rolled oats\n- 1 tbsp chia seeds\n- 1 cup almond milk\n- 1 tsp honey\n- Mix and let it sit for 10 minutes before eating.",
        "Avocado Toast with Egg": "- 1 slice whole-grain bread\n- 1/2 avocado\n- 1 boiled egg\n- Salt and pepper to taste\n- Mash avocado on toast, add sliced egg, and season."
    }
    selected_recipe = st.selectbox("Click to know more about a recipe", list(recipes.keys()))
    st.write(f"### {selected_recipe}")
    st.write(recipes[selected_recipe])

elif menu == "Mood Tracker":
    st.write("### Mood Tracker")
    
    if "mood_log" not in st.session_state:
        st.session_state.mood_log = []
    
    mood = st.radio("How are you feeling today?", ["Happy", "Stressed", "Tired", "Motivated"])
    note = st.text_area("Write a short journal entry about your mood (optional):")
    
    if st.button("Log Mood"):
        st.session_state.mood_log.append((mood, note))
        st.success("Mood logged successfully!")
    
    if st.session_state.mood_log:
        st.write("### Your Mood Log")
        df_mood = pd.DataFrame(st.session_state.mood_log, columns=["Mood", "Journal"])
        st.dataframe(df_mood)
        
        st.write("### Mood Trend")
        mood_counts = df_mood["Mood"].value_counts()
        plt.figure(figsize=(5, 3))
        plt.bar(mood_counts.index, mood_counts.values, color='skyblue')
        plt.xlabel("Mood")
        plt.ylabel("Count")
        plt.title("Mood Trends")
        st.pyplot(plt)
