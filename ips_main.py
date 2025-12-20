#!/usr/bin/env python3
import sys
from src.config import load_config
from src.ips import IPS

def main():
    if len(sys.argv) < 3:
        print("Usage: python ips_main.py <config.json> <log_file>")
        exit(1)
    config = load_config(sys.argv[1])
    ips = IPS(config)
    ips.analyze_and_block(sys.argv[2])
    print("IPS processing complete.")

if __name__ == "__main__":
    main()
