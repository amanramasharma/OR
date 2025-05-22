FROM python:3.11-slim

WORKDIR /app/server  # <-- directly run from inside 'server'

COPY requirements.txt ../requirements.txt
RUN pip install --upgrade pip && pip install -r ../requirements.txt

# Copy everything
COPY server/ .       # now /app/server has main.py, db.py, etc.
COPY public_site/ ../public_site/

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
