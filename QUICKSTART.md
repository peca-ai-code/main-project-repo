# Quick Start Guide 🚀

Get the Gynecology Chatbot running in just a few minutes!

## ⚡ Super Quick Setup

### 1. One-Command Setup
```bash
./setup_dev_environment.sh
```

### 2. Add Your API Keys
Edit `backend/.env`:
```env
OPENAI_API_KEY=your_openai_key_here
GEMINI_API_KEY=your_gemini_key_here
```

Edit `chainlit_app/.env`:
```env
GEMINI_API_KEY=your_gemini_key_here
DJANGO_API_TOKEN=your_jwt_token_from_setup
```

### 3. Start the Application
```bash
./run_servers.sh
```

### 4. Test Everything
```bash
./test_system.sh
```

## 🎯 Access Points

- **💬 Chat**: http://localhost:8001
- **🔧 Admin**: http://localhost:9000/admin
- **🩺 Appointments**: http://localhost:9000/appointments

## 🧪 Quick Test

1. Open http://localhost:8001
2. Type: "What is endometriosis?"
3. Get AI response
4. Try: "I have severe pelvic pain" (should show appointment button)

## 🆘 Problems?

```bash
# Check system status
./test_system.sh

# View logs
tail -f backend/logs.txt
tail -f chainlit_app/logs.txt
```

**Need help?** Check the full [README.md](README.md) or open an issue!
