# Auto Gmail Creator

This is a Termux-compatible Gmail account creator script using **Firefox headless**.

## Setup

```bash
pkg update -y && pkg upgrade -y
pkg install -y python firefox geckodriver git
git clone https://github.com/YOUR_USERNAME/Auto-Gmail-Creator.git
cd Auto-Gmail-Creator
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
