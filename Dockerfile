# Utilizăm imaginea oficială de Python
FROM python:3.12-slim

# Setăm directorul de lucru
WORKDIR /app

# Copiem fișierele proiectului
COPY . /app

# Instalăm dependințele
RUN pip install --no-cache-dir -r requirements.txt

# Expunem portul 5000
EXPOSE 5000

# Comandă de rulare
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
