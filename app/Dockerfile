FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
# Exponer el puerto necesario para tu aplicación
EXPOSE 5000

# Establecer el comando predeterminado para iniciar tu aplicación
CMD ["python", "app.py"]