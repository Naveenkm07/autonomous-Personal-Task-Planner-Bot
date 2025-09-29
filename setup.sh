#!/bin/bash

# Autonomous Task Planner Bot - Setup Script
# This script automates the initial setup process

set -e

echo "🤖 Autonomous Task Planner Bot Setup"
echo "===================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose found"

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data logs cache monitoring

# Copy environment template
if [ ! -f .env ]; then
    cp .env.example .env
    echo "📝 Created .env file from template"
    echo "⚠️  Please edit .env file with your API keys before proceeding"
else
    echo "✅ .env file already exists"
fi

# Create monitoring configuration
echo "📊 Setting up monitoring..."
mkdir -p monitoring
cat > monitoring/prometheus.yml << EOF
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'task-planner'
    static_configs:
      - targets: ['task-planner:8000']

  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres:5432']

  - job_name: 'redis'
    static_configs:
      - targets: ['redis:6379']
EOF

# Create database initialization script
echo "🗄️ Setting up database..."
cat > init.sql << EOF
-- Create tables for autonomous task planner
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    priority INTEGER DEFAULT 1,
    deadline TIMESTAMP,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB
);

CREATE TABLE IF NOT EXISTS learned_rules (
    id SERIAL PRIMARY KEY,
    rule_type VARCHAR(100) NOT NULL,
    rule_data JSONB NOT NULL,
    confidence FLOAT DEFAULT 0.5,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_used TIMESTAMP
);

CREATE TABLE IF NOT EXISTS agent_performance (
    id SERIAL PRIMARY KEY,
    agent_name VARCHAR(50) NOT NULL,
    operation VARCHAR(100) NOT NULL,
    duration FLOAT NOT NULL,
    success BOOLEAN DEFAULT TRUE,
    error_message TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_deadline ON tasks(deadline);
CREATE INDEX idx_rules_type ON learned_rules(rule_type);
CREATE INDEX idx_performance_agent ON agent_performance(agent_name);
EOF

echo "🔧 Setup completed!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API keys"
echo "2. Run: docker-compose up -d"
echo "3. Check status: docker-compose ps"
echo "4. View logs: docker-compose logs -f"
echo ""
echo "API Keys needed:"
echo "- GEMINI_API_KEY (Google AI)"
echo "- GOOGLE_CALENDAR_CREDENTIALS (Google Calendar)"
echo "- NOTION_API_TOKEN (Notion)"
echo "- OPENWEATHER_API_KEY (Weather)"
echo "- TELEGRAM_BOT_TOKEN (Telegram Bot)"
echo ""
echo "Happy planning! 🚀"
