#!/bin/bash

echo "🔧 Setting up Gynecology Chatbot Development Environment"
echo "======================================================="

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check if we're in the right directory
if [ ! -f "run_servers.sh" ]; then
    echo -e "${RED}❌ Please run this script from the gynecology_chatbot directory${NC}"
    exit 1
fi

echo -e "${YELLOW}📦 Installing system dependencies...${NC}"

# Update system packages
sudo apt update

# Install required system packages
sudo apt install -y python3 python3-pip python3-venv git curl

echo -e "${YELLOW}🏗️ Setting up backend environment...${NC}"

# Setup backend
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate virtual environment and install dependencies
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${YELLOW}⚠️ Please edit backend/.env with your API keys${NC}"
fi

# Run migrations
python3 manage.py migrate

# Create guest user
python3 create_guest_user.py

deactivate
cd ..

echo -e "${YELLOW}🎨 Setting up frontend environment...${NC}"

# Setup frontend
cd chainlit_app

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate virtual environment and install dependencies
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${YELLOW}⚠️ Please edit chainlit_app/.env with your configuration${NC}"
fi

deactivate
cd ..

# Make scripts executable
chmod +x run_servers.sh
chmod +x test_system.sh

echo -e "${GREEN}✅ Development environment setup complete!${NC}"
echo ""
echo "📝 Next steps:"
echo "1. Edit backend/.env with your API keys"
echo "2. Edit chainlit_app/.env with your configuration"
echo "3. Run './run_servers.sh' to start the application"
echo "4. Run './test_system.sh' to verify everything works"
echo ""
echo "🌐 Once running, access:"
echo "   - Chat Interface: http://localhost:8001"
echo "   - Admin Panel: http://localhost:9000/admin"
echo "   - Appointments: http://localhost:9000/appointments"
