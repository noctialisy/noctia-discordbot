FROM python:3.12.7
WORKDIR /usr/src/app/

# Install the application dependencies
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
RUN python -m pip install -U py-cord

# Copy in the source code
COPY Procfile.txt ./
COPY runtime.txt ./
COPY main.py ./
COPY settings.json ./
COPY game_classes ./game_classes
COPY game_saves ./game_saves

# Setup an app user so the container doesn't run as the root user
RUN useradd app
USER app

CMD ["python", "main.py"]