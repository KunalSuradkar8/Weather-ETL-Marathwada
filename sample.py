import sqlite3

# डेटाबेस कनेक्ट करा
conn = sqlite3.connect("data/weather_data.db")
cursor = conn.cursor()

# सर्व टेबल्सची नावे शोधा
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("तुमच्या डेटाबेसमधील टेबल्स:", tables)
conn.close()