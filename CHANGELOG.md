# Changelog

All notable changes to DDoSSCAN are documented here.

---

## [2.0.0] — 2026-03-20

### Added

- **Domain Safety Blocker** — Automatic blocking of government, military, financial, and critical infrastructure domains. Blocklist loaded from external `config/blocked_domains.json` with 298+ entries covering international domains across 6 continents
- **Smart Parameter Calculator** — Input your available bandwidth and max threads; tool auto-calculates optimal configuration
- **Live Monitor Dashboard** — Real-time session statistics with rating system (★ to ★★★★★)
- **Report Generator** — Export test results to TXT and JSON formats with auto-save after every session
- **Session Tracker** — Persistent session ID, uptime counter, and findings log across the entire run
- **VIP Terminal Interface** — Full box-drawing UI engine with consistent layout, status bar, and color theme
- **Animated Boot Sequence** — 5-stage boot animation with per-stage progress bars
- **Target Presets** — 6 built-in presets for common server types (Web, Game, API, TCP, Slowloris, Mixed)
- **Maintenance Menu** — Dependency checker, log cleaner, session info, about page
- **Domain Safety Check** — Standalone menu option to verify if a target is allowed before running any test
- **External Blocklist Config** — Domain blocklist separated from source code into `config/blocked_domains.json` for easy updates
- **Full English UI** — All interface text, prompts, warnings, and reports in English

### Changed

- Rewrote entire UI from basic colored text to structured box-drawing terminal interface
- Replaced static thread launcher with `ThreadPoolExecutor` for cleaner thread management
- Improved real-time stats display with proper progress bar and per-second rate counter
- Moved all hardcoded domain lists out of source code into external JSON config
- Confirmation flow now requires typing `CONFIRM` (uppercase) to prevent accidental launches

### Fixed

- Thread cleanup after attack completion
- SSL context handling for HTTPS targets
- Stats counter race condition under high thread counts

---

## [1.3.0] — 2026

### Added

- HTTP POST flood method
- SYN flood (raw socket attempt with TCP fallback)
- DNS amplification vector (educational demonstration)
- Auto-save results to JSON after each session
- Installation script (`install.sh`)

### Changed

- Improved HTTP flood with keep-alive and multiple requests per connection
- Better error handling in bruteforce modules

---

## [1.0.0] — 2025

### Initial Release

- TCP Flood
- HTTP Flood (GET)
- UDP Flood
- Slowloris
- Mixed mode (rotates between methods)
- Target preset system (Web Server, Game Server, VPN, API, Router)
- Quick Calculator (bandwidth-based parameter estimation)
- Real-time statistics display
- Basic usage guide in-tool
- Results saved to JSON

---

*DDoSSCAN — github.com/ruyynn/DDoSSCAN*
