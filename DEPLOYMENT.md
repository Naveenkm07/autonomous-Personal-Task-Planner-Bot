# Autonomous Personal Task Planner Bot
## Production Deployment Guide

### System Overview
This autonomous task planner bot uses a multi-agent architecture with 4 specialized AI agents:

- **WF4 Reviewer & Learner Agent**: Analyzes patterns and learns from user behavior
- **WF1 Collector Agent**: Monitors and collects data from various sources (every 15 min)
- **WF2 Planner Agent**: Intelligent planning and conflict resolution (the brain)
- **WF3 Executor Agent**: Executes approved plans and manages notifications

### Prerequisites
- Docker & Docker Compose
- API Keys for: Google (Gemini, Calendar), Notion, OpenWeatherMap, Telegram
- Linux/macOS environment (for cron jobs)
- 2GB+ RAM recommended
- 5GB+ disk space

### Quick Start

1. **Clone and Setup**
```bash
git clone <repository>
cd autonomous-task-planner
cp .env.example .env
# Edit .env with your API keys
```

2. **Configure API Keys**
```bash
# Edit .env file with your credentials
GEMINI_API_KEY=your_key_here
GOOGLE_CALENDAR_CREDENTIALS=./credentials.json
NOTION_API_TOKEN=secret_token
OPENWEATHER_API_KEY=api_key
TELEGRAM_BOT_TOKEN=bot_token
```

3. **Deploy with Docker**
```bash
# Build and start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f task-planner
```

4. **Verify Deployment**
```bash
# Health check
curl http://localhost:8000/health

# Test collector agent
docker-compose exec task-planner python autonomous_task_planner.py --agent collector

# Run full workflow
docker-compose exec task-planner python autonomous_task_planner.py --workflow
```

### Production Configuration

#### Environment Variables
```bash
# Production settings
ENVIRONMENT=production
LOG_LEVEL=INFO
MAX_RETRIES=3
TIMEOUT=30

# Agent schedules (cron format)
COLLECTOR_SCHEDULE="*/15 * * * *"  # Every 15 minutes
REVIEWER_SCHEDULE="0 22 * * *"    # Daily at 10 PM
```

#### Security Configuration
- Use Docker secrets for sensitive data
- Enable firewall rules for exposed ports
- Use HTTPS with reverse proxy (nginx/traefik)
- Rotate API keys regularly

#### Monitoring Setup
```bash
# Access monitoring dashboards
Grafana: http://localhost:3000 (admin/password)
Prometheus: http://localhost:9090
```

### API Integration Setup

#### 1. Google Calendar API
```bash
# 1. Go to Google Cloud Console
# 2. Enable Calendar API
# 3. Create service account
# 4. Download credentials.json
# 5. Place in project root
```

#### 2. Notion API
```bash
# 1. Go to notion.so/my-integrations
# 2. Create new integration
# 3. Copy internal integration token
# 4. Share your database with integration
```

#### 3. OpenWeatherMap API
```bash
# 1. Sign up at openweathermap.org
# 2. Get free API key
# 3. Add to .env file
```

#### 4. Telegram Bot
```bash
# 1. Message @BotFather on Telegram
# 2. Create new bot with /newbot
# 3. Copy bot token
# 4. Get your chat ID from bot
```

### Scaling and Performance

#### Horizontal Scaling
```yaml
# docker-compose.yml
services:
  collector-agent:
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
```

#### Performance Optimization
- Enable Redis caching for API responses
- Use connection pooling for database
- Implement circuit breakers for external APIs
- Add load balancing for multiple instances

### Troubleshooting

#### Common Issues
1. **API Rate Limits**
   - Check rate limiting configuration
   - Implement exponential backoff
   - Use multiple API keys if needed

2. **Cron Jobs Not Running**
   ```bash
   # Check cron service
   docker-compose exec task-planner service cron status

   # View cron logs
   docker-compose exec task-planner tail -f /var/log/cron.log
   ```

3. **Memory Issues**
   ```bash
   # Monitor resource usage
   docker stats

   # Increase memory limits in docker-compose.yml
   deploy:
     resources:
       limits:
         memory: 1G
   ```

#### Logging and Debugging
```bash
# View agent-specific logs
docker-compose logs collector-agent
docker-compose logs reviewer-agent

# Debug mode
ENVIRONMENT=development LOG_LEVEL=DEBUG docker-compose up

# Check system health
curl http://localhost:8000/health
```

### Backup and Recovery

#### Data Backup
```bash
# Backup database
docker-compose exec postgres pg_dump -U planner_user task_planner > backup.sql

# Backup configuration
tar -czf config-backup.tar.gz .env config.json
```

#### Disaster Recovery
```bash
# Restore from backup
docker-compose exec postgres psql -U planner_user task_planner < backup.sql

# Restart services
docker-compose restart
```

### Maintenance

#### Regular Tasks
- Update dependencies monthly
- Rotate API keys quarterly
- Review logs weekly
- Monitor resource usage daily

#### Updates
```bash
# Update system
git pull
docker-compose build --no-cache
docker-compose up -d
```

### Support
- Check logs first: `docker-compose logs`
- Monitor system health: `curl localhost:8000/health`
- Review API quotas and limits
- Check network connectivity

## Architecture Diagram
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Collector     │    │    Planner      │    │   Executor      │
│   Agent (WF1)   │───▶│  Agent (WF2)    │───▶│  Agent (WF3)    │
│  Every 15 min   │    │   The Brain     │    │   Notifications │
└─────────────────┘    └─────────────────┘    └─────────────────┘
        │                       │                       │
        ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Data Sources  │    │  Conflict Det.  │    │  Google Cal     │
│ • Calendar      │    │ • Weather       │    │ • Notion DB     │
│ • Notion        │    │ • Priorities    │    │ • Telegram      │
│ • Weather       │    │ • AI Planning   │    │ • Reminders     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   Reviewer      │
                       │  Agent (WF4)    │
                       │  Daily 10 PM    │
                       │ Learning & Rules│
                       └─────────────────┘
```

This system provides autonomous task planning with continuous learning and optimization capabilities.
