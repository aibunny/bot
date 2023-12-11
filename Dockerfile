FROM python:3.11

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir uvicorn

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

# Run app.py when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
