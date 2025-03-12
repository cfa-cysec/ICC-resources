import socket
import subprocess
import platform
import ipaddress
import shutil
import sys
import os
import urllib.request
import tempfile

def is_admin():
    try:
        return os.geteuid() == 0
    except AttributeError:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    
def install_nmap():
    if not is_admin():
        print("[*] Administrator privileges are required to install nmap.")
        print("[*] Please run this script as an administrator/root and try again.")
        sys.exit(1)

    try:
        if platform.system() == "Windows":
            print("[*] Downloading nmap installer for Windows...")
            nmap_url = "https://nmap.org/dist/nmap-7.95-setup.exe"
            installer_path = os.path.join(tempfile.gettempdir(), "nmap-7.95-setup.exe")
            urllib.request.urlretrieve(nmap_url, installer_path)
            
            print("[*] Installing nmap...")
            subprocess.run([installer_path, "/S"], check=True)
            
            print("[*] Cleaning up...")
            os.remove(installer_path)
            
            print("[*] Adding Nmap path to environment variables...")
            os.environ["PATH"] += os.pathsep + r"C:\Program Files (x86)\Nmap"
        else:
            if shutil.which("apt"):
                subprocess.run(["apt", "update"], check=True)
                subprocess.run(["apt", "install", "-y", "nmap"], check=True)
            elif shutil.which("yum"):
                subprocess.run(["yum", "install", "-y", "nmap"], check=True)
            else:
                print("[*] Unsupported Linux distribution. Please install nmap manually.")
                return False
        
        print("[*] Nmap installed successfully.")
        return True
    except Exception as e:
        print(f"[*] An error occurred while installing nmap: {e}")
        return False

def scan_network_nmap(prefix):
    try:
        output = subprocess.check_output(f"nmap -sV -A -p22,3389 {prefix} --open", shell=True, universal_newlines=True)
        ubuntu_machines = set()
        current_ip = None
        for line in output.split('\n'):
            if "Nmap scan report for" in line:
                current_ip = line.split()[-1]
            if "Linux" in line and current_ip:
                ubuntu_machines.add(current_ip)

        return ubuntu_machines
    except subprocess.CalledProcessError:
        print("[*] Error running nmap. Make sure it's installed and you have necessary permissions.")
        return []

def is_nmap_available():
    return shutil.which("nmap") is not None

def get_private_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

def get_network_address(cidr):
    try:
        network = ipaddress.IPv4Network(cidr, strict=False)
        return network
    except ValueError:
        print("[*] Invalid CIDR notation. Please provide a valid network address.")
        sys.exit(1)

if __name__ == "__main__":

    if len(sys.argv) > 1:
        cidr = sys.argv[1]
    else:
        cidr = input("[*] Please enter the network address in CIDR notation (e.g., 192.168.1.0/24): ")
    
    network = get_network_address(cidr)

    if not is_nmap_available():
        print("[*] Nmap is not installed. Attempting to install...")
        if not install_nmap():
            print("[*] Failed to install Nmap.")
            
    if is_nmap_available():
        print(f"[*] Scanning network {network}")
        ubuntu_machines = scan_network_nmap(network)

        print(f"[*] Found {len(ubuntu_machines)} possible machines:")
        own_ip = get_private_ip()

        for ip in ubuntu_machines:
            clean_ip = ip.replace("(", "").replace(")", "")
            if clean_ip != own_ip:
                print(f"-> {clean_ip}")

