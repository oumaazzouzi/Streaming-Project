FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000 8501

ENV PYTHONDONTWRITEBYTECODE=1
ENV APP_MODE=flask

CMD ["/bin/sh", "-c", "if [ \"$APP_MODE\" = \"streamlit\" ]; then \
        streamlit run dashboard.py --server.port=8501 --server.enableCORS=false; \
    else \
        python app.py; \
    fi"]
