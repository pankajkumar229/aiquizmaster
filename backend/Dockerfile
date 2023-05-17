FROM python:3.6

# Creating Application Source Code Directory
RUN mkdir -p /src

# Setting Home Directory for containers
WORKDIR /src

# Installing python dependencies
COPY requirements.txt /src
RUN pip install --no-cache-dir -r requirements.txt

# Copying src code to Container
COPY . /src/

# Exposing Ports
EXPOSE 5035

# Running Python Application
CMD ["python", "app.py"]
