# Use an official Python runtime as the base image
FROM python:3.12-slim AS base

# It is necessary to install git to run the pip install -r requirements.txt
RUN apt-get update && apt-get install -y git

RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
	PATH=/home/user/.local/bin:$PATH

# Set the working directory in the container
WORKDIR $HOME/app

# Copy the current directory contents into the container at /app
COPY --chown=user . $HOME/app

RUN pip install -r requirements.txt

FROM base AS test

CMD ["python", "-m", "pdb", "app.py"]

FROM base AS run

CMD ["python", "app.py"]
