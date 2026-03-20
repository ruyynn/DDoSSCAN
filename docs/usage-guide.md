# Usage Guide

## DDoSSCAN v2.0 — Network Availability & Stress Testing Tool

---

## Prerequisites

Before running any test, ensure:

1. You **own** the target system, or have **written permission** from the owner
2. Python 3.8+ is installed
3. Required dependencies are installed

```bash
pip install colorama
```

Optional dependencies for full functionality:
```bash
pip install requests scapy paramiko
```

---

## Running the Tool

```bash
python3 src/DDoSSCAN_v2.py
```

On Termux (Android):
```bash
python DDoSSCAN_v2.py
```

---

## Main Menu Overview

```
╔══════════════════════════════════════════════════════════════════════╗
║                   MAIN MENU  —  DDoSSCAN v2.0                        ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  [1]  🎯  Target Preset       WebServer  GameServer  API  Custom     ║
║  [2]  ⚡  Quick Attack        Quick launch with minimal parameters   ║
║  [3]  🧮  Smart Calculator    Calculate optimal parameters  [NEW]    ║
║  [4]  📊  Live Monitor        Real-time stats dashboard  [NEW]       ║
║  [5]  🛡  Domain Safety Check Verify target is allowed  [NEW]        ║
║  [6]  📋  Report Generator    Export results to TXT / JSON  [NEW]    ║
║  [7]  📖  Usage Guide         Guide & recommendations                ║
║  [8]  🔧  Maintenance         Deps  Logs  Session  About             ║
║                                                                      ║
║  [0]     Exit                                                        ║
╚══════════════════════════════════════════════════════════════════════╝
```

---

## Step-by-Step Usage

### Step 1 — Verify Your Target

Always run a **Domain Safety Check** before starting any test.

1. Select `[5] Domain Safety Check` from the main menu
2. Enter the target domain or IP
3. The tool will check against the blocklist and resolve the IP
4. If the target is **ALLOWED** — you may proceed
5. If the target is **BLOCKED** — do not attempt to test it

---

### Step 2 — Choose Your Method

**Option A: Target Preset (Recommended for beginners)**

1. Select `[1] Target Preset`
2. Choose a preset that matches your server type:

| # | Preset | Method | Threads | Duration |
|---|---|---|---|---|
| 1 | Web Server (Apache/Nginx) | HTTP | 500 | 120s |
| 2 | Game Server (UDP) | UDP | 800 | 90s |
| 3 | API Server (REST) | HTTP | 400 | 150s |
| 4 | TCP Service | TCP | 600 | 120s |
| 5 | Connection Limit Test | Slowloris | 300 | 180s |
| 6 | Mixed Stress Test | Mixed | 700 | 120s |

3. Enter your target IP/hostname and port
4. Pass the safety check
5. Type `CONFIRM` to start

---

**Option B: Quick Attack**

For experienced users who want to configure manually:

1. Select `[2] Quick Attack`
2. Enter target IP/hostname
3. Enter port (default: 80)
4. Set threads (recommended: 100–1000 for personal servers)
5. Set duration in seconds (recommended: 60–300)
6. Choose method: `tcp` / `http` / `udp` / `slowloris` / `mixed`
7. Pass the safety check
8. Type `CONFIRM` to start

---

**Option C: Smart Calculator**

Let the tool calculate optimal parameters based on your bandwidth:

1. Select `[3] Smart Calculator`
2. Enter your available bandwidth in Mbps
3. Enter your maximum thread count
4. Review the recommended configuration
5. Enter `y` to use these parameters
6. Set your target and proceed

---

### Step 3 — Monitor in Real-Time

During the test, a live progress bar is shown:

```
  [████████████░░░░░░░░] 61.2%  pkts:24,819  ok:18,204  312/s  061/120s
```

- **pkts** — total packets/requests sent
- **ok** — successful connections
- **/s** — current rate per second
- **time** — elapsed / total duration

---

### Step 4 — Review Results

After the test completes:

```
  [+] Duration     : 120.4s
  [+] Total Packets: 42,310
  [+] Successful   : 31,842
  [+] Errors       : 10,468
  [+] Avg Rate     : 351.4 pkt/s
  [+] Est. BW Used : 0.28 Mbps
  [+] Success Rate : 75.2%
```

A JSON report is auto-saved to the working directory.

---

### Step 5 — Export Report

1. Select `[6] Report Generator`
2. Choose format:
   - `[1]` TXT — human-readable plain text
   - `[2]` JSON — structured data for further analysis
   - `[3]` TXT + JSON — both formats

---

## Attack Methods Explained

### HTTP Flood
- **Layer:** 7 (Application)
- **How it works:** Opens persistent TCP connections and sends rapid HTTP GET requests
- **Best for:** Web servers (Apache, Nginx, IIS)
- **Port:** 80 (HTTP) or 443 (HTTPS)

### TCP Flood
- **Layer:** 4 (Transport)
- **How it works:** Opens TCP connections and sends random payload data
- **Best for:** Generic TCP services
- **Port:** Any TCP port

### UDP Flood
- **Layer:** 4 (Transport)
- **How it works:** Sends rapid UDP datagrams with random payloads (512–1400 bytes)
- **Best for:** Game servers, DNS, streaming services
- **Port:** Any UDP port

### Slowloris
- **Layer:** 7 (Application)
- **How it works:** Opens many partial HTTP connections and keeps them open, exhausting the server's connection pool
- **Best for:** Servers with low connection limits
- **Port:** 80 or 443

### Mixed
- **Layer:** 4 + 7
- **How it works:** Randomly rotates between TCP, HTTP, and UDP methods
- **Best for:** Comprehensive availability testing
- **Port:** Any

---

## Recommended Parameters by Server Type

| Server Type | Threads | Duration | Method | Port |
|---|---|---|---|---|
| Web Server | 300–800 | 120–300s | HTTP | 80/443 |
| Game Server | 500–1000 | 60–180s | UDP | varies |
| API Server | 200–500 | 120–240s | HTTP | 80/443 |
| TCP Service | 400–800 | 120–240s | TCP | varies |
| Connection Test | 200–400 | 180–360s | Slowloris | 80 |

> Start with lower thread counts and increase gradually. Monitor your server's CPU, RAM, and network utilization during testing.

---

## Tips for Effective Testing

- Start low — begin with 100–300 threads and scale up
- Monitor both sides — watch server metrics (CPU, RAM, connections) during the test
- Test at different times — run tests during both low and peak traffic periods
- Use the calculator — let `[3] Smart Calculator` suggest parameters based on your bandwidth
- Keep reports — use `[6] Report Generator` to document baseline vs stress results
- Clean up — use `[8] Maintenance → Clear Reports` to remove old log files

---

## Troubleshooting

| Problem | Likely Cause | Solution |
|---|---|---|
| Low success rate | Server has DDoS protection or rate limiting | This is expected — your server is working correctly |
| Tool errors on start | Missing dependency | Run `pip install colorama` |
| Target blocked by tool | Domain matches safety blocklist | You cannot test this target — use your own server |
| Very low packet rate | Too many threads for your system | Reduce thread count |
| SSL errors on HTTPS | Certificate issues | Expected on self-signed certs — tool handles this |

---

*DDoSSCAN v2.0 — github.com/ruyynn/DDoSSCAN — by ruyynn*
