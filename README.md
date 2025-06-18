# Gynecology Chatbot 🩺💬

A comprehensive medical chatbot application designed to provide gynecological health information and support. The system features a Django REST API backend with multiple LLM integrations and a modern Chainlit chat interface.

## 🌟 Features

- **Multi-LLM Integration**: Supports OpenAI GPT, Google Gemini, and Grok models
- **Intelligent Response Selection**: Automatically evaluates and selects the best response from multiple AI models
- **Appointment Booking**: Integrated appointment scheduling system with 30+ fictional gynecologists
- **User Management**: Complete authentication and user preference system
- **Chat History**: Persistent conversation management
- **Severity Assessment**: Automatic assessment of health concerns to show appointment booking options
- **Modern UI**: Clean, responsive interface built with Chainlit and React
- **RESTful API**: Complete Django REST Framework API for all operations

## 🏗️ Architecture

```
gynecology_chatbot/
├── backend/                 # Django REST API
│   ├── apps/
│   │   ├── users/          # User management
│   │   └── chatbot/        # Chat functionality
│   ├── appointments/       # Appointment booking system
│   └── utils/             # Utilities and LLM integrations
├── chainlit_app/          # Chainlit chat interface
└── documentation/         # Additional docs
```

## 🔧 Prerequisites

### System Requirements
- **Operating System**: Ubuntu 22.04 (tested) or compatible Linux distribution
- **Python**: Python 3.8+ (tested with Python 3.10)
- **Memory**: Minimum 4GB RAM recommended
- **Storage**: 2GB free disk space

### Required Software
```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install Python 3 and pip
sudo apt install python3 python3-pip python3-venv -y

# Install Git (if not already installed)
sudo apt install git -y

# Install curl for testing
sudo apt install curl -y
```

### API Keys Required
- **OpenAI API Key**: Get from [OpenAI Platform](https://platform.openai.com/api-keys)
- **Google Gemini API Key**: Get from [Google AI Studio](https://makersuite.google.com/app/apikey)
- **Grok API Key**: Currently simulated (optional)

## 📥 Installation

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd gynecology_chatbot
```

### 2. Backend Setup

#### Create Virtual Environment
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

#### Install Dependencies
```bash
pip install -r requirements.txt
```

#### Configure Environment Variables
```bash
# Copy environment template
cp .env.example .env

# Edit the .env file with your API keys
nano .env
```

**Add your API keys to `.env`:**
```env
DJANGO_SECRET_KEY="your-secret-key-here"
DEBUG=True
OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
GROK_API_KEY=your_grok_api_key_here  # Optional
```

#### Database Setup
```bash
# Run migrations
python3 manage.py migrate

# Create superuser (optional)
python3 manage.py createsuperuser

# Create guest user for testing
python3 create_guest_user.py
```

#### Test Backend
```bash
# Start Django server
python3 manage.py runserver 9000

# In another terminal, test the API
curl http://localhost:9000/api/health/
```

### 3. Frontend Setup

#### Navigate to Chainlit App
```bash
# From the gynecology_chatbot directory
cd chainlit_app
```

#### Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Install Dependencies
```bash
pip install -r requirements.txt
```

#### Configure Environment Variables
```bash
# Copy environment template
cp .env.example .env

# Edit the .env file
nano .env
```

**Add configuration to `.env`:**
```env
DJANGO_API_URL=http://localhost:9000/api
DJANGO_API_TOKEN=your_jwt_token_from_guest_user_creation
GEMINI_API_KEY=your_gemini_api_key_here
```

## 🚀 Running the Application

### Method 1: Using the Automated Script (Recommended)
```bash
# From the gynecology_chatbot directory
chmod +x run_servers.sh
./run_servers.sh
```

This script will:
- Start the Django backend on port 9000
- Start the Chainlit frontend on port 8001
- Handle graceful shutdown with Ctrl+C

### Method 2: Manual Startup

#### Terminal 1 - Backend
```bash
cd backend
source venv/bin/activate
python3 manage.py runserver 9000
```

#### Terminal 2 - Frontend
```bash
cd chainlit_app
source venv/bin/activate
chainlit run app.py --port 8001
```

### 🌐 Access Your Application

Once both servers are running:

- **💬 Chat Interface**: http://localhost:8001
- **🔧 Admin Panel**: http://localhost:9000/admin
- **🩺 Book Appointments**: http://localhost:9000/appointments
- **📊 API Health**: http://localhost:9000/api/health

## 🧪 Testing the System

### Automated System Test
```bash
# From the gynecology_chatbot directory
chmod +x test_system.sh
./test_system.sh
```

This comprehensive test will verify:
- Backend configuration and health
- Database migrations
- API endpoints
- LLM integrations
- Frontend functionality
- Full integration testing

### Manual Testing

#### Test Backend API
```bash
# Health check
curl http://localhost:9000/api/health/

# Test authentication
curl http://localhost:9000/api/users/

# Test appointments page
curl http://localhost:9000/appointments/
```

#### Test Chat Interface
1. Open http://localhost:8001
2. Send a test message like "What is endometriosis?"
3. Verify you receive a response
4. Check if appointment booking button appears for concerning symptoms

## 🎯 Usage Guide

### For End Users

#### Starting a Chat Session
1. Navigate to http://localhost:8001
2. Type your gynecological health question
3. Receive AI-powered responses from multiple models
4. If the system detects concerning symptoms, you'll see a "Book Appointment" button

#### Booking Appointments
1. Click the "Book Appointment" button in chat, or
2. Navigate directly to http://localhost:9000/appointments
3. Browse 30+ available gynecologists
4. Filter by specialty, rating, experience, or price
5. Select date and time
6. Confirm your appointment

### For Developers

#### API Endpoints

**Authentication**
- `POST /api/token/` - Obtain JWT token
- `POST /api/token/refresh/` - Refresh JWT token

**Users**
- `GET /api/users/me/` - Get current user profile
- `PUT /api/users/update_settings/` - Update user settings

**Chatbot**
- `GET /api/chatbot/conversations/` - List conversations
- `POST /api/chatbot/conversations/` - Create conversation
- `POST /api/chatbot/conversations/{id}/send_message/` - Send message
- `DELETE /api/chatbot/conversations/{id}/clear/` - Clear conversation

## ⚙️ Configuration

### Environment Variables

#### Backend (.env)
```env
# Django Core
DJANGO_SECRET_KEY="your-secret-key"
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# API Keys
OPENAI_API_KEY=your_openai_key
GEMINI_API_KEY=your_gemini_key
GROK_API_KEY=your_grok_key

# Model Configuration
OPENAI_MODEL=gpt-4o
GEMINI_MODEL=gemini-1.5-flash
GROK_MODEL=grok-2
```

#### Frontend (.env)
```env
DJANGO_API_URL=http://localhost:9000/api
DJANGO_API_TOKEN=your_jwt_token
GEMINI_API_KEY=your_gemini_key
```

### Customization

#### System Prompt
Modify the system prompt in `backend/gynecology_chatbot_project/settings.py`:
```python
GYNECOLOGY_SYSTEM_PROMPT = """
Your custom system prompt here...
"""
```

#### UI Configuration
Edit `chainlit_app/.chainlit/config.toml` for UI customization:
- Assistant name
- Theme settings
- Feature toggles

## 🐛 Troubleshooting

### Common Issues

#### Backend Won't Start
```bash
# Check if virtual environment is activated
source backend/venv/bin/activate

# Verify dependencies
pip install -r backend/requirements.txt

# Check migrations
python3 manage.py migrate

# Verify environment variables
cat backend/.env
```

#### Frontend Connection Issues
```bash
# Verify backend is running
curl http://localhost:9000/api/health/

# Check frontend environment
cat chainlit_app/.env

# Verify JWT token is valid
python3 backend/create_guest_user.py
```

#### LLM API Errors
- **OpenAI**: Verify API key and billing status
- **Gemini**: Check API key and quota limits
- **Rate Limits**: Implement exponential backoff

#### Port Conflicts
```bash
# Check if ports are in use
netstat -tulpn | grep :9000
netstat -tulpn | grep :8001

# Kill processes if needed
sudo kill -9 $(lsof -t -i:9000)
sudo kill -9 $(lsof -t -i:8001)
```

### Logs and Debugging

#### Django Logs
```bash
# Enable debug mode in backend/.env
DEBUG=True

# Check Django logs in terminal output
```

#### Chainlit Logs
```bash
# Check Chainlit logs in terminal output
# Enable verbose logging in chainlit config
```

## 🔒 Security Considerations

### Production Deployment
1. **Set DEBUG=False** in production
2. **Use strong SECRET_KEY**
3. **Configure ALLOWED_HOSTS** properly
4. **Use HTTPS** in production
5. **Secure API keys** using environment variables
6. **Enable CSRF protection**
7. **Use database like PostgreSQL** instead of SQLite

### API Key Security
- Never commit API keys to version control
- Use environment variables or secret management
- Rotate keys regularly
- Monitor usage and costs

## 📚 Additional Resources

### LLM Integration
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Google Gemini Documentation](https://ai.google.dev/docs)
- [Django REST Framework](https://www.django-rest-framework.org/)

### Frontend Framework
- [Chainlit Documentation](https://docs.chainlit.io/)
- [React Documentation](https://react.dev/)

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly using `./test_system.sh`
5. Submit a pull request

### Code Standards
- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings to functions
- Write tests for new features

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter issues:

1. **Check the troubleshooting section** above
2. **Run the system test**: `./test_system.sh`
3. **Check logs** in both terminal windows
4. **Verify API keys** are correctly configured
5. **Open an issue** on the repository with:
   - Operating system and Python version
   - Error messages
   - Steps to reproduce

## 🔄 Updates and Maintenance

### Keeping Dependencies Updated
```bash
# Backend
cd backend
source venv/bin/activate
pip list --outdated
pip install --upgrade package_name

# Frontend
cd chainlit_app
source venv/bin/activate
pip list --outdated
pip install --upgrade package_name
```

### Database Migrations
```bash
# When making model changes
cd backend
source venv/bin/activate
python3 manage.py makemigrations
python3 manage.py migrate
```

---

**Made with ❤️ for women's health**

*This application is for informational purposes only and should not replace professional medical advice.*
