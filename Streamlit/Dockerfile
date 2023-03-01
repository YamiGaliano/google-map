FROM python:3.10

# Expose port you want your app on
EXPOSE 8080

# Upgrade pip and install requirements
COPY requirements.txt requirements.txt
RUN pip install -U pip
RUN pip install -r requirements.txt

# Copy app code and set working directory
COPY __pycache__ __pycache__
COPY .env .env
COPY Dockerfile Dockerfile
COPY fromdb.py fromdb.py
COPY main.py main.py
COPY pybigQcred.json pybigQcred.json
COPY tobigq.py tobigq.py
WORKDIR .

# Run
ENTRYPOINT [“streamlit”, “run”, “main.py”, “–server.port=8080”, “–server.address=0.0.0.0”]