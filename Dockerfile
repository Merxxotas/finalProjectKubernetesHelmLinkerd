FROM python:3

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages

RUN pip install fastapi
RUN pip install pylint
RUN pip install black
RUN pip install isort
RUN pip install uvicorn
RUN pip install motor
RUN pip install pydantic

# Make port 8000 available to the world outside this container, and port 27017 for the database
EXPOSE 8000
EXPOSE 27017

# Run main.py when the container launches
CMD uvicorn main:app --host 0.0.0.0 --port 8000
