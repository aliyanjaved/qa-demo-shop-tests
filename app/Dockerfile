FROM python:3.12-slim
WORKDIR /srv
RUN pip install --no-cache-dir flask
COPY app.py .
COPY templates templates
ENV SEEDED_BUGS=false
EXPOSE 5000
HEALTHCHECK --interval=3s --timeout=3s --retries=10 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')"
CMD ["python", "app.py"]
