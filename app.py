# import streamlit as st
# import joblib
# import numpy as np
# import os
# import pandas as pd
# import plotly.express as px

# # -------------------------------
# # Page Configuration
# # -------------------------------
# st.set_page_config(
#     page_title="Hospital Waiting Time Predictor",
#     page_icon="🏥",
#     layout="wide"
# )

# # -------------------------------
# # Dark Mode Toggle
# # -------------------------------
# dark_mode = st.sidebar.checkbox("🌙 Dark Mode")

# # Color Scheme
# if dark_mode:
#     bg_color = "#0E1117"
#     text_color = "white"
#     card_color = "#1f2937"
#     secondary_text = "#cbd5e1"
# else:
#     bg_color = "#F4F6F9"
#     text_color = "black"
#     card_color = "#ffffff"
#     secondary_text = "#7f8c8d"

# # -------------------------------
# # CSS Styling
# # -------------------------------
# st.markdown(f"""
# <style>
# /* Page background */
# [data-testid="stAppViewContainer"] {{
#     background-color: {bg_color};
#     color: {text_color};
# }}

# /* Sidebar background */
# [data-testid="stSidebar"] {{
#     background-color: {card_color};
#     color: {text_color};
# }}

# /* Sidebar radio buttons */
# div[role="radiogroup"] label {{
#     color: {text_color} !important;
#     font-weight: 600;
# }}

# div[role="radiogroup"] input[type="radio"] {{
#     accent-color: #1abc9c;
# }}

# /* Card styling */
# .card {{
#     background-color: {card_color};
#     border-radius: 16px;
#     padding: 20px;
#     margin-top: 20px;
#     box-shadow: 0px 6px 20px rgba(0,0,0,0.2);
#     transition: transform 0.2s;
# }}
# .card:hover {{
#     transform: scale(1.03);
# }}

# /* Buttons */
# .stButton>button {{
#     background-color: #1abc9c;
#     color: white;
#     font-size: 16px;
#     border-radius: 10px;
#     padding: 8px 0;
# }}

# /* Form labels */
# label {{
#     color: {text_color} !important;
# }}
# </style>
# """, unsafe_allow_html=True)

# # -------------------------------
# # Load Models
# # -------------------------------
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# reg_model = joblib.load(os.path.join(BASE_DIR, "models", "regression_model.pkl"))
# cls_model = joblib.load(os.path.join(BASE_DIR, "models", "classification_model.pkl"))

# # -------------------------------
# # Sidebar Navigation
# # -------------------------------
# st.sidebar.title("🏥 Navigation")
# page = st.sidebar.radio("", ["Home", "Predict", "Graphs"])

# # -------------------------------
# # Home Page
# # -------------------------------
# if page == "Home":
#     st.title("🏥 Patient Waiting Time Prediction System")
#     st.markdown(f"""
#     <p style='color:{secondary_text}; font-size:18px;'>
#     Welcome to the <b>Hospital Waiting Time Predictor</b>.<br>
#     This system predicts <b>how long a patient will wait</b> based on:
#     </p>
#     <ul style='color:{secondary_text}'>
#         <li>Arrival Hour</li>
#         <li>Queue Length</li>
#         <li>Doctors Available</li>
#         <li>Patient Age</li>
#         <li>Triage Level</li>
#     </ul>
#     """, unsafe_allow_html=True)

# # -------------------------------
# # Prediction Page
# # -------------------------------
# elif page == "Predict":
#     st.title("🔍 Predict Waiting Time")

#     with st.form(key="patient_form"):
#         st.subheader("📋 Patient Information")
#         arrival_hour = st.slider("Arrival Hour", 0, 23)
#         patient_age = st.number_input("Patient Age", min_value=0, max_value=100)
#         triage_level = st.selectbox(
#             "Triage Level",
#             [1, 2, 3],
#             help="1 = Emergency | 2 = Moderate | 3 = Low priority"
#         )

#         st.subheader("🏥 Hospital Status")
#         queue_length = st.number_input("Queue Length", min_value=0, max_value=50)
#         doctors_available = st.number_input("Doctors Available", min_value=1, max_value=10)

#         submit_button = st.form_submit_button("🔍 Predict Waiting Time")

#     if submit_button:
#         features = np.array([[arrival_hour, queue_length, doctors_available, triage_level, patient_age]])
#         waiting_time = reg_model.predict(features)[0]
#         category = cls_model.predict(features)[0]

#         # -------------------------------
#         # Minimal Attractive Card
#         # -------------------------------
#         st.markdown(f'<div class="card">', unsafe_allow_html=True)
#         col1, col2 = st.columns(2)

#         with col1:
#             st.markdown(f"<h3 style='color:{text_color}'>⏱ Waiting Time</h3>", unsafe_allow_html=True)
#             st.markdown(f"<h2 style='color:#1abc9c'>{round(waiting_time,2)} minutes</h2>", unsafe_allow_html=True)

#         with col2:
#             st.markdown(f"<h3 style='color:{text_color}'>📊 Category</h3>", unsafe_allow_html=True)
#             if category == "Short":
#                 st.markdown(f"<h2 style='color:#2ecc71'>{category}</h2>", unsafe_allow_html=True)
#             elif category == "Medium":
#                 st.markdown(f"<h2 style='color:#f39c12'>{category}</h2>", unsafe_allow_html=True)
#             else:
#                 st.markdown(f"<h2 style='color:#e74c3c'>{category}</h2>", unsafe_allow_html=True)

#         st.markdown("</div>", unsafe_allow_html=True)

# # -------------------------------
# # Graphs Page
# # -------------------------------
# elif page == "Graphs":
#     st.title("📊 Visual Analytics")

#     st.sidebar.subheader("Graph Options")
#     graph_option = st.sidebar.selectbox(
#         "Select Graph",
#         ["Hospital Load", "Patient Arrival Trend"]
#     )

#     if graph_option == "Hospital Load":
#         st.subheader("Input Factors Affecting Waiting Time")
#         data = pd.DataFrame({
#             "Factor": ["Queue Length","Doctors Available","Arrival Hour","Patient Age","Triage Level"],
#             "Value": [
#                 queue_length if 'queue_length' in locals() else 10,
#                 doctors_available if 'doctors_available' in locals() else 3,
#                 arrival_hour if 'arrival_hour' in locals() else 9,
#                 patient_age if 'patient_age' in locals() else 30,
#                 triage_level if 'triage_level' in locals() else 2
#             ]
#         })
#         fig = px.bar(
#             data, x="Factor", y="Value", color="Factor",
#             text="Value", color_discrete_sequence=px.colors.sequential.Teal
#         )
#         st.plotly_chart(fig, use_container_width=True)

#     elif graph_option == "Patient Arrival Trend":
#         st.subheader("Simulated Patient Arrival Trend")
#         sample_data = pd.DataFrame({
#             "Hour": list(range(24)),
#             "Patients": [np.random.randint(5,50) for i in range(24)]
#         })
#         fig2 = px.line(
#             sample_data, x="Hour", y="Patients", markers=True,
#             line_shape='spline', color_discrete_sequence=['#1abc9c']
#         )
#         st.plotly_chart(fig2, use_container_width=True)

# # -------------------------------
# # Footer
# # -------------------------------
# st.sidebar.caption("Machine Learning Project | Streamlit + Random Forest")



import streamlit as st
import joblib
import numpy as np
import os
import pandas as pd
import plotly.express as px

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Hospital Waiting Time Predictor",
    page_icon="🏥",
    layout="wide"
)

# -------------------------------
# Fixed Light Mode Colors
# -------------------------------
bg_color = "#F4F6F9"
text_color = "black"
card_color = "#ffffff"
secondary_text = "#7f8c8d"

# -------------------------------
# CSS Styling
# -------------------------------
st.markdown(f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-color: {bg_color};
    color: {text_color};
}}
[data-testid="stSidebar"] {{
    background-color: {card_color};
    color: {text_color};
}}
div[role="radiogroup"] label {{
    color: {text_color} !important;
    font-weight: 600;
}}
div[role="radiogroup"] input[type="radio"] {{
    accent-color: #1abc9c;
}}
.card {{
    background-color: {card_color};
    border-radius: 16px;
    padding: 20px;
    margin-top: 20px;
    box-shadow: 0px 6px 20px rgba(0,0,0,0.2);
    transition: transform 0.2s;
}}
.card:hover {{
    transform: scale(1.03);
}}
.stButton>button {{
    background-color: #1abc9c;
    color: white;
    font-size: 16px;
    border-radius: 10px;
    padding: 8px 0;
}}
label {{
    color: {text_color} !important;
}}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# Load Models
# -------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
reg_model = joblib.load(os.path.join(BASE_DIR, "models", "regression_model.pkl"))
cls_model = joblib.load(os.path.join(BASE_DIR, "models", "classification_model.pkl"))

# -------------------------------
# Sidebar Navigation
# -------------------------------
st.sidebar.title("🏥 Navigation")
page = st.sidebar.radio("Select page", ["Home", "Predict", "Graphs"])

# -------------------------------
# Home Page
# -------------------------------
if page == "Home":
    st.title("🏥 Patient Waiting Time Prediction System")
    st.markdown(f"""
    <p style='color:{secondary_text}; font-size:18px;'>
    Welcome to the <b>Hospital Waiting Time Predictor</b>.<br>
    This system predicts <b>how long a patient will wait</b> based on:
    </p>
    <ul style='color:{secondary_text}'>
        <li>Arrival Hour</li>
        <li>Queue Length</li>
        <li>Doctors Available</li>
        <li>Patient Age</li>
        <li>Triage Level</li>
    </ul>
    """, unsafe_allow_html=True)

# -------------------------------
# Prediction Page
# -------------------------------
elif page == "Predict":
    st.title("🔍 Predict Waiting Time")
    with st.form(key="patient_form"):
        st.subheader("📋 Patient Information")
        arrival_hour = st.slider("Arrival Hour", 0, 23)
        patient_age = st.number_input("Patient Age", min_value=0, max_value=100)
        triage_level = st.selectbox(
            "Triage Level",
            [1, 2, 3],
            help="1 = Emergency | 2 = Moderate | 3 = Low priority"
        )
        st.subheader("🏥 Hospital Status")
        queue_length = st.number_input("Queue Length", min_value=0, max_value=50)
        doctors_available = st.number_input("Doctors Available", min_value=1, max_value=10)
        submit_button = st.form_submit_button("🔍 Predict Waiting Time")

    if submit_button:
        features = np.array([[arrival_hour, queue_length, doctors_available, triage_level, patient_age]])
        waiting_time = reg_model.predict(features)[0]
        category = cls_model.predict(features)[0]

        st.markdown(f'<div class="card">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"<h3 style='color:{text_color}'>⏱ Waiting Time</h3>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='color:#1abc9c'>{round(waiting_time,2)} minutes</h2>", unsafe_allow_html=True)

        with col2:
            st.markdown(f"<h3 style='color:{text_color}'>📊 Category</h3>", unsafe_allow_html=True)
            if category == "Short":
                st.markdown(f"<h2 style='color:#2ecc71'>{category}</h2>", unsafe_allow_html=True)
            elif category == "Medium":
                st.markdown(f"<h2 style='color:#f39c12'>{category}</h2>", unsafe_allow_html=True)
            else:
                st.markdown(f"<h2 style='color:#e74c3c'>{category}</h2>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------
# Graphs Page
# -------------------------------
elif page == "Graphs":
    st.title("📊 Visual Analytics")
    st.sidebar.subheader("Graph Options")
    graph_option = st.sidebar.selectbox(
        "Select Graph",
        ["Hospital Load", "Patient Arrival Trend"]
    )

    if graph_option == "Hospital Load":
        st.subheader("Input Factors Affecting Waiting Time")
        data = pd.DataFrame({
            "Factor": ["Queue Length","Doctors Available","Arrival Hour","Patient Age","Triage Level"],
            "Value": [
                queue_length if 'queue_length' in locals() else 10,
                doctors_available if 'doctors_available' in locals() else 3,
                arrival_hour if 'arrival_hour' in locals() else 9,
                patient_age if 'patient_age' in locals() else 30,
                triage_level if 'triage_level' in locals() else 2
            ]
        })
        fig = px.bar(
            data, x="Factor", y="Value", color="Factor",
            text="Value", color_discrete_sequence=px.colors.sequential.Teal
        )
        st.plotly_chart(fig, use_container_width=True)

    elif graph_option == "Patient Arrival Trend":
        st.subheader("Simulated Patient Arrival Trend")
        sample_data = pd.DataFrame({
            "Hour": list(range(24)),
            "Patients": [np.random.randint(5,50) for i in range(24)]
        })
        fig2 = px.line(
            sample_data, x="Hour", y="Patients", markers=True,
            line_shape='spline', color_discrete_sequence=['#1abc9c']
        )
        st.plotly_chart(fig2, use_container_width=True)

# -------------------------------
# Footer
# -------------------------------
st.sidebar.caption("Machine Learning Project | Streamlit + Random Forest")