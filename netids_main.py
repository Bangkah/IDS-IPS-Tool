import argparse
from src.config import load_config
from src.netids import NetIDS

def main():
    parser = argparse.ArgumentParser(description="Network IDS ala Suricata (Python)")
    parser.add_argument('config', help='Path to config.json')
    parser.add_argument('--iface', help='Network interface (default: all)', default=None)
    args = parser.parse_args()

    config = load_config(args.config)
    netids = NetIDS(config)
    netids.start(iface=args.iface)

if __name__ == "__main__":
    main()
