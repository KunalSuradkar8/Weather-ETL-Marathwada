import requests

# 1. तुमची माहिती इथे टाका (डबल कोट्स मध्ये)
BOT_TOKEN = "8340107395:AAFq4jJG2fcn7k6uuKjLBGP4laOt41TvhVE"
CHAT_ID = "740834009"


def send_telegram_message(message):
    # जर मेसेज रिकामी असेल तर एरर येऊ नये म्हणून चेक
    if not message:
        print("❌ एरर: मेसेज रिकामा आहे!")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print(f"✅ मेसेज गेला: {message}")
        else:
            print(f"❌ टेलिग्राम एरर: {response.text}")
    except Exception as e:
        print(f"❌ कनेक्शन एरर: {e}")


# --- फक्त टेस्ट करण्यासाठी (हा भाग महत्त्वाचा आहे) ---
if __name__ == "__main__":
    send_telegram_message("हे टेस्ट आहे!")