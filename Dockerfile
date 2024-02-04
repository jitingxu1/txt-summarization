# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install poetry
RUN poetry install --no-root

# Expose the port that FastAPI and Streamlit will run on
EXPOSE 8501
EXPOSE 8000

# Command to run both applications
CMD ["bash", "-c", "poetry run uvicorn fast_api:app --host 0.0.0.0 --port 8000 & poetry run streamlit run stream_lit.py --server.port 8501"]