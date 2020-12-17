FROM python:3.8.6
#EXPOSE 8005
COPY requirements.txt .
RUN pip install -r requirements.txt
#COPY . .
#COPY .env .
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]