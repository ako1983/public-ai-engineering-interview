"""
AI Health Assistant Chat Agent

This module implements a LangChain-powered chat agent that can interact with
patient EMR data, wearables analytics, and RevDoc's healthcare services.
"""

import os
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from .emr_parser import extract_chronic_conditions, extract_vital_events
from .wearables_analytics import analyze_heartrate_trends, analyze_glucose_trends

load_dotenv()

class HealthChatAgent:
    def __init__(self):
        # Initialize OpenAI client
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        self.llm = ChatOpenAI(
            temperature=0,
            model="gpt-4",
            openai_api_key=openai_api_key
        )
        
        # Create LangChain tools
        self.tools = [
            Tool(
                name="GetChronicConditions",
                func=self._get_chronic_conditions,
                description="Returns list of chronic conditions from EMR data for the current user."
            ),
            Tool(
                name="GetVitalEvents",
                func=self._get_vital_events,
                description="Returns significant health events (hospitalizations, procedures, ER visits) from EMR data for the current user."
            ),
            Tool(
                name="AnalyzeGlucoseTrend", 
                func=self._analyze_glucose_trend,
                description="Analyzes glucose trends from CGM data (Freestyle Libre, Dexcom) for the current user."
            ),
            Tool(
                name="AnalyzeHeartRateTrend",
                func=self._analyze_heartrate_trend,
                description="Analyzes heartrate and HRV trends from wearables data for the current user."
            )
        ]
        
        # Initialize the agent
        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.OPENAI_FUNCTIONS,
            verbose=True,
            handle_parsing_errors=True
        )
        
        self.current_user_id = None

    def chat(self, user_id: str, message: str) -> str:
        """
        Process a chat message for a specific user.
        
        Args:
            user_id: Vital user ID
            message: User's chat message
            
        Returns:
            str: AI assistant response
        """
        self.current_user_id = user_id
        
        try:
            # Add context about the user to the message
            contextualized_message = f"""
User ID: {user_id}
User Message: {message}

Please provide a helpful response about the user's health data, and use the available tools to get real-time information when relevant. Be conversational and friendly, but professional. If you're booking appointments or refilling prescriptions, confirm the action was completed.
"""
            
            response = self.agent.run(contextualized_message)
            return response
            
        except Exception as e:
            return f"I apologize, but I encountered an error processing your request: {str(e)}. Please try again or rephrase your question."

    # Tool implementation methods
    def _get_chronic_conditions(self, input_text="") -> str:
        """Get chronic conditions from EMR data"""
        try:
            chronic_conditions = extract_chronic_conditions(self.current_user_id)
            
            if not chronic_conditions:
                return "No chronic conditions found in your medical records."
            
            # Format the conditions for display
            condition_descriptions = []
            for condition in chronic_conditions:
                status_text = f" ({condition.status})" if condition.status else ""
                condition_descriptions.append(f"{condition.description}{status_text}")
            
            return f"Your chronic conditions: {', '.join(condition_descriptions)}"
            
        except Exception as e:
            return f"Unable to retrieve chronic conditions: {str(e)}"

    def _get_vital_events(self, input_text="") -> str:
        """Get significant health events from EMR data"""
        try:
            vital_events = extract_vital_events(self.current_user_id)
            
            if not vital_events:
                return "No significant health events found in your medical records."
            
            # Format the events for display
            event_descriptions = []
            for event in vital_events:
                date_str = event.date.strftime("%B %d, %Y") if event.date else "Unknown date"
                provider_text = f" at {event.provider}" if event.provider else ""
                event_descriptions.append(f"{event.description} ({event.event_type}) on {date_str}{provider_text}")
            
            return f"Your significant health events:\n" + "\n".join([f"- {desc}" for desc in event_descriptions])
            
        except Exception as e:
            return f"Unable to retrieve vital events: {str(e)}"

    def _analyze_glucose_trend(self, input_text="") -> str:
        """Analyze glucose trends from CGM data"""
        try:
            glucose_analysis = analyze_glucose_trends(self.current_user_id)
            
            if not glucose_analysis:
                return "No glucose data available for analysis."
            
            # Format the analysis results
            avg_trend = glucose_analysis.average_glucose_trend
            time_in_range = glucose_analysis.time_in_range_trend
            
            result = f"Glucose Analysis:\n"
            result += f"- Average glucose trend: {avg_trend.trend_direction.value} "
            result += f"(confidence: {avg_trend.confidence_score:.1%})\n"
            result += f"- Time in range: {time_in_range.average_value:.1f}% "
            result += f"({time_in_range.trend_direction.value})\n"
            
            if glucose_analysis.hypo_episodes > 0:
                result += f"- Hypoglycemic episodes: {glucose_analysis.hypo_episodes}\n"
            if glucose_analysis.hyper_episodes > 0:
                result += f"- Hyperglycemic episodes: {glucose_analysis.hyper_episodes}\n"
            
            if glucose_analysis.risk_factors:
                result += f"- Risk factors: {', '.join(glucose_analysis.risk_factors)}"
            
            return result
            
        except Exception as e:
            return f"Unable to analyze glucose trends: {str(e)}"


    def _analyze_heartrate_trend(self, input_text="") -> str:
        """Analyze heartrate trends"""
        try:
            heartrate_analysis = analyze_heartrate_trends(self.current_user_id)
            
            if not heartrate_analysis:
                return "No heartrate data available for analysis."
            
            # Format the heartrate analysis results
            resting_hr = heartrate_analysis.resting_hr_trend
            max_hr = heartrate_analysis.max_hr_trend
            hrv = heartrate_analysis.hrv_trend
            
            result = f"Heart Rate Analysis:\n"
            result += f"- Resting HR trend: {resting_hr.trend_direction.value} "
            result += f"(avg: {resting_hr.average_value:.1f} bpm)\n"
            result += f"- Max HR trend: {max_hr.trend_direction.value} "
            result += f"(avg: {max_hr.average_value:.1f} bpm)\n"
            
            if hrv:
                result += f"- HRV trend: {hrv.trend_direction.value} "
                result += f"(avg: {hrv.average_value:.1f} ms)\n"
            
            result += f"- Anomalies detected: {heartrate_analysis.anomaly_count}\n"
            
            if heartrate_analysis.risk_factors:
                result += f"- Risk factors: {', '.join(heartrate_analysis.risk_factors)}"
            
            return result
            
        except Exception as e:
            return f"Unable to analyze heartrate trends: {str(e)}"


# Global agent instance
_chat_agent = None

def get_chat_agent() -> HealthChatAgent:
    """Get singleton chat agent instance"""
    global _chat_agent
    if _chat_agent is None:
        _chat_agent = HealthChatAgent()
    return _chat_agent