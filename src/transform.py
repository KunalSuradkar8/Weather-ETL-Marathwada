import pandas as pd
from datetime import datetime


def clean_weather_data(raw_data, city):
    print("🛠️ डेटा क्लीनिंग आणि ट्रान्सफॉर्मेशन सुरू आहे...")
    df = pd.DataFrame([raw_data])

    # अनावश्यक गोष्टी काढून नवीन कॉलम जोडणे
    df['city'] = city
    df['processed_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # कॉलमची नावे नीट करणे
    df = df[['city', 'time', 'temperature', 'windspeed', 'processed_at']]
    return df