import streamlit as st
import sqlite3
import pandas as pd
import os

# --- पेज सेटिंग्ज ---
st.set_page_config(page_title="मराठवाडा वेदर डॅशबोर्ड", layout="wide")

st.title("🌦️ मराठवाडा वेदर डॅशबोर्ड")
st.markdown("हा डॅशबोर्ड **weather_data.db** मधून रिअल-टाइम डेटा दाखवतो.")


# --- डेटाबेस कनेक्शन फंक्शन ---
# --- डेटाबेस कनेक्शन फंक्शन ---
# --- डेटाबेस कनेक्शन फंक्शन ---
def load_data():
    # डेटाबेसचा पाथ (Path) सेट करा
    db_path = os.path.join("data", "weather_data.db")

    # चेक करा की डेटाबेस अस्तित्वात आहे का
    if not os.path.exists(db_path):
        st.error(f"⚠️ एरर: '{db_path}' ही फाईल सापडली नाही! कृपया आधी main.py रन करून डेटा जमा करा.")
        return pd.DataFrame()

    try:
        # डेटाबेस कनेक्ट करा
        conn = sqlite3.connect(db_path)

        # ✅ सुधारणा: इथे टेबलचे नाव 'weather_reports' केले आहे (तुमच्या DB प्रमाणे)
        query = "SELECT * FROM weather_reports"

        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"⚠️ डेटाबेस वाचताना एरर आला: {e}")
        return pd.DataFrame()


# --- डेटा लोड करणे ---
df = load_data()
if not df.empty:
    # --- डेटा प्रीव्यू (Data Preview) ---
    st.subheader("📊 सध्याचा डेटा (Recent Data)")
    st.dataframe(df.tail(10))  # शेवटच्या 10 नोंदी दाखवा

    # --- मेट्रिक्स (Metrics) ---
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="एकूण नोंदी", value=len(df))
    with col2:
        avg_temp = df['temperature'].mean() if 'temperature' in df.columns else 0
        st.metric(label="सरासरी तापमान", value=f"{avg_temp:.2f} °C")
    with col3:
        avg_hum = df['humidity'].mean() if 'humidity' in df.columns else 0
        st.metric(label="सरासरी आर्द्रता (Humidity)", value=f"{avg_hum:.2f} %")

    # --- ग्राफ्स (Charts) ---
    st.markdown("---")

    # शहरांनुसार तापमान (Bar Chart)
    if 'city' in df.columns and 'temperature' in df.columns:
        st.subheader("🌡️ शहरानुसार तापमान")
        # सर्वात अलीकडील डेटा घेण्यासाठी
        latest_data = df.drop_duplicates(subset=['city'], keep='last')
        st.bar_chart(latest_data.set_index('city')['temperature'])

    # ह्युमिडिटी लाईन चार्ट
    if 'timestamp' in df.columns and 'humidity' in df.columns:
        st.subheader("💧 आर्द्रता (Humidity) ट्रेंड")
        st.line_chart(df.set_index('timestamp')['humidity'])

else:
    st.warning("डेटाबेस रिकामा आहे किंवा कनेक्ट झालेला नाही.")