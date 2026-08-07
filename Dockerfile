# 1. Base image with Python pre-installed
FROM python:3.11-slim

# 2. Prevent Python from buffering stdout/stderr (helps with live logs)
ENV PYTHONUNBUFFERED=1

# 3. Set the working directory inside the container
WORKDIR /app

# 4. Copy requirements and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy apps, backend, templates, static, manage.py, etc.
COPY . /app/

# 6. Expose Django's default port
EXPOSE 8000

# 7. Run development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]