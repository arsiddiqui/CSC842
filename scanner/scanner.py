#Developer: Ashar Siddiqui
#Date Created: 05/28/2025
#Date Updated: 06/07/2025
#Change Log
# 05/31/2025: Added Service Description
# 06/01/2025: Subnet Scanning
# 06/03/2025:  Add Save
# 06/07/2025: Fixed the error when no argument is provided. 
#CSC 842, Security tool development Cycle 3

import socket
import argparse
import ipaddress
from functools import partial 
from concurrent.futures import ThreadPoolExecutor
import os
import json

#IP to Scan used local for testing

target_IP = "127.0.0.1" 

# Set of commom ports
common_ports = [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 8080]

def scanPort(ip, ports, timeout):
    results = []
    for port in ports: 
        try:
           #Create TCP socket
           s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
           #Time out one second
           s.settimeout(timeout)
           s.connect((ip, port))

           #try to receive a banner
           try:
              banner = s.recv(1024).decode().strip()
           except:
              banner = "No banner received"
           serviceDescription= getServiceDescription(port, banner)
           print(f"Scanning ip - {ip}")
           print(f"Port {port} open - Banner: {banner}")
           print(f"                   |____{serviceDescription}")
           s.close()
           results.append({"ip": ip, "port": port, "status": "open", "banner": banner, "service": serviceDescription})
        except (socket.timeout, socket.error):
           results.append({"ip": ip, "port": port, "status": "closed", "banner": None, "service": None})
    return results

def getServiceDescription(port, banner):
    if banner:
        banner = banner.lower()
        if "ftp" in banner:
            return "FTP"
        elif "http" in banner:
            return "HTTP"
        elif "imap" in banner:
            return "IMAP"
        elif "pop3" in banner:
            return "POP3"
        elif "rdp" in banner:
            return "RDP"
        elif "remote desktop" in banner:
            return "RDP"
        elif "smtp" in banner:
            return "SMPT"
        elif "ssh" in banner:
            return "SSH"
      #if banner is empty or keyword is not found we can assign description to known ports
    knownPorts = {21: "FTP", 22: "SSH", 23: "TELNET", 25: "SMTP", 53: "DNS", 80: "HTTP", 110: "POP3", 139: "NETBIOS", 143: "IMAP", 443: "HTTPS", 445: "SMB", 3389: "RDP" }
    return(knownPorts.get(port, "UNKNOWN"))

def scanSubnet(subnet, ports, timeout, workers=50):
    
   results = []
   ipList = [str(ip) for ip in ipaddress.IPv4Network(subnet,strict=False)]
   scanPartial = partial(scanPort, ports=ports, timeout=timeout)

   with ThreadPoolExecutor(max_workers=workers) as executor:
         allResults = executor.map(scanPartial, ipList)
         for hostResult in allResults:
             results.extend(hostResult)
   return results

def saveAsJson(savePath, results):

    os.makedirs(os.path.dirname(savePath), exist_ok=True)
    with open(savePath, "w") as f:
        json.dump(results, f, indent=4)
    print(f"Results saved to {savePath}")

def main():
    
    
   
    #Get arguments from CLI.
    parser = argparse.ArgumentParser(description="Port scanner &  Banner grabber")
    parser.add_argument("--ip",  help="Target ip address")
    parser.add_argument("--subnet", help="Target subnet in CIDR (e.g 192.168.0.0/24)")
    parser.add_argument("--ports", help="List of ports (e.g 22,23,8080,....)")
    parser.add_argument("--timeout", type=float, default=1.0, help="Timeout for socket connection in seconds, defualt is 1.0 Second")
    parser.add_argument("--output", default="output/Scan_results.json", help="Output file name, default: output/Scan_result.json")
    args = parser.parse_args()
     
    if args.ip or args.subnet:
     
      if args.ports:
          ports = [int(port.strip()) for port in args.ports.split(",")]
      else:
          ports = common_ports
    
      timeout = args.timeout
      #for each port in the list scan IP
      print("Scanning ..........")
      if not args.ports:
          print(f"No port provided, defualt ports will be scanned {common_ports}")

      print(f"|___Ip.... {args.ip}") 
      print(f"   |___Timeout is....{timeout}")

      if args.subnet:
        print(f"      |___Scaning subnet....{args.subnet}")
        results = scanSubnet(args.subnet, ports, timeout) 
        #print(f"Subnaet results: {results}")  
      else:
        print(f"      |___Scaning ports....{ports}")
        results = scanPort(args.ip, ports, timeout)
    
        saveAsJson(args.output, results)
    else:
        print("Either Port or subnet is rquired, scanner --help")
if __name__ == "__main__":
    main()
