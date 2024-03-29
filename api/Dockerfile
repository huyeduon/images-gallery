FROM python:3.10

WORKDIR /app

# Install pipenv
RUN pip install pipenv

# Copy Pipfile and Pipfile.lock
COPY Pipfile Pipfile.lock ./

# Install dependencies using pipenv
RUN pipenv install --deploy --system

# Copy the rest of the application code
COPY . ./

# Expose the port the app runs on
EXPOSE 5050

# Command to run the application
CMD ["python", "main.py"]