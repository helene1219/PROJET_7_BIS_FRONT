FROM python:3.9-slim as build
EXPOSE 8000
WORKDIR /app
COPY . .
RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt
ENTRYPOINT ["streamlit", "run", "dashboard.py", "--server.port=8000"]