#Developer: Ashar Siddiqui
#Date Created: 05/28/2025
#Date Updated: 05/31/2025
#CSC 842, Security tool development Cycle 2

import socket
import argparse

#IP to Scan used local for testing

target_IP = "127.0.0.1" 

# Set of commom ports
common_ports = [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 8080]

def scanPort(ip, port):
    try:
        #Create TCP socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #Time out one second
        s.settimeout(1)
        s.connect((ip, port))

        #try to receive a banner
        try:
            banner = s.recv(1024).decode().strip()
        except:
            banner = "No banner received"

        print(f"Port {port} open - Banner: {banner}")
        s.close()

    except socket.timeout:
        pass
    except socket.error:
        pass

def main():
    
    
   
    #Get arguments from CLI.
    parser = argparse.ArgumentParser(description="Port scanner &  Banner grabber")
    parser.add_argument("--ip", required=True, help="Target ip address")
    parser.add_argument("--ports", help="List of ports (e.g 22,23,8080,....)")
    parser.add_argument("--timeout", type=float, default=1.0, help="Timeout for socket connection in seconds, defualt is 1.0 Second")
    parser.add_argument("--output", default="output/Scan_results.json", help="Output file name, default: output/Scan_result.json")
    args = parser.parse_args()
     
    if args.ports:
        ports = [int(port.strip()) for port in args.ports.split(",")]
    else:
        ports = common_ports

#for each port in the list scan IP
    print(f"Scaning ip.... {args.ip}") 
    if not args.ports:
       print(f"No port provided, defualt ports will be scanned {common_ports}")
    for port in ports:
        print(f"Scaning Port : {port}")
        scanPort(args.ip, port)

if __name__ == "__main__":
    main()
