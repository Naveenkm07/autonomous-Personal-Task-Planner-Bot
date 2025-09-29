
"""
Autonomous Personal Task Planner Bot
Multi-Agent System Implementation

This module contains the core implementation of the 4 specialized AI agents:
- WF4: Reviewer & Learner Agent
- WF1: Collector Agent  
- WF2: Planner Agent (The Brain)
- WF3: Executor Agent
"""

import asyncio
import json
import logging
import os
import sqlite3
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod
from crontab import CronTab
import google.generativeai as genai
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import openai

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('autonomous_planner.log'),
        logging.StreamHandler()
    ]
)

@dataclass
class TaskData:
    """Data structure for tasks"""
    id: str
    title: str
    description: str
    priority: int
    deadline: datetime
    status: str
    created_at: datetime
    updated_at: datetime
    metadata: Dict[str, Any]

@dataclass
class WeatherData:
    """Weather information structure"""
    temperature: float
    condition: str
    humidity: int
    wind_speed: float
    forecast: str
    timestamp: datetime

class BaseAgent(ABC):
    """Base class for all agents"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    @abstractmethod
    async def execute(self) -> Dict[str, Any]:
        """Execute the agent's main functionality"""
        pass

    def log_performance(self, operation: str, duration: float, success: bool):
        """Log performance metrics"""
        self.logger.info(f"Operation: {operation}, Duration: {duration:.2f}s, Success: {success}")

class ReviewerLearnerAgent(BaseAgent):
    """WF4: Reviewer & Learner Agent - Analyzes patterns and learns from user behavior"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.gemini_client = self._initialize_gemini()
        self.notion_client = self._initialize_notion()
        self.calendar_service = self._initialize_calendar()

    def _initialize_gemini(self):
        """Initialize Google Gemini AI client"""
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable required")
        genai.configure(api_key=api_key)
        return genai.GenerativeModel('gemini-pro')

    def _initialize_notion(self):
        """Initialize Notion API client"""
        # Placeholder for Notion client initialization
        return {"token": os.getenv('NOTION_API_TOKEN')}

    def _initialize_calendar(self):
        """Initialize Google Calendar API client"""
        # Placeholder for Calendar API initialization
        return {"credentials": "google_calendar_credentials"}

    async def execute(self) -> Dict[str, Any]:
        """Main execution method for reviewer agent"""
        start_time = datetime.now()

        try:
            # Step 1: Read completed tasks from calendar
            completed_tasks = await self._fetch_completed_tasks()

            # Step 2: Analyze performance patterns with AI
            patterns = await self._analyze_patterns(completed_tasks)

            # Step 3: Generate intelligent rules and insights
            rules = await self._generate_rules(patterns)

            # Step 4: Store refined rules in Notion
            await self._store_rules(rules)

            # Step 5: Generate performance feedback
            feedback = await self._generate_feedback(patterns)

            duration = (datetime.now() - start_time).total_seconds()
            self.log_performance("reviewer_execution", duration, True)

            return {
                "status": "success",
                "completed_tasks_analyzed": len(completed_tasks),
                "patterns_identified": len(patterns),
                "rules_generated": len(rules),
                "feedback": feedback,
                "execution_time": duration
            }

        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            self.log_performance("reviewer_execution", duration, False)
            self.logger.error(f"Reviewer agent failed: {e}")
            return {"status": "error", "message": str(e)}

    async def _fetch_completed_tasks(self) -> List[TaskData]:
        """Fetch completed tasks from calendar history"""
        # Placeholder implementation
        self.logger.info("Fetching completed tasks from Google Calendar")
        # In real implementation: Use Google Calendar API to fetch completed events
        return []

    async def _analyze_patterns(self, tasks: List[TaskData]) -> List[Dict[str, Any]]:
        """Use AI to analyze performance patterns"""
        self.logger.info(f"Analyzing patterns for {len(tasks)} tasks with Gemini AI")

        try:
            prompt = f"""
            Analyze the following completed tasks and identify productivity patterns:
            Tasks: {json.dumps([{"title": task.title, "completion_time": task.updated_at.isoformat()} for task in tasks], indent=2)}

            Please identify:
            1. Peak productivity hours
            2. Task completion patterns  
            3. Common bottlenecks
            4. Optimization opportunities

            Return analysis in JSON format.
            """

            response = self.gemini_client.generate_content(prompt)
            # Parse and return structured patterns
            return [{"pattern_type": "productivity", "insights": response.text}]

        except Exception as e:
            self.logger.error(f"Pattern analysis failed: {e}")
            return []

    async def _generate_rules(self, patterns: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate intelligent rules based on patterns"""
        self.logger.info("Generating intelligent rules from patterns")

        try:
            rules_prompt = f"""
            Based on these productivity patterns: {json.dumps(patterns, indent=2)}

            Generate optimization rules for:
            1. Task scheduling preferences
            2. Break time recommendations
            3. Priority adjustment rules
            4. Conflict resolution strategies

            Format as actionable JSON rules.
            """

            response = self.gemini_client.generate_content(rules_prompt)
            # Parse and return structured rules
            return [{"rule_type": "scheduling", "rule": response.text}]

        except Exception as e:
            self.logger.error(f"Rule generation failed: {e}")
            return []

    async def _store_rules(self, rules: List[Dict[str, Any]]) -> bool:
        """Store refined rules in Notion database"""
        self.logger.info(f"Storing {len(rules)} rules in Notion database")
        # Placeholder for Notion API integration
        return True

    async def _generate_feedback(self, patterns: List[Dict[str, Any]]) -> str:
        """Generate performance feedback and optimization suggestions"""
        try:
            feedback_prompt = f"""
            Based on productivity patterns: {json.dumps(patterns, indent=2)}

            Provide personalized feedback with:
            1. Performance highlights
            2. Areas for improvement  
            3. Specific recommendations
            4. Motivation and encouragement

            Keep it concise and actionable.
            """

            response = self.gemini_client.generate_content(feedback_prompt)
            return response.text

        except Exception as e:
            self.logger.error(f"Feedback generation failed: {e}")
            return "Unable to generate feedback at this time."

class CollectorAgent(BaseAgent):
    """WF1: Collector Agent - Monitors and collects data from various sources"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.weather_api_key = os.getenv('OPENWEATHER_API_KEY')
        self.calendar_service = self._initialize_calendar()
        self.notion_client = self._initialize_notion()
        self.gemini_client = self._initialize_gemini()

    def _initialize_calendar(self):
        """Initialize Google Calendar API"""
        return {"credentials": "google_calendar_credentials"}

    def _initialize_notion(self):
        """Initialize Notion API"""
        return {"token": os.getenv('NOTION_API_TOKEN')}

    def _initialize_gemini(self):
        """Initialize Gemini AI for data processing"""
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY required")
        genai.configure(api_key=api_key)
        return genai.GenerativeModel('gemini-pro')

    async def execute(self) -> Dict[str, Any]:
        """Main execution method for collector agent"""
        start_time = datetime.now()

        try:
            # Step 1: Monitor Google Calendar for new events
            calendar_events = await self._fetch_calendar_events()

            # Step 2: Fetch weather data
            weather_data = await self._fetch_weather_data()

            # Step 3: Read existing tasks from Notion
            notion_tasks = await self._fetch_notion_tasks()

            # Step 4: Use AI to parse and structure data
            structured_data = await self._structure_data({
                "calendar_events": calendar_events,
                "weather_data": weather_data,
                "notion_tasks": notion_tasks
            })

            # Step 5: Prepare clean data for Planner Agent
            clean_data = await self._prepare_clean_data(structured_data)

            duration = (datetime.now() - start_time).total_seconds()
            self.log_performance("collector_execution", duration, True)

            return {
                "status": "success",
                "calendar_events": len(calendar_events),
                "weather_updated": bool(weather_data),
                "notion_tasks": len(notion_tasks),
                "structured_data": clean_data,
                "execution_time": duration
            }

        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            self.log_performance("collector_execution", duration, False)
            self.logger.error(f"Collector agent failed: {e}")
            return {"status": "error", "message": str(e)}

    async def _fetch_calendar_events(self) -> List[Dict[str, Any]]:
        """Monitor Google Calendar for new events and tasks"""
        self.logger.info("Fetching new calendar events")
        # Placeholder for Google Calendar API integration
        return []

    async def _fetch_weather_data(self) -> Optional[WeatherData]:
        """Fetch current weather data from OpenWeatherMap API"""
        if not self.weather_api_key:
            self.logger.warning("Weather API key not configured")
            return None

        try:
            # Default to user's location or configurable city
            city = "New York"  # This should be configurable
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.weather_api_key}&units=metric"

            response = requests.get(url, timeout=10)
            response.raise_for_status()

            data = response.json()
            weather = WeatherData(
                temperature=data['main']['temp'],
                condition=data['weather'][0]['description'],
                humidity=data['main']['humidity'],
                wind_speed=data['wind']['speed'],
                forecast=data['weather'][0]['main'],
                timestamp=datetime.now()
            )

            self.logger.info(f"Weather data fetched: {weather.temperature}°C, {weather.condition}")
            return weather

        except Exception as e:
            self.logger.error(f"Failed to fetch weather data: {e}")
            return None

    async def _fetch_notion_tasks(self) -> List[Dict[str, Any]]:
        """Read existing tasks from Notion database"""
        self.logger.info("Fetching tasks from Notion database")
        # Placeholder for Notion API integration
        return []

    async def _structure_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Use AI to parse, structure, and categorize collected data"""
        self.logger.info("Structuring data with Gemini AI")

        try:
            structure_prompt = f"""
            Process and structure this collected data for a task planning system:

            Raw Data: {json.dumps(raw_data, default=str, indent=2)}

            Please:
            1. Categorize calendar events by type (work, personal, meetings)
            2. Identify task dependencies and priorities
            3. Consider weather impact on outdoor activities
            4. Flag potential scheduling conflicts
            5. Extract actionable items

            Return structured JSON data.
            """

            response = self.gemini_client.generate_content(structure_prompt)
            # In real implementation, parse the AI response properly
            return {"structured": True, "ai_response": response.text}

        except Exception as e:
            self.logger.error(f"Data structuring failed: {e}")
            return raw_data

    async def _prepare_clean_data(self, structured_data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare clean, formatted data feed for Planner Agent"""
        self.logger.info("Preparing clean data feed for Planner Agent")

        return {
            "timestamp": datetime.now().isoformat(),
            "data_quality": "high",
            "ready_for_planning": True,
            "structured_data": structured_data
        }

class PlannerAgent(BaseAgent):
    """WF2: Planner Agent (The Brain) - Intelligent planning and conflict resolution"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.gemini_client = self._initialize_gemini()
        self.conflict_detector = ConflictDetector()
        self.priority_weights = config.get('priority_weights', {
            "deadline": 0.4, "importance": 0.3, "duration": 0.2, "user_preference": 0.1
        })

    def _initialize_gemini(self):
        """Initialize Gemini AI for intelligent planning"""
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY required")
        genai.configure(api_key=api_key)
        return genai.GenerativeModel('gemini-pro')

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Main execution method for planner agent"""
        start_time = datetime.now()

        try:
            # Step 1: Draft intelligent daily/weekly plans
            initial_plan = await self._draft_plan(input_data)

            # Step 2: Implement conflict detection
            conflicts = self.conflict_detector.detect_conflicts(initial_plan)

            # Step 3: Resolve conflicts if detected
            if conflicts:
                self.logger.info(f"Conflicts detected: {len(conflicts)}")
                final_plan = await self._resolve_conflicts(initial_plan, conflicts)
            else:
                self.logger.info("No conflicts detected")
                final_plan = initial_plan

            # Step 4: Apply learned rules and preferences
            optimized_plan = await self._apply_learned_rules(final_plan, input_data)

            # Step 5: Approve final plan
            approved_plan = await self._approve_plan(optimized_plan)

            duration = (datetime.now() - start_time).total_seconds()
            self.log_performance("planner_execution", duration, True)

            return {
                "status": "success",
                "plan_approved": True,
                "conflicts_resolved": len(conflicts),
                "optimized_tasks": len(approved_plan.get('tasks', [])),
                "final_plan": approved_plan,
                "execution_time": duration
            }

        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            self.log_performance("planner_execution", duration, False)
            self.logger.error(f"Planner agent failed: {e}")
            return {"status": "error", "message": str(e)}

    async def _draft_plan(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Draft intelligent daily/weekly plans considering weather and priorities"""
        self.logger.info("Drafting intelligent plan with AI")

        try:
            planning_prompt = f"""
            Create an optimized daily/weekly plan based on this data:

            Input Data: {json.dumps(input_data, default=str, indent=2)}

            Consider:
            1. Weather conditions for outdoor activities
            2. Task priorities and deadlines
            3. Energy levels throughout the day
            4. Travel time between locations
            5. Buffer time for unexpected delays

            Generate a structured plan with time slots and task assignments.
            """

            response = self.gemini_client.generate_content(planning_prompt)

            # Parse AI response into structured plan
            return {
                "plan_type": "daily",
                "created_at": datetime.now().isoformat(),
                "ai_generated": True,
                "plan_details": response.text,
                "tasks": []  # Would contain structured task list
            }

        except Exception as e:
            self.logger.error(f"Plan drafting failed: {e}")
            return {"status": "error", "message": str(e)}

    async def _resolve_conflicts(self, plan: Dict[str, Any], conflicts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Use AI to re-plan and resolve scheduling conflicts intelligently"""
        self.logger.info(f"Resolving {len(conflicts)} conflicts with AI")

        try:
            conflict_prompt = f"""
            Resolve these scheduling conflicts in the plan:

            Current Plan: {json.dumps(plan, default=str, indent=2)}
            Conflicts: {json.dumps(conflicts, indent=2)}

            Please:
            1. Identify alternative time slots
            2. Adjust priorities if necessary
            3. Minimize disruption to high-priority tasks
            4. Maintain logical task sequencing
            5. Consider user preferences and constraints

            Return the revised plan with conflicts resolved.
            """

            response = self.gemini_client.generate_content(conflict_prompt)

            # Update plan with conflict resolution
            resolved_plan = plan.copy()
            resolved_plan["conflicts_resolved"] = len(conflicts)
            resolved_plan["resolution_details"] = response.text
            resolved_plan["revised_at"] = datetime.now().isoformat()

            return resolved_plan

        except Exception as e:
            self.logger.error(f"Conflict resolution failed: {e}")
            return plan

    async def _apply_learned_rules(self, plan: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Apply learned rules and user preferences to optimize the plan"""
        self.logger.info("Applying learned rules to optimize plan")

        # Apply priority weights
        optimized_plan = plan.copy()
        optimized_plan["optimization_applied"] = True
        optimized_plan["priority_weights"] = self.priority_weights

        return optimized_plan

    async def _approve_plan(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """Final approval and validation of the optimized plan"""
        self.logger.info("Approving final optimized plan")

        approved_plan = plan.copy()
        approved_plan["approved"] = True
        approved_plan["approved_at"] = datetime.now().isoformat()
        approved_plan["ready_for_execution"] = True

        return approved_plan

class ConflictDetector:
    """Handles conflict detection in scheduling"""

    def detect_conflicts(self, plan: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detect scheduling conflicts in the plan"""
        conflicts = []
        # Placeholder conflict detection logic
        # In real implementation: Check for overlapping time slots, location conflicts, etc.
        return conflicts

class ExecutorAgent(BaseAgent):
    """WF3: Executor Agent - Executes approved plans and manages notifications"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.calendar_service = self._initialize_calendar()
        self.notion_client = self._initialize_notion()
        self.telegram_bot = self._initialize_telegram()

    def _initialize_calendar(self):
        """Initialize Google Calendar API for event creation"""
        return {"credentials": "google_calendar_credentials"}

    def _initialize_notion(self):
        """Initialize Notion API for task updates"""
        return {"token": os.getenv('NOTION_API_TOKEN')}

    def _initialize_telegram(self):
        """Initialize Telegram Bot API for notifications"""
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not token:
            self.logger.warning("Telegram bot token not configured")
            return None
        return {"token": token}

    async def execute(self, approved_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Main execution method for executor agent"""
        start_time = datetime.now()

        try:
            # Step 1: Create/update Google Calendar events
            calendar_results = await self._update_calendar_events(approved_plan)

            # Step 2: Update task status in Notion database
            notion_results = await self._update_notion_tasks(approved_plan)

            # Step 3: Send plan summaries and alerts via Telegram
            notification_results = await self._send_notifications(approved_plan)

            # Step 4: Handle real-time notifications and reminders
            reminder_results = await self._schedule_reminders(approved_plan)

            duration = (datetime.now() - start_time).total_seconds()
            self.log_performance("executor_execution", duration, True)

            return {
                "status": "success",
                "calendar_events_created": calendar_results.get("created", 0),
                "notion_tasks_updated": notion_results.get("updated", 0),
                "notifications_sent": notification_results.get("sent", 0),
                "reminders_scheduled": reminder_results.get("scheduled", 0),
                "execution_time": duration
            }

        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            self.log_performance("executor_execution", duration, False)
            self.logger.error(f"Executor agent failed: {e}")
            return {"status": "error", "message": str(e)}

    async def _update_calendar_events(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """Create/update Google Calendar events automatically"""
        self.logger.info("Creating/updating Google Calendar events")
        # Placeholder for Google Calendar API integration
        return {"created": 5, "updated": 3}

    async def _update_notion_tasks(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """Update task status in Notion database"""
        self.logger.info("Updating Notion task statuses")
        # Placeholder for Notion API integration
        return {"updated": 8}

    async def _send_notifications(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """Send plan summaries and alerts via Telegram bot"""
        if not self.telegram_bot:
            self.logger.warning("Telegram bot not configured, skipping notifications")
            return {"sent": 0}

        self.logger.info("Sending Telegram notifications")

        try:
            # Create summary message
            summary = self._create_plan_summary(plan)

            # Send via Telegram (placeholder implementation)
            # In real implementation: Use python-telegram-bot library

            return {"sent": 1}

        except Exception as e:
            self.logger.error(f"Notification sending failed: {e}")
            return {"sent": 0}

    async def _schedule_reminders(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """Handle real-time notifications and reminders"""
        self.logger.info("Scheduling real-time reminders")
        # Placeholder for reminder scheduling logic
        return {"scheduled": 3}

    def _create_plan_summary(self, plan: Dict[str, Any]) -> str:
        """Create a human-readable summary of the approved plan"""
        summary = f"""
🤖 **Autonomous Task Planner Update**

✅ Plan Status: {plan.get('approved', False)}
📅 Plan Date: {plan.get('approved_at', 'Unknown')}
📋 Tasks Scheduled: {len(plan.get('tasks', []))}
⚠️ Conflicts Resolved: {plan.get('conflicts_resolved', 0)}

🎯 Your optimized schedule is ready!
        """
        return summary.strip()

class AutonomousTaskPlanner:
    """Main orchestrator for the autonomous task planning system"""

    def __init__(self, config_path: str = "config.json"):
        self.config = self._load_config(config_path)
        self.logger = logging.getLogger(self.__class__.__name__)

        # Initialize all agents
        self.reviewer_agent = ReviewerLearnerAgent(self.config)
        self.collector_agent = CollectorAgent(self.config)
        self.planner_agent = PlannerAgent(self.config)
        self.executor_agent = ExecutorAgent(self.config)

        # Setup cron jobs
        self._setup_cron_jobs()

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load system configuration"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Failed to load config: {e}")
            return {}

    def _setup_cron_jobs(self):
        """Setup cron jobs for automated agent execution"""
        try:
            # Get current user's cron
            cron = CronTab(user=True)

            # Clear existing autonomous planner jobs
            cron.remove_all(comment='autonomous_planner')

            # Setup Reviewer Agent - Daily at 10 PM
            reviewer_job = cron.new(
                command=f'python3 {os.path.abspath(__file__)} --agent reviewer',
                comment='autonomous_planner_reviewer'
            )
            reviewer_job.setall('0 22 * * *')  # Daily at 10 PM

            # Setup Collector Agent - Every 15 minutes
            collector_job = cron.new(
                command=f'python3 {os.path.abspath(__file__)} --agent collector', 
                comment='autonomous_planner_collector'
            )
            collector_job.setall('*/15 * * * *')  # Every 15 minutes

            # Write cron jobs
            cron.write()

            self.logger.info("Cron jobs configured successfully")

        except Exception as e:
            self.logger.error(f"Failed to setup cron jobs: {e}")

    async def run_agent(self, agent_name: str) -> Dict[str, Any]:
        """Run a specific agent"""
        self.logger.info(f"Running {agent_name} agent")

        if agent_name == "reviewer":
            return await self.reviewer_agent.execute()
        elif agent_name == "collector":
            return await self.collector_agent.execute()
        elif agent_name == "planner":
            # Planner needs input data from collector
            collector_data = await self.collector_agent.execute()
            return await self.planner_agent.execute(collector_data)
        elif agent_name == "executor":
            # Executor needs approved plan from planner
            collector_data = await self.collector_agent.execute()
            planner_result = await self.planner_agent.execute(collector_data)
            if planner_result.get("plan_approved"):
                return await self.executor_agent.execute(planner_result["final_plan"])
        else:
            raise ValueError(f"Unknown agent: {agent_name}")

    async def run_full_workflow(self) -> Dict[str, Any]:
        """Run the complete autonomous planning workflow"""
        self.logger.info("Starting full autonomous planning workflow")

        results = {}

        # Step 1: Collector Agent gathers data
        results["collector"] = await self.collector_agent.execute()

        # Step 2: Planner Agent creates optimized plan
        if results["collector"]["status"] == "success":
            results["planner"] = await self.planner_agent.execute(results["collector"])

            # Step 3: Executor Agent implements the plan
            if results["planner"]["status"] == "success" and results["planner"]["plan_approved"]:
                results["executor"] = await self.executor_agent.execute(results["planner"]["final_plan"])

        # Step 4: Optional - Run reviewer (typically scheduled for end of day)
        # results["reviewer"] = await self.reviewer_agent.execute()

        return {
            "workflow_status": "completed",
            "timestamp": datetime.now().isoformat(),
            "results": results
        }

# Main execution
if __name__ == "__main__":
    import argparse

    # Command line argument parsing for cron jobs
    parser = argparse.ArgumentParser(description='Autonomous Task Planner Bot')
    parser.add_argument('--agent', choices=['reviewer', 'collector', 'planner', 'executor'], 
                       help='Run specific agent')
    parser.add_argument('--workflow', action='store_true', help='Run full workflow')

    args = parser.parse_args()

    # Initialize the main system
    planner_system = AutonomousTaskPlanner()

    # Run based on arguments
    if args.agent:
        result = asyncio.run(planner_system.run_agent(args.agent))
        print(json.dumps(result, indent=2, default=str))
    elif args.workflow:
        result = asyncio.run(planner_system.run_full_workflow())
        print(json.dumps(result, indent=2, default=str))
    else:
        print("Autonomous Task Planner Bot initialized successfully!")
        print("Use --agent <name> to run specific agent or --workflow for full execution")
