import sqlite3
import pandas as pd
import os


def save_to_sqlite(df, db_path):
    try:
        conn = sqlite3.connect(db_path)
        df.to_sql('weather_reports', conn, if_exists='append', index=False)
        conn.close()
        return True
    except Exception as e:
        raise Exception(f"Database Load Error: {str(e)}")


def save_to_csv(df, csv_path):
    try:
        # जर फाईल आधीच असेल, तर हेडर (Columns) लिहू नका
        file_exists = os.path.isfile(csv_path)

        # 'a' मोड म्हणजे Append (जुन्या डेटाच्या खाली नवीन डेटा जोडणे)
        df.to_csv(csv_path, mode='a', index=False, header=not file_exists)
        return True
    except Exception as e:
        raise Exception(f"CSV Load Error: {str(e)}")