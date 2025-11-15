#!/bin/bash
# Test script for Cerebrum Web backend

echo "🧪 Testing Cerebrum Web Backend..."
echo ""

# Test 1: Check if Python dependencies can be imported
echo "Test 1: Checking Python imports..."
cd backend
python3 -c "
import sys
from pathlib import Path

# Add project root to path (cerebrum-web/backend -> Obsidian-atomizer)
sys.path.insert(0, str(Path.cwd().parent.parent))

try:
    from app.main import app
    print('✅ FastAPI app imported successfully')
except Exception as e:
    print(f'❌ Failed to import FastAPI app: {e}')
    sys.exit(1)

try:
    from cerebrum.core.orchestrator import Orchestrator
    print('✅ Cerebrum orchestrator imported successfully')
except Exception as e:
    print(f'❌ Failed to import Cerebrum: {e}')
    sys.exit(1)
"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ All imports successful!"
    echo ""
    echo "📝 Next steps:"
    echo "  1. Install backend dependencies: pip install -r requirements.txt"
    echo "  2. Start backend: python -m app.main"
    echo "  3. Install frontend dependencies: cd ../frontend && npm install"
    echo "  4. Start frontend: npm run dev"
    echo "  5. Open: http://localhost:5173"
else
    echo ""
    echo "❌ Import tests failed. Please check dependencies."
    exit 1
fi
