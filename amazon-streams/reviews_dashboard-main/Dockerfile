FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# collect local static (css, js, images) into /app/staticfiles
RUN python manage.py  
EXPOSE 8000
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "reviews_dashboard.asgi:application"]
