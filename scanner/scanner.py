#Developer: Ashar Siddiqui
#Date Created: 05/28/2025
#Date Updated: 05/31/2025
#CSC 842, Security tool development Cycle 2

import socket

#IP to Scan used local for testing

target_IP = "127.0.0.1" 

# Set of commom ports
common_ports = [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 3389]

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
    print(f"\nScanning {target_IP}...    \n")
    #for each port in the list scan IP
    for port in common_ports:
        scanPort(target_IP, port)

if __name__ == "__main__":
    main()
