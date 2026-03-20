# DDoSSCAN

<div align="center">

**Network Availability & Stress Testing Tool**

![Version](https://img.shields.io/badge/Version-2.0.0-22d3ee?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-22d3ee?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-Custom-ff6b6b?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS%20%7C%20Termux-22d3ee?style=for-the-badge)

[![GitHub](https://img.shields.io/badge/GitHub-0d1117?style=for-the-badge&logo=github&logoColor=22d3ee)](https://github.com/ruyynn)
[![Facebook](https://img.shields.io/badge/Facebook-0d1117?style=for-the-badge&logo=facebook&logoColor=22d3ee)](https://web.facebook.com/profile.php?id=61587795784907)
[![Email](https://img.shields.io/badge/Email-0d1117?style=for-the-badge&logo=gmail&logoColor=D14836)](mailto:ruyynn25@gmail.com)

</div>

---

## ⚠️ Disclaimer

> **DDoSSCAN is for authorized testing only.**
> Using this tool against systems you do not own or have written permission to test is **illegal** and may result in criminal prosecution.
> The author is **not responsible** for any misuse.

---

## 📖 About

DDoSSCAN is an open-source **network availability and stress testing tool** written in Python. It is designed for security researchers, network engineers, and system administrators who need to test the resilience and availability of their own infrastructure.

**Key highlights:**
- Built-in **Domain Safety Blocker** — automatically blocks government, military, and critical infrastructure domains
- Multi-vector stress testing: TCP, HTTP, UDP, Slowloris, Mixed
- Smart parameter calculator based on your available bandwidth
- Real-time live statistics dashboard
- Session-based report generator (TXT + JSON)
- Clean VIP terminal interface with animated boot sequence
- Works on Linux, Windows, macOS, and Termux (Android)

---

## 🛡 Domain Safety Blocker

DDoSSCAN includes an automatic domain blocker that **prevents testing against**:

| Category | Examples |
|---|---|
| Government TLDs | `.gov` `.mil` `.go.id` `.gouv.fr` `.gob.mx` `.gc.ca` and 60+ more |
| Military keywords | `army`, `navy`, `tni`, `nato`, `pentagon`, `kopassus`, etc. |
| Government keywords | `congress`, `parliament`, `kremlin`, `kominfo`, etc. |
| Critical infrastructure | Google, Facebook, major banks, media, CDN providers, UN, WHO, etc. |

The full blocked list is maintained in `config/blocked_domains.json` and can be updated independently.

---

## ✅ Permitted Use

- Load testing servers **you own**
- Stress testing your own VPS / cloud instances
- Internal network capacity testing
- Security research with **written permission** from the target owner
- CTF competitions and lab environments

## ❌ Prohibited Use

- Attacking any server without explicit written authorization
- Targeting government, military, or critical infrastructure
- Any form of illegal activity

---

## 🚀 Installation

### Requirements

```
Python 3.8+
```

### Dependencies

```bash
pip install colorama
```

Optional (for full functionality):

```bash
pip install requests scapy paramiko
```

### Clone & Run

```bash
git clone https://github.com/ruyynn/DDoSSCAN.git
cd DDoSSCAN
pip install colorama
python3 src/DDoSSCAN_v2.py
```

### Termux (Android)

```bash
pkg update && pkg upgrade
pkg install python git
git clone https://github.com/ruyynn/DDoSSCAN.git
cd DDoSSCAN
pip install colorama
python DDoSSCAN_v2.py
```

---

## 📋 Features

| Feature | v1.0 | v2.0 |
|---|---|---|
| TCP Flood | ✅ | ✅ |
| HTTP Flood | ✅ | ✅ |
| UDP Flood | ✅ | ✅ |
| Slowloris | ✅ | ✅ |
| Mixed Mode | ✅ | ✅ |
| Domain Safety Blocker | ❌ | ✅ |
| Smart Calculator | ❌ | ✅ |
| Live Monitor Dashboard | ❌ | ✅ |
| Report Generator (TXT/JSON) | ❌ | ✅ |
| VIP Terminal Interface | ❌ | ✅ |
| Animated Boot Sequence | ❌ | ✅ |
| Session Tracker | ❌ | ✅ |
| External Blocklist Config | ❌ | ✅ |

---

## 📊 Attack Methods

| Method | Layer | Description |
|---|---|---|
| HTTP | Layer 7 | Exhausts HTTP connection pool |
| TCP | Layer 4 | TCP connection flood |
| UDP | Layer 4 | High-bandwidth UDP packet flood |
| Slowloris | Layer 7 | Holds connections open to exhaust limits |
| Mixed | L4 + L7 | Rotates between all methods |

---

## 🗂 Project Structure

```
ruyynn/DDoSSCAN
├── README.md
├── LICENSE.txt
├── DISCLAIMER.md
├── CHANGELOG.md
├── src/
│   └── DDoSSCAN_v2.py
├── config/
│   └── blocked_domains.json
└── docs/
    ├── usage-guide.md
    └── faq.md
```

---

## 💖 Support

If this tool has been useful, consider supporting development:

<a href="https://saweria.co/Ruyynn" target="_blank">
  <img src="https://user-images.githubusercontent.com/26188697/180601310-e82c63e4-412b-4c36-b7b5-7ba713c80380.png" width="180" alt="Saweria">
</a>

Every contribution keeps the project going. Thank you 🙏

---

## 📄 License

DDoSSCAN is released under a **Custom License**. See [LICENSE.txt](LICENSE.txt) for full terms.

**TL;DR:** You may use and share this tool for personal and authorized testing. You may **not** modify, sell, or redistribute it without permission. You may **not** remove author credits.

---

<div align="center">

**DDoSSCAN v2.0** — by ruyynn

*Use responsibly. Test only what you own.*

</div>
