FROM python:3.12

# Set the working directory
WORKDIR /app

# Install dependencies and Chrome
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    gcc \
    libffi-dev \
    libssl-dev \
    apt-transport-https \
    ca-certificates \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Command to run the Scrapy spider
CMD ["scrapy", "crawl", "imdb_top50", "-o", "output/top50_movies.json"]