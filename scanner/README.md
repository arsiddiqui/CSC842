# 🛡️ DNS Exfiltration Detection Tool

A command-line tool to detect potential DNS tunneling and data exfiltration attempts using entropy-based heuristics.

Developed for **CSC842 - Security tool Development**, this tool analyzes DNS traffic either from a '.pcap' file or via live sniffing and identifies suspicious DNS queries.

---

## 🔍 Features

- Analyze DNS queries from a PCAP file
- Live DNS traffic sniffing (UDP port 53)
- Heuristics-based detection:
  - High entropy subdomains
  - Excessively long subdomain names
- Logs suspicious queries to a JSON file
- CLI interface – no dependencies on web frameworks

---

## ⚙️ Requirements

- Python 3.8+
- [Scapy](https://scapy.readthedocs.io/)
- Root privileges (for live capture)
---

## 📁 Sample PCAP Files
You can download sample PCAP files for testing from the following source:

 - [malware-traffic-analysis](https://www.malware-traffic-analysis.net/training-exercises.html)

---
## 🎥 Tool Demo
Watch the demonstration video on YouTube:

- [DNS Exfiltration Detection - Youtube](https://www.youtube.com/watch?v=V6J6_2B84xI)

Install dependencies:

```bash
pip install scapy





