from send_alert import send_telegram_message  # आपली नवीन फाईल
import logging
from src.extract import get_weather_data
from src.transform import clean_weather_data
from src.load import save_to_sqlite, save_to_csv
from src.utils import load_config, setup_logging


def run_pipeline():
    logger = setup_logging()
    config = load_config()

    if not config:
        print("❌ Config फाईल सापडली नाही!")
        return

    locations_list = config.get('locations', [])
    db_path = config['database']['name']
    csv_path = config['database']['csv_name']

    if not locations_list:
        logger.error("YAML मध्ये कोणतीही शहरे (locations) सापडली नाहीत!")
        return

    logger.info(f"🚀 {len(locations_list)} शहरांसाठी प्रोसेस सुरू होत आहे...")

    for loc in locations_list:
        try:
            city = loc['city']
            lat = loc['lat']
            lon = loc['lon']

            logger.info(f"📡 {city} चा डेटा घेत आहे...")

            # १. डेटा खेचणे
            raw_data = get_weather_data(lat, lon)

            # ---------------------------------------------------------
            # 🔔 नवीन: टेलिग्राम अलर्ट लॉजिक (फक्त इथे ॲड केले आहे)
            # ---------------------------------------------------------
            try:
                # API मधून डेटा चेक करणे (हे OpenWeatherMap च्या फॉरमॅटवर अवलंबून आहे)
                # जर 'current' असेल तर (OneCall API)
                if 'current' in raw_data:
                    temp = raw_data['current']['temp']
                    desc = raw_data['current']['weather'][0]['description']
                # जर 'main' असेल तर (Current Weather API)
                else:
                    temp = raw_data['main']['temp']
                    desc = raw_data['weather'][0]['description']

                print(f"📊 {city}: {desc}, {temp}°C")  # हे टर्मिनलमध्ये दिसेल

                # लॉजिक 1: जर पाऊस असेल
                if "rain" in desc.lower():
                    msg = f"☔ अलर्ट: {city} मध्ये आज पाऊस आहे! ({desc}, {temp}°C). छत्री सोबत ठेवा!"
                    send_telegram_message(msg)
                    logger.info(f"📩 {city} साठी पावसाचा अलर्ट पाठवला.")

                # लॉजिक 2: जर तापमान 35 च्या वर असेल (तुम्ही हे बदलू शकता)
                elif temp > 35:
                    msg = f"🔥 बापरे! {city} मध्ये खूप ऊन आहे! ({temp}°C). काळजी घ्या!"
                    send_telegram_message(msg)
                    logger.info(f"📩 {city} साठी उन्हाचा अलर्ट पाठवला.")

            except Exception as alert_error:
                logger.warning(f"⚠️ अलर्ट पाठवताना छोटी एरर: {alert_error}")
            # ---------------------------------------------------------

            # २. डेटा स्वच्छ करणे (Clean Data)
            clean_df = clean_weather_data(raw_data, city, lat, lon)

            # ३. डेटा सेव्ह करणे (Save Data)
            save_to_sqlite(clean_df, db_path)
            save_to_csv(clean_df, csv_path)

            logger.info(f"✅ {city} चा डेटा यशस्वीरित्या सेव्ह झाला.")

        except Exception as e:
            logger.error(f"❌ {loc.get('city', 'Unknown')} मध्ये त्रुटी: {e}")

    print("\n🏁 पूर्ण मराठवाड्याचा डेटा जमा झाला आहे! 'data' फोल्डर तपासा.")


if __name__ == "__main__":
    run_pipeline()