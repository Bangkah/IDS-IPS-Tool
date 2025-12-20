# Dockerfile for IDS/IPS Tool (CLI only)
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (for scapy, firewall tools)
RUN apt-get update && \
    apt-get install -y iptables nftables ufw sudo && \
    rm -rf /var/lib/apt/lists/*

# Copy source code
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install .

# By default, run bash for manual CLI usage
CMD ["bash"]

# Example usage:
# docker build -t ids-ips-tool .
# docker run --rm -it --cap-add=NET_ADMIN -v $(pwd):/app ids-ips-tool
# lalu jalankan: python -m ids_main config.json sample.log
