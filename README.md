<div align="center">

![DDoSSCAN Banner](https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=28&duration=3000&pause=500&color=22D3EE&center=true&vCenter=true&random=false&width=600&height=70&lines=DDoSSCAN+v2.0;Network+Stress+Testing;Infrastructure+Resilience;Professional+Load+Testing)

# 🔥 DDoSSCAN

### *Advanced Network Availability & Stress Testing Framework*

[![Version](https://img.shields.io/badge/Version-2.0.0-22d3ee?style=flat-square&logo=github&logoColor=white)](https://github.com/ruyynn/DDoSSCAN)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-Custom-ff6b6b?style=flat-square&logo=opensourceinitiative&logoColor=white)](LICENSE.txt)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS%20%7C%20Termux-22d3ee?style=flat-square&logo=android&logoColor=white)](https://termux.com)

[![GitHub](https://img.shields.io/badge/GitHub-ruyynn-0d1117?style=flat-square&logo=github)](https://github.com/ruyynn)
[![Facebook](https://img.shields.io/badge/Facebook-@ruyynn-1877F2?style=flat-square&logo=facebook)](https://web.facebook.com/profile.php?id=61587795784907)
[![Email](https://img.shields.io/badge/Email-ruyynn25@gmail.com-D14836?style=flat-square&logo=gmail)](mailto:ruyynn25@gmail.com)
[![Support](https://img.shields.io/badge/Support-Saweria-ff5e5e?style=flat-square&logo=ko-fi)](https://saweria.co/Ruyynn)

</div>

---

## 🚨 **IMPORTANT LEGAL NOTICE**

> ### ⚖️ **For Authorized Testing Only**
> 
> This tool is designed exclusively for:
> - **Security professionals** conducting authorized penetration tests
> - **System administrators** testing their own infrastructure
> - **Network engineers** performing capacity planning
> - **Educational institutions** in controlled lab environments
> 
> **Unauthorized use against any system you do not own or have explicit written permission to test is:**
> - ❌ **ILLEGAL** under international cybercrime laws
> - ❌ **UNETHICAL** and violates responsible disclosure practices
> - ❌ **PUNISHABLE** by imprisonment, fines, and civil liability
> 
> **The author assumes NO responsibility for any misuse. You are solely accountable for your actions.**

---

## 📖 About
 
_DDoSSCAN is an open-source **network availability and stress testing tool** written in Python. It is designed for security researchers, network engineers, and system administrators who need to test the resilience and availability of their own infrastructure._
 
**Key highlights:**
- Built-in **Domain Safety Blocker** — automatically blocks government, military, and critical infrastructure domains
- Multi-vector stress testing: TCP, HTTP, UDP, Slowloris, Mixed
- Smart parameter calculator based on your available bandwidth
- Real-time live statistics dashboard
- Session-based report generator (TXT + JSON)
- Clean VIP terminal interface with animated boot sequence
- Works on Linux, Windows, macOS, and Termux (Android)


## ✨ **What Makes DDoSSCAN Different?**

| Feature | Description | Status |
|---------|-------------|--------|
| 🛡️ **Smart Domain Blocking** | Automatic protection against government/military/critical infrastructure | ✅ **NEW** |
| 📊 **Real-Time Dashboard** | Live statistics with packet counters, success rates, and performance metrics | ✅ **NEW** |
| 🧠 **Bandwidth Calculator** | AI-powered parameter optimization based on your network capacity | ✅ **NEW** |
| 📝 **Session Reports** | Automatic report generation (JSON/TXT) with execution logs | ✅ **NEW** |
| 🎨 **VIP Interface** | Animated terminal UI with professional color scheme | ✅ **NEW** |
| 🔄 **Multi-Vector Attacks** | TCP, HTTP, UDP, Slowloris, and Mixed modes | ✅ **ENHANCED** |
| 📱 **Cross-Platform** | Linux, Windows, macOS, and Termux (Android) support | ✅ |

---

## 🛡️ **Domain Safety System**

DDoSSCAN includes an **automatic domain blocker** that prevents testing against protected infrastructure:

### **Blocked Categories:**

```mermaid
graph LR
    A[Domain Safety System] --> B[Government TLDs]
    A --> C[Military Keywords]
    A --> D[Critical Infrastructure]
    A --> E[Major CDNs]
    A --> F[International Orgs]
    
    B --> B1[.gov, .mil, .go.id, .gouv.fr...]
    C --> C1[army, navy, tni, nato, pentagon...]
    D --> D1[google, facebook, banks, media...]
    E --> E1[cloudflare, akamai, fastly...]
    F --> F1[un.org, who.int, redcross...]
```
```Configurable Blocklist: config/blocked_domains.json```

## 🎯 Use Cases & Permissions

### ✅ Permitted Use

`✔️ Load testing servers you personally own`

`✔️ Stress testing your VPS/cloud instances`

`✔️ Internal network capacity testing`

`✔️ Security research with written authorization`

`✔️ CTF competitions & lab environments`

`✔️ Educational demonstrations`

### ❌ Prohibited Use

`✖️ Attacking any server without explicit written consent`

`✖️ Targeting government, military, or critical infrastructure`

`✖️ DDoS attacks against production systems`

`✖️ Any malicious or illegal activities`

## 🚀 Quick Installation

### 📋 Prerequisites
```bash
Python 3.8+ | pip | git
```
### 💻 Installation Commands

<details> <summary><b>🐧 Linux / macOS</b></summary>

```bash
git clone https://github.com/ruyynn/DDoSSCAN.git
cd DDoSSCAN
pip install colorama
python3 src/DDoSSCAN_v2.py
```

</details><details> <summary><b>🪟 Windows</b></summary>

```bash
git clone https://github.com/ruyynn/DDoSSCAN.git
cd DDoSSCAN
pip install colorama
python src/DDoSSCAN_v2.py
```

</details><details> <summary><b>📱 Termux (Android)</b></summary>

```bash
pkg update && pkg upgrade
pkg install python git
git clone https://github.com/ruyynn/DDoSSCAN.git
cd DDoSSCAN
pip install colorama
python DDoSSCAN_v2.py
```
</details>

### 🔧 Optional Dependencies
```bash
pip install requests scapy paramiko  # Enhanced functionality
```

## 🎮 Attack Methods

| Method|  OSI Layer |  Technique |  Best For |
|-------|------------|------------|-----------|
|HTTP Flood|Layer 7|Exhausts HTTP connection pool|	Web servers, applications|
|TCP Flood|	Layer 4|SYN/ACK connection flood|	Firewalls, stateful devices|
|UDP Flood|	Layer 4|High-bandwidth packet flood| Network infrastructure|
|Slowloris|	Layer 7|Holds connections open|	Apache, threaded servers|
|Mixed Mode|L4 + L7|Rotating attack vectors| Comprehensive testing|

## 📁 Project Structure
```text
DDoSSCAN/
├── 📄 README.md                 # Documentation
├── 📜 LICENSE.txt               # Custom license
├── ⚠️ DISCLAIMER.md            # Legal disclaimer
├── 📋 CHANGELOG.md              # Version history
├── 📁 src/
│   └── 🐍 DDoSSCAN_v2.py       # Main application
├── 📁 config/
│   └── 🛡️ blocked_domains.json # Safety blocklist
└── 📁 docs/
    ├── 📘 usage-guide.md       # Detailed usage
    └── ❓ faq.md               # Frequently asked questions
```

---

## 🔐 Safety Features

> ✅ Automatic domain blocking - No accidental targeting of protected sites

> ✅ Bandwidth throttling - Prevents network saturation

> ✅ Graceful termination - Ctrl+C safely stops all operations

> ✅ Session logging - Complete audit trail of all activities

> ✅ Error handling - Robust exception management

---

## 🤝 Contributing

_We welcome contributions! Please:_

_Fork the repository_

_Create a feature branch_ (`git checkout -b feature/AmazingFeature`)

_Commit your changes_ (`git commit -m 'Add AmazingFeature`)

_Push to branch_ (`git push origin feature/AmazingFeature`)

_Open a Pull Request_

---

## 💖 Support Development
_If DDoSSCAN has helped you in your security research or network testing, consider supporting future development:_

<a href="https://saweria.co/Ruyynn" target="_blank">
  <img src="https://user-images.githubusercontent.com/26188697/180601310-e82c63e4-412b-4c36-b7b5-7ba713c80380.png" width="180" alt="Saweria">
</a>

_Every contribution helps maintain and improve the tool_

</div>

---

## 📜 License

This project is licensed under the **GNU General Public License v3.0**.

You are free to:

> ✅ Use the software

> ✅ Study and modify the source code

> ✅ Share and redistribute the software

> ✅ Create derivative works under the same GPL v3 license

Additional project terms apply, including attribution and project name protection.
See **[ADDITIONAL_TERMS.md](ADDITIONAL_TERMS.md)** for details.

---

## 📞 Contact & Support

| Platform | Link | Action |
|----------|------|--------|
| **💻 GitHub** | [@ruyynn](https://github.com/ruyynn) | [![GitHub](https://img.shields.io/badge/Visit_Profile-0d1117?style=for-the-badge&logo=github&logoColor=22d3ee)](https://github.com/ruyynn) |
| **📘 Facebook** | [@ruyynn](https://web.facebook.com/profile.php?id=61587795784907) | [![Facebook](https://img.shields.io/badge/Visit_Profile-0d1117?style=for-the-badge&logo=facebook&logoColor=22d3ee)](https://web.facebook.com/profile.php?id=61587795784907) |
| **📧 Email** | ruyynn25@gmail.com | [![Email](https://img.shields.io/badge/Send_Email-0d1117?style=for-the-badge&logo=gmail&logoColor=D14836)](mailto:ruyynn25@gmail.com) |


<div align="center">
    
*Use Responsibly. Test Ethically. Secure Proactively.*

**DDoSSCAN v2.0** — Made with 🔥 by **[ruyynn](https://github.com/ruyynn)**

[⬆ Back to Top](#)

</div>
