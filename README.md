# 🌩️ Personal Cloud Storage

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)


A lightweight, self-hosted file storage app with Flask. Secure multi-user uploads, downloads, and management—your private Dropbox in <150 lines!

## ✨ Features
- User sign-up/login with hashed passwords
- Per-user private folders
- Upload/download/delete files (auto-rename conflicts)
- Responsive Bootstrap UI (mobile-friendly)
- Session-based auth; in-memory users (easy SQLite upgrade)

## 📸 Screenshots
<img width="220" height="300" alt="Screenshot 2025-11-18 182354" src="https://github.com/user-attachments/assets/429fe9c8-bc56-4f2f-be7e-7ecd83fe78cc" />
<img width="320" height="300" alt="Screenshot 2025-11-18 182436" src="https://github.com/user-attachments/assets/94c0625e-515b-4bb5-8036-5d74c3fe69b3" />
<img width="300" height="300" alt="Screenshot 2025-11-18 182509" src="https://github.com/user-attachments/assets/b3f9dac4-7d09-41d0-ade2-9cb621363d2f" />

## 🚀 Quick Setup
1. Install deps: `pip install -r requirements.txt`
2. Run: `python app.py`
3. Visit: 

## 🌐 Deploy Free
- **Railway/Render**: Link GitHub repo → Auto-deploy in 1 min
- Add env var: `SECRET_KEY=your-random-key`

## 🔒 Notes
- Change `app.secret_key` for prod
- Files in `./uploads/<user>/`

## 📄 License
MIT – See [LICENSE](LICENSE).

*Built with ❤️ by Ashwini Hebbali*
