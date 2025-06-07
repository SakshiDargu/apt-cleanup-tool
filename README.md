# 🧹 APT Sources Cleanup Tool

[![Made by Sakshi](https://img.shields.io/badge/Created%20by-Sakshi-blue)](https://github.com/SakshiDargu)


A simple Python utility to detect and clean up duplicate or invalid APT source entries in Debian-based systems like Ubuntu.

---

## 📌 Purpose

Detects and disables duplicate entries in `/etc/apt/sources.list` and
removes `.list` files in `/etc/apt/sources.list.d/` that no longer contain valid source lines.

---

## ✅ Prerequisites

**TL;DR:**
```bash
sudo apt install python3-apt python3-regex
```

### Mandatory
- Python 3.4 or higher
- `aptsources` module (from `python3-apt` package)

### Optional
- `regex` module (from `python3-regex`) for better language handling

---

## 📥 Installation

### Option 1: Run from Source (Recommended)

```bash
git clone https://github.com/YOUR_USERNAME/apt-cleanup-tool.git
cd apt-cleanup-tool
sudo python3 src/__main__.py
```

### Option 2: Build a ZIP Executable (Advanced)

You can bundle the script into a `.pyz` zip app using tools like `shiv` or `zipapp`.

---

## 🚀 Usage

### From source:

```bash
sudo python3 src/__main__.py
```

### Example with dry-run:

```bash
sudo python3 src/__main__.py --dry-run
```

---

## ✨ Custom Flag

This version includes a custom flag:
```bash
--hello
```

Try it out:
```bash
python3 src/__main__.py --hello
```

---

## 📈 Future Plans

- Add logging support
- Create a desktop UI
- Support cron-based scheduled cleanups

---

## 👤 Author

Customized by **Sakshi** for personal system maintenance and learning.
Inspired by open-source Linux utilities.
