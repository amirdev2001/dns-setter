import shutil
import requests
from dataclasses import dataclass

@dataclass
class DNSProvider:
    name: str
    primary_ip: str
    secondary_ip: str

class DNSManager:
    def __init__(self):
        self.resolv_conf_path = "/etc/resolv.conf"
        self.backup_path = "/etc/resolv.conf.backup"
        self.test_url = "http://ipinfo.io/json"
        self.dns_providers = [
            DNSProvider("Shekan", "178.22.122.100", "185.51.200.2"),
            DNSProvider("begzar", "185.55.226.26", "185.55.225.25"),
            DNSProvider("radar", "10.202.10.10", "10.202.10.11"),
            DNSProvider("electrotm", "78.157.42.100", "78.157.42.101"),
            DNSProvider("pishgaman", "5.202.100.100", "5.202.100.101"),
            DNSProvider("Level3", "209.244.0.3", "209.244.0.4"),
            DNSProvider("Google DNS", "8.8.8.8", "8.8.4.4"),
            DNSProvider("Cloudflare DNS", "1.1.1.1", "1.0.0.1"),
            DNSProvider("Quad9 DNS", "9.9.9.9", "149.112.112.112"),
            DNSProvider("OpenDNS", "208.67.222.222", "208.67.220.220"),
            DNSProvider("AdGuard DNS", "94.140.14.14", "94.140.15.15"),

            # i think these are not working
            # DNSProvider("shatel", "85.15.1.14", "85.15.1.15"),
            # DNSProvider("beshkanapp", "181.41.194.177", "181.41.194.186"),
            # DNSProvider("sheltertm", "94.103.125.157", "94.103.125.158"),
            # DNSProvider("403online", "10.202.10.202", "10.202.10.102"),
        ]

    def backup_dns(self) -> None:
        shutil.copy2(self.resolv_conf_path, self.backup_path)
        print("📦 DNS settings backed up")

    def restore_dns(self) -> None:
        try:
            shutil.move(self.backup_path, self.resolv_conf_path)
            print("🔄 DNS restored to previous settings")
        except FileNotFoundError:
            print("❌ No backup file found")

    def set_dns(self, provider: DNSProvider) -> None:
        content = "# Custom DNS Configuration\n"
        content += f"nameserver {provider.primary_ip}\n"
        content += f"nameserver {provider.secondary_ip}\n"
        
        with open(self.resolv_conf_path, 'w') as f:
            f.write(content)
        
        print(f"DNS set to: {provider.name} ({provider.primary_ip}, {provider.secondary_ip})")

    def test_dns(self, provider: DNSProvider) -> bool:
        self.set_dns(provider)
        
        try:
            print(f"Testing {provider.name}...")
            response = requests.head(self.test_url, timeout=3)
            print(response)
            if response.status_code == 200:
                print(f"✅ Success: {self.test_url} is reachable using {provider.name}!")
                return True
        except requests.RequestException:
            print(f"❌ Failed: Unable to reach {self.test_url} with {provider.name}")
        return False

    def find_working_dns(self) -> None:
        self.backup_dns()
        
        for provider in self.dns_providers:
            print(f"\nTrying {provider.name}...")
            if self.test_dns(provider):
                print(f"✅ Using {provider.name} as the final DNS")
                return
        
        print("\n❌ No working DNS found. Restoring original settings...")
        self.restore_dns()

def main():
    dns_manager = DNSManager()
    dns_manager.find_working_dns()

if __name__ == "__main__":
    main()
