#!/bin/bash
# Quick Launch Script for Samsung S25 Ultra Coding Agent App
# ===========================================================

echo "🚀 Launching Coding Agent App..."

# Check if we're in the right directory
if [ ! -f "server/index.js" ]; then
    echo "❌ Error: Not in the s25-ultra-agent-app directory"
    echo "📂 Please run: cd ~/aic_projects/s25-ultra-agent-app"
    exit 1
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your OPENAI_API_KEY"
    echo "   nano .env"
    exit 1
fi

# Check if API key is set
if grep -q "your-api-key-here" .env; then
    echo "⚠️  API key not configured!"
    echo "📝 Please edit .env and add your OPENAI_API_KEY"
    echo "   nano .env"
    echo ""
    echo "Get your API key from: https://platform.openai.com/api-keys"
    exit 1
fi

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

echo ""
echo "✅ All checks passed!"
echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║  Choose launch method:                               ║"
echo "╠══════════════════════════════════════════════════════╣"
echo "║  1) npm start       - Simple start                   ║"
echo "║  2) npm run dev     - Development mode (auto-reload) ║"
echo "║  3) PM2 start       - Background process             ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""
read -p "Enter choice (1-3): " choice

case $choice in
    1)
        echo "🚀 Starting server with npm..."
        npm start
        ;;
    2)
        echo "🔧 Starting development server..."
        npm run dev
        ;;
    3)
        echo "🔄 Starting with PM2..."
        if ! command -v pm2 &> /dev/null; then
            echo "📦 Installing PM2..."
            npm install -g pm2
        fi
        npm run pm2:start
        echo ""
        echo "✅ Server running in background!"
        echo "📊 View logs: npm run pm2:logs"
        echo "🛑 Stop server: npm run pm2:stop"
        ;;
    *)
        echo "❌ Invalid choice. Defaulting to npm start..."
        npm start
        ;;
esac
