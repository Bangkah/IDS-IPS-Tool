import argparse
from firewall.manager import FirewallManager

def main():
    parser = argparse.ArgumentParser(description="Firewall Management Tool (iptables/nftables/ufw)")
    parser.add_argument('--block', metavar='IP', help='Blokir IP address')
    parser.add_argument('--unblock', metavar='IP', help='Unblock IP address')
    parser.add_argument('--list', action='store_true', help='List blocked IPs')
    parser.add_argument('--backend', choices=['auto', 'iptables', 'nftables', 'ufw'], default='auto', help='Pilih backend firewall')
    args = parser.parse_args()

    fw = FirewallManager(backend=args.backend)

    if args.block:
        fw.block_ip(args.block)
    elif args.unblock:
        fw.unblock_ip(args.unblock)
    elif args.list:
        fw.list_blocked()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
