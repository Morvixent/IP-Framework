import os
import requests
import socket
import platform
import time
import whois  # Import the whois package
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)

# Add your IPQualityScore API key here
API_KEY = 'your_ipqualityscore_api_key_here'

def get_connected_wifi_ip():
    try:
        # Get public IP and location info using a public API
        ip_info = requests.get('https://ipinfo.io/json').json()
        public_ip = ip_info['ip']
        city = ip_info.get('city', 'Unknown')
        country = ip_info.get('country', 'Unknown')
        postcode = ip_info.get('postal', 'Unknown')
        loc = ip_info.get('loc', 'Unknown')  # Latitude,Longitude
        
        # Get private IP (local machine IP)
        private_ip = socket.gethostbyname(socket.gethostname())
        
        print(f"Public IP: {public_ip}")
        print(f"Private IP: {private_ip}")
        print(f"City: {city}")
        print(f"Country: {country}")
        print(f"Postcode: {postcode}")
        print(f"Location (Lat, Long): {loc}")
        input("Press Enter to continue...")  # Wait for user input
    except requests.exceptions.RequestException as e:
        print(f"Error fetching IP info: {e}")
        input("Press Enter to continue...")

def check_ip_ping():
    target_ip = input("Enter IP address to ping: ")
    
    # Determine the OS to run the ping command
    if platform.system().lower() == 'windows':
        command = f"ping -n 4 {target_ip}"
    else:
        command = f"ping -c 4 {target_ip}"
    
    os.system(command)
    input("Press Enter to continue...")  # Wait for user input

def research_ip():
    ip_to_research = input("Enter the IP address to research: ")
    
    try:
        # Research IP info using ipinfo.io API
        response = requests.get(f'https://ipinfo.io/{ip_to_research}/json')
        ip_data = response.json()
        
        public_ip = ip_data.get('ip', 'Unknown')
        city = ip_data.get('city', 'Unknown')
        country = ip_data.get('country', 'Unknown')
        postcode = ip_data.get('postal', 'Unknown')
        loc = ip_data.get('loc', 'Unknown')  # Latitude,Longitude
        
        print(f"Public IP: {public_ip}")
        print(f"City: {city}")
        print(f"Country: {country}")
        print(f"Postcode: {postcode}")
        print(f"Location (Lat, Long): {loc}")
        input("Press Enter to continue...")  # Wait for user input
        
    except requests.exceptions.RequestException as e:
        print(f"Error researching IP: {e}")
        input("Press Enter to continue...")

def port_scanner():
    target_ip = input("Enter the IP address to scan: ")
    start_port = int(input("Enter the start port: "))
    end_port = int(input("Enter the end port: "))
    
    print(f"\nScanning {target_ip} from port {start_port} to {end_port}...\n")
    
    # Try each port in the range
    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Set timeout to 1 second
        result = sock.connect_ex((target_ip, port))  # Try to connect
        
        if result == 0:
            print(f"Port {port} is open.")
        else:
            print(f"Port {port} is closed.")
        
        sock.close()
    
    input("Press Enter to continue...")  # Wait for user input

def whois_lookup():
    ip_address = input("Enter the IP address to perform a WHOIS lookup: ")
    
    try:
        # Perform WHOIS lookup using the whois package
        w = whois.whois(ip_address)
        
        print(f"\nWHOIS Information for {ip_address}:\n")
        print(w)  # This will print the WHOIS data, including registrant, contact, etc.
        input("Press Enter to continue...")  # Wait for user input
    
    except Exception as e:
        print(f"Error performing WHOIS lookup: {e}")
        input("Press Enter to continue...")

def vpn_proxy_detection():
    ip_to_check = input("Enter the IP address to check for VPN/Proxy: ")
    
    try:
        # Make a request to the IPQualityScore API
        response = requests.get(f"https://ipqualityscore.com/api/json/ip/{API_KEY}/{ip_to_check}")
        data = response.json()
        
        # Check if the IP address is a VPN, Proxy, or Tor exit node
        if data.get("success", False) == False:
            print(f"Error: {data.get('message', 'Unknown error')}")
            input("Press Enter to continue...")
            return
        
        vpn_status = "Yes" if data.get("vpn", False) else "No"
        proxy_status = "Yes" if data.get("proxy", False) else "No"
        tor_status = "Yes" if data.get("tor", False) else "No"
        
        print(f"\nVPN Detected: {vpn_status}")
        print(f"Proxy Detected: {proxy_status}")
        print(f"Tor Exit Node Detected: {tor_status}")
        
        input("Press Enter to continue...")  # Wait for user input
        
    except requests.exceptions.RequestException as e:
        print(f"Error checking VPN/Proxy status: {e}")
        input("Press Enter to continue...")

# New function for Rate Limit Test
def rate_limit_test():
    ip_or_url = input("Enter the IP address or URL to test rate limit: ")
    test_url = f"http://{ip_or_url}"  # Assuming HTTP, modify if needed
    
    # Send 10 requests to the target and measure responses
    try:
        successful_requests = 0
        start_time = time.time()
        
        # Send 10 requests
        for i in range(10):
            try:
                response = requests.get(test_url)
                if response.status_code == 200:
                    successful_requests += 1
            except requests.exceptions.RequestException:
                print(f"Request {i+1} failed.")
        
        end_time = time.time()
        time_taken = end_time - start_time
        
        # Output the results
        print(f"\nRate Limit Test Results for {ip_or_url}:")
        print(f"Total successful requests: {successful_requests}")
        print(f"Time taken for 10 requests: {time_taken:.2f} seconds")
        
        # Calculate requests per second (RPS)
        rps = successful_requests / time_taken if time_taken > 0 else 0
        print(f"Requests per second: {rps:.2f} RPS")
        
        if successful_requests < 10:
            print("Warning: You might be hitting rate limits.")
        else:
            print("Server is handling the requests well.")
    
        input("Press Enter to continue...")  # Wait for user input
        
    except Exception as e:
        print(f"Error performing rate limit test: {e}")
        input("Press Enter to continue...")

def display_menu():
    os.system('cls' if os.name == 'nt' else 'clear')

    menu_text = f'''
{Fore.YELLOW}██╗██████╗     ███████╗██████╗  █████╗ ███╗   ███╗███████╗██╗    ██╗ ██████╗ ██████╗ ██╗  ██╗
██║██╔══██╗    ██╔════╝██╔══██╗██╔══██╗████╗ ████║██╔════╝██║    ██║██╔═══██╗██╔══██╗██║ ██╔╝
██║██████╔╝    █████╗  ██████╔╝███████║██╔████╔██║█████╗  ██║ █╗ ██║██║   ██║██████╔╝█████╔╝ 
{Fore.RED}██║██╔═══╝     ██╔══╝  ██╔══██╗██╔══██║██║╚██╔╝██║██╔══╝  ██║███╗██║██║   ██║██╔══██╗██╔═██╗ 
██║██║         ██║     ██║  ██║██║  ██║██║ ╚═╝ ██║███████╗╚███╔███╔╝╚██████╔╝██║  ██║██║  ██╗
╚═╝╚═╝         ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝ ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝

{Fore.YELLOW} [Made By Morvixent] ---> https://github.com/Morvixent

{Fore.YELLOW}1) Get Your Connected WiFi's IP
{Fore.RED}2) Check an IP Ping
{Fore.YELLOW}3) Research An IP
{Fore.RED}4) Port Scanner on IP
{Fore.YELLOW}5) Do a WHOIS on an IP
{Fore.RED}6) VPN/Proxy Detection on an IP
{Fore.YELLOW}8) Rate Limit Test on an IP
{Fore.YELLOW}9) Exit
'''
    print(menu_text)

def main():
    while True:
        display_menu()
        try:
            choice = int(input("Select an option: "))
        except ValueError:
            print("Please enter a valid number.")
            continue
        
        if choice == 1:
            get_connected_wifi_ip()
        elif choice == 2:
            check_ip_ping()
        elif choice == 3:
            research_ip()
        elif choice == 4:
            port_scanner()
        elif choice == 5:
            whois_lookup()
        elif choice == 6:
            vpn_proxy_detection()
        elif choice == 8:
            rate_limit_test()  # Call the new Rate Limit Test function
        elif choice == 9:
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice, please select again.")

        time.sleep(2)  # Pause for a moment before showing the menu again

if __name__ == "__main__":
    main()
