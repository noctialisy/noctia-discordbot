FROM python:3.12.7
WORKDIR /usr/src/app/

# Install the application dependencies
RUN apt update
RUN apt install -y git

# Get the app
RUN git clone -b main https://github.com/noctialisy/noctia-discordbot.git .
RUN mv settings_example.json settings.json

# Install venv
RUN python -m venv ./venv/
RUN /usr/src/app/venv/bin/python -m pip install --no-cache-dir -r requirements.txt

# Setup an app user so the container doesn't run as the root user
RUN useradd app
USER app

CMD ["/usr/src/app/venv/bin/python", "main.py"]