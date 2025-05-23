#Developer:Ashar Siddiqui
#Artifact: Security Tool Development  CSC842 Summer 2025
#Lab1
#Create Date: 05/16/2025
#Last Update:  05/22/2025

import argparse
import math
import json
import os
from scapy.all import rdpcap, sniff, DNS, DNSQR
from collections import defaultdict
from datetime import datetime

LOG_FILE = "logs/suspicious_domains.json"

def calculate_entropy(data):
    prob = [float(data.count(c)) / len(data) for c in dict.fromkeys(data)]
    return -sum(p * math.log2(p) for p in prob)

def is_suspicious(domain):
    subdomain = domain.split('.')[0]
    entropy = calculate_entropy(subdomain)
    length = len(subdomain)
    return (entropy > 4.0 or length > 50), entropy, length

def log_suspicious(domain, entropy, length):
    os.makedirs("logs", exist_ok=True)
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "domain": domain,
        "entropy": round(entropy, 2),
        "length": length
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")

def analyze_packet(pkt, domain_stats):
    if pkt.haslayer(DNS) and pkt.getlayer(DNS).qr == 0:
        query = pkt[DNSQR].qname.decode().rstrip('.')
        domain_stats[query] += 1
        suspicious, entropy, length = is_suspicious(query)
        if suspicious:
            print(f"[!] Suspicious Domain: {query}")
            print(f"    ├─ Entropy: {entropy:.2f}")
            print(f"    └─ Length: {length}")
            log_suspicious(query, entropy, length)

def analyze_pcap(pcap_file):
    domain_stats = defaultdict(int)
    packets = rdpcap(pcap_file)
    print(f"[+] Analyzing {len(packets)} packets from {pcap_file}")
    for pkt in packets:
        analyze_packet(pkt, domain_stats)

    print("\n[+] Top Queried Domains:")
    for domain, count in sorted(domain_stats.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  - {domain}: {count} queries")

def live_capture():
    print("[+] Starting live DNS sniffing... Press CTRL+C to stop.\n")
    domain_stats = defaultdict(int)
    try:
        sniff(filter="udp port 53", prn=lambda pkt: analyze_packet(pkt, domain_stats), store=0)
    except KeyboardInterrupt:
        print("\n[+] Stopped live capture.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DNS Exfiltration Detection Tool")
    parser.add_argument("--pcap", help="PCAP file to analyze")
    parser.add_argument("--live", action="store_true", help="Sniff live DNS traffic")
    args = parser.parse_args()

    if args.pcap:
        analyze_pcap(args.pcap)
    elif args.live:
        live_capture()
    else:
        parser.print_help()
