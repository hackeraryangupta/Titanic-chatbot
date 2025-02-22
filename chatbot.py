### FastAPI Backend (main.py) ###
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd

# Load Titanic dataset
df = pd.read_csv('titanic.csv')

# Initialize FastAPI app
app = FastAPI()

# Define request model
class QueryRequest(BaseModel):
    question: str

# Basic endpoint for processing questions
@app.post("/query")
def query_titanic(request: QueryRequest):
    question = request.question.lower()
    
    if "percentage of passengers were male" in question:
        male_percentage = (df['Sex'] == 'male').mean() * 100
        return {"answer": f"{male_percentage:.2f}% of passengers were male."}
    elif "histogram of passenger ages" in question:
        return {"visualization": "age_histogram"}  # To be handled by frontend
    elif "average ticket fare" in question:
        avg_fare = df['Fare'].mean()
        return {"answer": f"The average ticket fare was ${avg_fare:.2f}."}
    elif "passengers embarked from each port" in question:
        embarked_counts = df['Embarked'].value_counts().to_dict()
        return {"answer": embarked_counts}
    else:
        raise HTTPException(status_code=400, detail="I couldn't understand your question.")


### Streamlit Frontend (app.py) ###
import streamlit as st
import requests
import matplotlib.pyplot as plt

# Streamlit App
st.title("Titanic Dataset Chatbot")

user_question = st.text_input("Ask a question about the Titanic dataset:")
if st.button("Submit"):
    response = requests.post("http://localhost:8000/query", json={"question": user_question})
    if response.status_code == 200:
        result = response.json()
        if 'answer' in result:
            st.write(result['answer'])
        elif result.get('visualization') == 'age_histogram':
            # Load data and show histogram
            df = pd.read_csv('titanic.csv')
            plt.hist(df['Age'].dropna(), bins=30, color='skyblue')
            plt.xlabel('Age')
            plt.ylabel('Count')
            plt.title('Histogram of Passenger Ages')
            st.pyplot(plt)
    else:
        st.error("Error: Could not process your request.")

### LangChain Integration (placeholder for future) ###
# Will handle more complex natural language understanding later.
