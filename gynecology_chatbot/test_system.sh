#!/bin/bash

echo "🧪 GYNECOLOGY CHATBOT - SYSTEM TEST"
echo "=================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counters
TESTS_PASSED=0
TESTS_FAILED=0

test_result() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ PASS${NC}: $2"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}❌ FAIL${NC}: $2"
        ((TESTS_FAILED++))
    fi
}

echo -e "${BLUE}📋 Testing Backend Django API...${NC}"
echo "================================="

# Test 1: Backend virtual environment
cd backend
if [ -d "venv" ]; then
    source venv/bin/activate
    test_result 0 "Backend virtual environment found"
else
    test_result 1 "Backend virtual environment not found"
fi

# Test 2: Django settings
python3 manage.py check > /dev/null 2>&1
test_result $? "Django configuration check"

# Test 3: Database migrations
python3 manage.py showmigrations --list | grep -q "\[X\]"
test_result $? "Database migrations applied"

# Test 4: Start backend server
echo -e "${YELLOW}🚀 Starting Django backend server...${NC}"
python3 manage.py runserver 9000 > /dev/null 2>&1 &
BACKEND_PID=$!
sleep 3

# Test 5: Backend health check
curl -s http://localhost:9000/api/health/ | grep -q "ok"
test_result $? "Backend health endpoint responding"

# Test 6: Admin interface
curl -s http://localhost:9000/admin/ | grep -q "Django"
test_result $? "Django admin interface accessible"

# Test 7: API endpoints
curl -s http://localhost:9000/api/users/ | grep -q "authentication"
test_result $? "API authentication working"

# Test 8: Appointments page
curl -s http://localhost:9000/appointments/ | grep -q "WomanCare"
test_result $? "Appointments page accessible"

echo ""
echo -e "${BLUE}🤖 Testing LLM Integrations...${NC}"
echo "============================="

# Test 9: OpenAI integration
python3 -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gynecology_chatbot_project.settings')
import django
django.setup()
from apps.chatbot.api import get_openai_response_sync
response = get_openai_response_sync('test')
exit(0 if 'Error' not in response else 1)
" > /dev/null 2>&1
test_result $? "OpenAI integration"

# Test 10: Gemini integration  
python3 -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gynecology_chatbot_project.settings')
import django
django.setup()
from apps.chatbot.api import get_gemini_response_sync
response = get_gemini_response_sync('test')
exit(0 if 'Error' not in response else 1)
" > /dev/null 2>&1
test_result $? "Gemini integration"

# Test 11: Grok integration
python3 -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gynecology_chatbot_project.settings')
import django
django.setup()
from apps.chatbot.api import get_grok_response_sync
response = get_grok_response_sync('test')
exit(0 if response else 1)
" > /dev/null 2>&1
test_result $? "Grok integration"

echo ""
echo -e "${BLUE}💬 Testing Chainlit Frontend...${NC}"
echo "==============================="

# Stop backend for now
kill $BACKEND_PID > /dev/null 2>&1

# Test 12: Chainlit environment
cd ../chainlit_app
if [ -f ".env" ]; then
    test_result 0 "Chainlit environment file found"
else
    test_result 1 "Chainlit environment file missing"
fi

# Test 13: Chainlit dependencies
python3 -c "import chainlit; import aiohttp; import google.generativeai" > /dev/null 2>&1
test_result $? "Chainlit dependencies installed"

# Test 14: Start Chainlit server
echo -e "${YELLOW}🚀 Starting Chainlit frontend server...${NC}"
timeout 10 chainlit run app.py --port 8001 --headless > /dev/null 2>&1 &
CHAINLIT_PID=$!
sleep 3

# Test 15: Chainlit health
curl -s http://localhost:8001 | grep -q "Chainlit" > /dev/null 2>&1
test_result $? "Chainlit frontend accessible"

kill $CHAINLIT_PID > /dev/null 2>&1

echo ""
echo -e "${BLUE}🔄 Testing Full Integration...${NC}"
echo "============================="

# Restart backend for integration test
cd ../backend
source venv/bin/activate
python3 manage.py runserver 9000 > /dev/null 2>&1 &
BACKEND_PID=$!
sleep 3

# Start chainlit
cd ../chainlit_app
chainlit run app.py --port 8001 --headless > /dev/null 2>&1 &
CHAINLIT_PID=$!
sleep 3

# Test 16: Integration test
curl -s http://localhost:8001 > /dev/null 2>&1 && curl -s http://localhost:9000/api/health/ > /dev/null 2>&1
test_result $? "Both services running simultaneously"

# Cleanup
kill $BACKEND_PID $CHAINLIT_PID > /dev/null 2>&1

echo ""
echo "🏁 TEST SUMMARY"
echo "==============="
echo -e "${GREEN}✅ Tests Passed: $TESTS_PASSED${NC}"
echo -e "${RED}❌ Tests Failed: $TESTS_FAILED${NC}"

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 ALL TESTS PASSED! Your application is working perfectly!${NC}"
    echo ""
    echo "🚀 To start your application:"
    echo "   Backend:  cd backend && source venv/bin/activate && python3 manage.py runserver 9000"
    echo "   Frontend: cd chainlit_app && chainlit run app.py --port 8001"
    echo ""
    echo "🌐 Access your application:"
    echo "   Chat Interface: http://localhost:8001"
    echo "   Admin Panel:    http://localhost:9000/admin"
    echo "   Book Doctors:   http://localhost:9000/appointments"
    echo "   API Health:     http://localhost:9000/api/health"
else
    echo -e "${RED}⚠️  Some tests failed. Check the output above for details.${NC}"
fi

echo ""
