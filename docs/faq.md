# FAQ

## DDoSSCAN v2.0 — Frequently Asked Questions

---

### General

**Q: What is DDoSSCAN?**

DDoSSCAN is a network availability and stress testing tool written in Python. It is designed for testing the resilience of servers and network infrastructure that you own or have explicit written permission to test.

---

**Q: Is DDoSSCAN free to use?**

Yes. DDoSSCAN is free for personal, educational, and authorized security research use. See [LICENSE.txt](../LICENSE.txt) for the full terms. Commercial redistribution or resale is not permitted.

---

**Q: Who is this tool for?**

- System administrators testing their own servers
- Network engineers performing capacity planning
- Security researchers conducting authorized penetration tests
- Students learning about network security in a lab environment
- CTF participants

---

**Q: Is DDoSSCAN safe to run on my system?**

Yes — the tool runs entirely from your machine and only sends traffic to the target you configure. It does not install any background services, does not phone home, and does not modify your system.

---

### Legal & Safety

**Q: Can I use DDoSSCAN on any target?**

No. You may only use DDoSSCAN on:
- Systems you personally own
- Systems where you have obtained **written permission** from the owner

Testing any other target — even just checking if it responds — without authorization may be illegal in your jurisdiction.

---

**Q: Why does the tool block certain domains automatically?**

DDoSSCAN includes a Domain Safety Blocker that prevents the tool from running tests against government, military, financial, and critical infrastructure domains. This is a built-in safety feature to reduce the risk of misuse. The blocklist covers 298+ entries across all major jurisdictions.

---

**Q: My target got blocked by the safety checker. Can I bypass it?**

No. The blocker exists to protect those domains. If your legitimate test target was incorrectly flagged, it means the domain matches a pattern in the blocklist (e.g. a keyword or TLD). In that case, contact the author to report the false positive.

---

**Q: I work in a SOC / red team — can I use this professionally?**

Yes, provided you have written authorization for each engagement. The tool is suitable for professional authorized testing. Keep documentation of your authorization before running any test.

---

**Q: What laws could I violate by misusing this tool?**

- Indonesia: UU ITE No. 11 / 2008
- USA: Computer Fraud and Abuse Act (CFAA)
- UK: Computer Misuse Act 1990
- EU: Directive 2013/40/EU
- Australia: Criminal Code Act 1995
- Singapore: Computer Misuse Act

Penalties include fines and imprisonment. Do not misuse this tool.

---

### Technical

**Q: What Python version is required?**

Python 3.8 or higher.

---

**Q: What are the required dependencies?**

Required:
```
colorama
```

Optional (for full functionality):
```
requests   — for HTTP analysis features
scapy      — for ARP scanning
paramiko   — for SSH-related features
```

Install with:
```bash
pip install colorama requests scapy paramiko
```

---

**Q: Does it work on Windows?**

Yes. DDoSSCAN is cross-platform and works on Linux, Windows, macOS, and Termux (Android). Some features (like raw socket-based attacks) may require administrator/root privileges on certain systems.

---

**Q: How many threads should I use?**

Start conservatively. For a typical personal VPS or home server:
- **100–300 threads** is a good starting point
- Monitor your server's CPU and memory during testing
- Increase gradually if the server handles the load

The `[3] Smart Calculator` option will suggest parameters based on your available bandwidth.

---

**Q: What does "success rate" mean in the results?**

Success rate is the ratio of successful connections (server responded) to total packets sent. A high success rate (>70%) means your server is handling the load well. A low success rate may indicate the server is dropping connections — which is the expected behavior when a server is under stress.

---

**Q: Why is my packet rate low even with many threads?**

Several possible reasons:
- Your local CPU or network is the bottleneck, not the target
- Your OS has a limit on open file descriptors (sockets) — on Linux, increase with `ulimit -n 65536`
- The target has rate limiting or DDoS protection that drops connections early
- Too many threads for your available bandwidth — use the Smart Calculator

---

**Q: Where are reports saved?**

Reports are saved to the directory where you run the tool:
- Auto-save: `ddosscan_report_YYYYMMDD_HHMMSS.json`
- Manual export: TXT or JSON via `[6] Report Generator`

---

**Q: Can I add my own domains to the blocklist?**

Yes. Open `config/blocked_domains.json` and add entries to the appropriate arrays:
- `blocked_tlds` — for TLD-based blocking (e.g. `.gov`)
- `blocked_keywords_military` — for military keyword matching
- `blocked_keywords_government` — for government keyword matching
- `blocked_domains` — for exact domain matching

---

**Q: The tool shows my target as ALLOWED but I'm not sure it's safe to test.**

The Domain Safety Blocker only catches known patterns. It is **not** a substitute for your own due diligence. If you are unsure whether you are authorized to test a target, **do not test it**.

---

### Contact & Support

**Q: I found a bug. How do I report it?**

Open an issue on GitHub or contact the author directly:

[![GitHub](https://img.shields.io/badge/GitHub-0d1117?style=for-the-badge&logo=github&logoColor=22d3ee)](https://github.com/ruyynn)
[![Email](https://img.shields.io/badge/Email-0d1117?style=for-the-badge&logo=gmail&logoColor=D14836)](mailto:ruyynn25@gmail.com)

---

**Q: Can I contribute to DDoSSCAN?**

Yes. See the contributing guidelines in the README. Pull requests are welcome for bug fixes, new features, and blocklist updates — provided they align with the tool's legitimate use purpose.

---

**Q: How can I support the project?**

<a href="https://saweria.co/Ruyynn" target="_blank">
  <img src="https://user-images.githubusercontent.com/26188697/180601310-e82c63e4-412b-4c36-b7b5-7ba713c80380.png" width="180" alt="Saweria">
</a>

Every donation helps keep development going. Thank you 🙏

---

*DDoSSCAN v2.0 — github.com/ruyynn/DDoSSCAN — by ruyynn*
