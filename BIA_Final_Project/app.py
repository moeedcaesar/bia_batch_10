import streamlit as st
import pickle
import numpy as np
import pandas as pd
import altair as alt

# ------------------------- Load Model & Mapping -------------------------
with open("crop_recommendation.pkl", "rb") as model_file: # opens the "crop_recommendation.pkl" as model_file
    data = pickle.load(model_file)                        # Loads the pickeled data into the file
    model = data['model']                                 # puts the pickeled model in 'model' variable
    category_mapping = data['mapping']                    # puts the pickeled mapping into 'category_mapping'

# Titles the values of crops in the dictionary
category_mapping = {k: v.title() for k, v in category_mapping.items()}

# ------------------------- Page Styling -------------------------
st.title("🌾 Crop Recommendation System")
st.write("Enter the following measurements to get the recommendation")

# ------------------------- Input Tabs -------------------------
tab1, tab2, tab3, tab4 = st.tabs(["🌱 Soil", "🌊 Water", "🌡️ Climate", "💧 Nutrients"]) # made 4 distinct tabs

with tab1:
    SOIL_PH = st.slider("Average Soil pH", 1.0, 15.0, step=0.1) # 1st argument is min, 2nd is max and 3rd is step
    SOIL_PH_HIGH = st.slider("Max Soil pH", 1.0, 15.0, step=0.1)

    CROPDURATION = st.slider("Crop Duration (days)", 1, 365, step=1)
    CROPDURATION_MAX = st.slider("Max Crop Duration (days)", 1, 365, step=1)

with tab2:
    WATERREQUIRED = st.slider("Average Water Available (in millimeters, mm)", 300, 3000, step=5)
    WATERREQUIRED_MAX = st.slider("Max Water (in millimeters, mm)", 300, 3000, step=5)

with tab3:
    TEMP = st.slider("Average Temperature (°C)", 15.0, 55.0, step=0.1)
    MAX_TEMP = st.slider("Max Temperature (°C)", 15.0, 55.0, step=0.1)
    RELATIVE_HUMIDITY = st.slider("Relative Humidity (%)", 0.0, 100.0, step=1.0)
    RELATIVE_HUMIDITY_MAX = st.slider("Max Humidity (%)", 0.0, 100.0, step=1.0)

with tab4:
    N = st.slider("Nitrogen (kg/ha)", 1, 250, step=1)
    N_MAX = st.slider("Max Nitrogen (kg/ha)", 1, 250, step=1)
    P = st.slider("Phosphorus (kg/ha)", 1, 250, step=1)
    P_MAX = st.slider("Max Phosphorus (kg/ha)", 1, 250, step=1)
    K = st.slider("Potassium (kg/ha)", 1, 250, step=1)
    K_MAX = st.slider("Max Potassium (kg/ha)", 1, 250, step=1)

# ------------------------- Prediction -------------------------
if st.button("Predict"):
    features  = np.array([[SOIL_PH, # these are the features that we will pass to the 'model.predict' to get prediction
                           SOIL_PH_HIGH,
                           CROPDURATION,
                           CROPDURATION_MAX,
                           TEMP,
                           MAX_TEMP,
                           WATERREQUIRED,
                           WATERREQUIRED_MAX,
                           RELATIVE_HUMIDITY,
                           RELATIVE_HUMIDITY_MAX,
                           N,
                           N_MAX,
                           P,
                           P_MAX,
                           K,
                           K_MAX]])

    # Using try and except to catch error if it occurs
    try:
        prediction = model.predict(features)
        crop_name = category_mapping[prediction[0]] # Gives the name of crop with dictionary indexing
    except Exception as e:
        st.error(f"Prediction error: {e}")
        st.stop()                                   # stopping the program and display error

    # gives you expandable tab in which you can see the summary of your input values
    with st.expander("📋 Your Input Summary"):
        # 'features' here indicate all values that we inputted and the 'columns' argument use to name the columns
        st.write(pd.DataFrame(features, columns=[
            "Soil pH", "Max Soil pH", "Crop Duration", "Max Crop Duration",
            "Temp", "Max Temp", "Water", "Max Water",
            "Humidity", "Max Humidity", "N", "N Max", "P", "P Max", "K", "K Max"
        ]))

    # for styling, 'padding' gives spacing, 'border-radius' makes border round of box in which recommendation display
    st.markdown(
        f"""
            <div style="padding:15px; border-radius:10px; background-color:#006400 ; text-align:center;">
                <h2>🌾 Recommended Crop: <b>{crop_name}</b></h2>
            </div>
            """,
        unsafe_allow_html=True
    )

    # Gives the top 3 recommended crops along with their probabilities
    probs = model.predict_proba(features)[0] # takes the probabilities and store them in 'probs'
    # arrange probs in ascending order, -3 gives last 3 and -1 reverses them and store them in 'top3_idx'
    top3_idx = np.argsort(probs)[-3:][::-1]
    st.subheader("Top 3 Recommended Crops:")
    for idx in top3_idx:
        # label is name of crop retrieved from 'category_mapping' dictionary from its key and 'value' gives probability
        st.metric(label=category_mapping[idx], value=f"{probs[idx] * 100:.2f}%")

    # Creating a 'prob_df' to store the crops and their recommendation probabilities for the bar chart
    prob_df = pd.DataFrame({
        "Crop": [category_mapping[i] for i in range(len(probs))],
        "Probability": probs
    })

    # Creating a bar chart
    chart = alt.Chart(prob_df).mark_bar().encode(
        x="Crop",
        y="Probability",
        tooltip=["Crop", "Probability"]   # shows values when you hover
    ).properties(width=700).interactive() # lets you interact

    # Displaying the bar chart
    st.altair_chart(chart)

# ------------------------- Footer -------------------------
st.markdown(
        "<hr><center>🚀 BIA Final Project by <b>Moeed Qaisar</b></center>",
        unsafe_allow_html=True
    )