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

    # कॉन्फिग मधून माहिती मिळवा
    locations_list = config.get('locations', [])
    db_path = config['database']['name']
    csv_path = config['database']['csv_name']

    if not locations_list:
        logger.error("YAML मध्ये कोणतीही शहरे (locations) सापडली नाहीत!")
        return

    logger.info(f"🚀 {len(locations_list)} शहरांसाठी प्रोसेस सुरू होत आहे...")

    # लूप सुरू होतोय - इथेच प्रत्येक शहराची माहिती वेगळी होईल
    for loc in locations_list:
        try:
            # 'loc' हा आता एक डिक्शनरी आहे
            city = loc['city']
            lat = loc['lat']
            lon = loc['lon']

            logger.info(f"📡 {city} चा डेटा घेत आहे...")

            # १. डेटा खेचणे
            raw_data = get_weather_data(lat, lon)

            # २. डेटा स्वच्छ करणे
            clean_df = clean_weather_data(raw_data, city)

            # ३. डेटा सेव्ह करणे
            save_to_sqlite(clean_df, db_path)
            save_to_csv(clean_df, csv_path)

            logger.info(f"✅ {city} चा डेटा यशस्वीरित्या सेव्ह झाला.")

        except Exception as e:
            logger.error(f"❌ {loc.get('city', 'Unknown')} मध्ये त्रुटी: {e}")

    print("\n🏁 पूर्ण मराठवाड्याचा डेटा जमा झाला आहे! 'data' फोल्डर तपासा.")


if __name__ == "__main__":
    run_pipeline()