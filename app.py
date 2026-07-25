import re
import string
import warnings

import joblib
import nltk
import streamlit as st

from tensorflow.keras.models import load_model

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from url_scanner import extract_url_features
from heuristic_engine import calculate_risk
from gemini_explainer import explain_url

warnings.filterwarnings("ignore")

nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)
nltk.download("omw-1.4", quiet=True)

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

FILE_EXTENSIONS = {
    "pdf","doc","docx",
    "xls","xlsx",
    "ppt","pptx",
    "csv","txt",
    "zip","rar",
    "jpg","jpeg",
    "png","gif"
}

@st.cache_resource
def load_artifacts():
    model = load_model("Models/phishing_email_model.keras")
    vectorizer = joblib.load("Models/tfidf_vectorizer.pkl")
    return model, vectorizer

model, vectorizer = load_artifacts()

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", " urltoken ", text)
    text = re.sub(r"\S+@\S+", " emailtoken ", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\b\d+\b", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    processed_words = []
    for word in text.split():
        if word in stop_words:
            continue
        if word in FILE_EXTENSIONS:
            continue
        word = lemmatizer.lemmatize(word)
        processed_words.append(word)

    return " ".join(processed_words)

st.set_page_config(page_title="PhishGuard AI", layout="wide")

page = st.sidebar.radio(
    "🛡️ Navigation",
    ["📧 Email Scanner", "🌐 URL Scanner", "ℹ️ About"]
)

if page == "📧 Email Scanner":
    st.title("📧 AI-Powered Phishing Email Detection")
    st.caption("Use Natural Language Processing and Machine Learning to identify phishing emails.")
    st.divider()

    st.markdown("""
    This application analyzes email content and predicts whether it is a **Legitimate Email** or a **Phishing Email** using a trained Neural Network model.
    """)

    st.subheader("📩 Enter Email Content")
    
    email_text = st.text_area("Email Text", placeholder="Paste email here...", label_visibility="collapsed")


    col1, col2 = st.columns([3,1])
    with col1:
        predict_button = st.button(" Detect Email", use_container_width=True, key="email_detect_btn")
    with col2:
        clear_button = st.button("Clear", use_container_width=True, key="email_clear_btn")

    if clear_button:
        st.rerun()

    st.divider()

    if predict_button:
        if email_text.strip() == "":
            st.warning("Please enter an email.")
        else:
            with st.spinner("Analyzing email..."):
                cleaned_email = preprocess_text(email_text)
                email_vector = vectorizer.transform([cleaned_email])
                
                probability = float(model.predict(email_vector.toarray(), verbose=0)[0][0])
                predicted_label = 1 if probability >= 0.5 else 0
                confidence = max(probability, 1 - probability) * 100

            st.subheader("Prediction Result")
            if predicted_label == 1:
                st.error("🚨 Phishing Email Detected")
            else:
                st.success(" Legitimate Email")

            st.metric("Confidence", f"{confidence:.2f}%")
            st.progress(confidence / 100)

            st.write("### Prediction Probability")
            st.write(f"Phishing : **{probability:.4f}**")
            st.write(f"Legitimate : **{1-probability:.4f}**")
elif page == "🌐 URL Scanner":
    st.title("🌐 AI-Powered URL Risk Analysis")
    st.caption("Scan suspicious links and get actionable cybersecurity insights.")
    st.divider()
    
    st.subheader("🔗 Enter URL to Scan")
    
    url = st.text_input("URL", placeholder="https://www.example.com/login", label_visibility="collapsed")
    
    scan_button = st.button("🔍 Scan URL", use_container_width=True, key="url_scan_btn")
    
    st.divider()
    
    if scan_button:
        if url.strip() == "":
            st.warning("Please enter a URL.")
        else:
            with st.spinner("Extracting features and analyzing risk..."):
                features = extract_url_features(url)
                risk = calculate_risk(features)
                ai_response = explain_url(url, features, risk)

            st.metric("Risk Score", f"{risk['risk_score']}/100")
            
            st.subheader("Risk Level")
            if risk["risk_level"] == "Critical":
                st.error(risk["risk_level"])
            elif risk["risk_level"] == "High":
                st.error(risk["risk_level"])
            elif risk["risk_level"] == "Medium":
                st.warning(risk["risk_level"])
            else:
                st.success(risk["risk_level"])

            st.subheader("Why was this URL flagged?")
            if risk["reasons"]:
                for reason in risk["reasons"]:
                    st.write(f"• {reason}")
            else:
                st.write("• No immediate suspicious heuristic indicators found.")

            st.subheader(" AI Security Analysis")
            st.markdown(ai_response)

elif page == "ℹ️ About":
    st.title("About PhishGuard AI")
    st.write("""
    PhishGuard AI is an AI-powered cybersecurity application.

    **Features:**
    *   Email phishing detection
    *   URL risk analysis
    *   Risk scoring heuristics
    *   Explainable AI 
    *   Machine Learning & NLP
    *   Generative AI integrations
    """)