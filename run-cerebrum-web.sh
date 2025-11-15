#!/bin/bash
# Cerebrum Web - Complete Setup & Run Script
# Run this on YOUR LOCAL MACHINE to see the preview!

set -e

echo "🧠 Cerebrum Web - Complete Setup"
echo "=================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -d "cerebrum-web" ]; then
    echo "❌ Error: cerebrum-web directory not found"
    echo "Please run this script from the Obsidian-atomizer root directory"
    exit 1
fi

echo "${BLUE}📦 Step 1: Installing Backend Dependencies...${NC}"
cd cerebrum-web/backend
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi
source venv/bin/activate
pip install -q -r requirements.txt

# Install Cerebrum core dependencies
echo "Installing Cerebrum core dependencies..."
pip install -q python-frontmatter pypdf chromadb google-generativeai

echo "${GREEN}✅ Backend dependencies installed${NC}"
echo ""

cd ../..

echo "${BLUE}📦 Step 2: Installing Frontend Dependencies...${NC}"
cd cerebrum-web/frontend
if [ ! -d "node_modules" ]; then
    npm install
else
    echo "node_modules already exists, skipping npm install"
fi
echo "${GREEN}✅ Frontend dependencies installed${NC}"
echo ""

cd ../..

echo "${BLUE}🚀 Step 3: Starting Servers...${NC}"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "${YELLOW}🛑 Shutting down servers...${NC}"
    kill $BACKEND_PID 2>/dev/null || true
    kill $FRONTEND_PID 2>/dev/null || true
    exit 0
}

trap cleanup EXIT INT TERM

# Start backend
echo "Starting backend on http://localhost:8000..."
cd cerebrum-web/backend
source venv/bin/activate
python -m app.main > /tmp/cerebrum-backend.log 2>&1 &
BACKEND_PID=$!
cd ../..

sleep 3

# Check if backend started
if ps -p $BACKEND_PID > /dev/null; then
    echo "${GREEN}✅ Backend running (PID: $BACKEND_PID)${NC}"
else
    echo "${YELLOW}❌ Backend failed to start. Check /tmp/cerebrum-backend.log${NC}"
    cat /tmp/cerebrum-backend.log
    exit 1
fi

# Start frontend
echo "Starting frontend on http://localhost:5173..."
cd cerebrum-web/frontend
npm run dev > /tmp/cerebrum-frontend.log 2>&1 &
FRONTEND_PID=$!
cd ../..

sleep 3

# Check if frontend started
if ps -p $FRONTEND_PID > /dev/null; then
    echo "${GREEN}✅ Frontend running (PID: $FRONTEND_PID)${NC}"
else
    echo "${YELLOW}❌ Frontend failed to start. Check /tmp/cerebrum-frontend.log${NC}"
    cat /tmp/cerebrum-frontend.log
    exit 1
fi

echo ""
echo "=================================="
echo "${GREEN}🎉 Cerebrum Web is RUNNING!${NC}"
echo "=================================="
echo ""
echo "📱 Open in your browser:"
echo "   ${BLUE}http://localhost:5173${NC}"
echo ""
echo "📊 Backend API docs:"
echo "   ${BLUE}http://localhost:8000/api/docs${NC}"
echo ""
echo "📝 Logs:"
echo "   Backend:  /tmp/cerebrum-backend.log"
echo "   Frontend: /tmp/cerebrum-frontend.log"
echo ""
echo "${YELLOW}Press Ctrl+C to stop servers${NC}"
echo ""

# Wait for user to stop
wait
