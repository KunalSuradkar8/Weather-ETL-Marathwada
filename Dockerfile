# 1. Base Image: Python चे छोटे व्हर्जन वापरू (Linux वर आधारित)
FROM python:3.9-slim

# 2. Work Directory: कंटेनरमध्ये एक फोल्डर बनवू
WORKDIR /app

# 3. Requirements कॉपी करू आणि इन्स्टॉल करू
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. आपला बाकीचा कोड कॉपी करू
COPY . .

# 5. Streamlit चा पोर्ट उघडा (Streamlit 8501 वर चालते)
EXPOSE 8501

# 6. कमांड: कंटेनर सुरू झाल्यावर काय रन करायचे?
CMD ["streamlit", "run", "dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]