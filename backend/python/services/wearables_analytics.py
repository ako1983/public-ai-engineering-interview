"""
Wearables Data Analytics Service

This module processes and analyzes wearables data to identify health trends
and patterns.

TODO: Implement the following functions for the coding interview:
1. analyze_heartrate_trends() - Process heartrate data
2. analyze_glucose_trends() - Process glucose data
"""

from typing import List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel
from enum import Enum
from vital import Client
import os
from dotenv import load_dotenv

# Load environment variables and initialize Vital client
load_dotenv()
VITAL_API_KEY = os.getenv("VITAL_API_KEY")
VITAL_ENVIRONMENT = os.getenv("VITAL_ENV")
VITAL_REGION = os.getenv("VITAL_REGION")

client = Client(api_key=VITAL_API_KEY, environment=VITAL_ENVIRONMENT, region=VITAL_REGION)


class TrendDirection(str, Enum):
    IMPROVING = "improving"
    STABLE = "stable"
    DECLINING = "declining"
    INSUFFICIENT_DATA = "insufficient_data"


class BiometricTrend(BaseModel):
    """Represents a trend analysis for a specific biometric"""
    metric_name: str
    trend_direction: TrendDirection
    confidence_score: float  # 0.0 to 1.0
    average_value: float
    trend_percentage: float  # positive = improving, negative = declining
    data_points: int
    analysis_period_days: int
    last_updated: datetime


class HeartRateAnalysis(BaseModel):
    """Heartrate trend analysis results"""
    resting_hr_trend: BiometricTrend
    max_hr_trend: BiometricTrend
    hrv_trend: Optional[BiometricTrend]
    anomaly_count: int
    risk_factors: List[str]


class GlucoseAnalysis(BaseModel):
    """Glucose trend analysis results"""
    average_glucose_trend: BiometricTrend
    time_in_range_trend: BiometricTrend  # Percentage time in 70-180 mg/dL
    variability_trend: BiometricTrend
    dawn_phenomenon_severity: Optional[float]
    hypo_episodes: int
    hyper_episodes: int
    risk_factors: List[str]


# class WearablesHealthMetrics(BaseModel):
#     """Consolidated wearables health metrics for scoring"""
#     user_id: str
#     heartrate_analysis: Optional[HeartRateAnalysis]
#     glucose_analysis: Optional[GlucoseAnalysis]
#     overall_trend_score: float  # 0-100, higher = better trends
#     data_quality_score: float  # 0-100, higher = more reliable data
#     last_analysis: datetime


def analyze_heartrate_trends(user_id: str) -> HeartRateAnalysis:
    """
    Analyze heartrate trends from Vital API data (Oura, Fitbit, etc.).
    
    Key metrics to analyze:
    - Resting heartrate trends (lower is generally better)
    - Heartrate variability (HRV) trends (higher is generally better)
    - Anomaly detection (unusual spikes/drops)
    
    Args:
        user_id: Vital user ID
        
    Returns:
        HeartRateAnalysis: Comprehensive heartrate trend analysis
    """
    try:
        # Get heartrate data from Vital API
        heartrate_data = get_heartrate_data(user_id)
        # print(f"Heartrate data for user {user_id}: {heartrate_data}")
        if not heartrate_data:
            return None
        
        # For now, return a simple analysis with the data
        # TODO: Implement actual trend analysis algorithms
        
        return HeartRateAnalysis(
            resting_hr_trend=BiometricTrend(
                metric_name="resting_heartrate",
                trend_direction=TrendDirection.INSUFFICIENT_DATA,
                confidence_score=0.0,
                average_value=0.0,
                trend_percentage=0.0,
                data_points=len(heartrate_data) if heartrate_data else 0,
                analysis_period_days=7,
                last_updated=datetime.now()
            ),
            max_hr_trend=BiometricTrend(
                metric_name="max_heartrate",
                trend_direction=TrendDirection.INSUFFICIENT_DATA,
                confidence_score=0.0,
                average_value=0.0,
                trend_percentage=0.0,
                data_points=len(heartrate_data) if heartrate_data else 0,
                analysis_period_days=7,
                last_updated=datetime.now()
            ),
            hrv_trend=None,
            anomaly_count=0,
            risk_factors=[]
        )
    except Exception as e:
        print(f"Error getting heartrate data for user {user_id}: {e}")
        return None


def analyze_glucose_trends(user_id: str) -> GlucoseAnalysis:
    """
    Analyze glucose trends from CGM data (Freestyle Libre, Dexcom).
    
    Key metrics to analyze:
    - Average glucose levels
    - Time in range (70-180 mg/dL for non-diabetics, 70-140 for diabetics)
    - Glucose variability (coefficient of variation)
    - Dawn phenomenon detection; periodic episodes of hyperglycemia experienced by patients with diabetes in the early morning hours
    - Hypoglycemic/hyperglycemic episodes
        - Hypoglycemic episodes: episodes of blood glucose below 70 mg/dL
        - Hyperglycemic episodes: episodes of blood glucose above 180 mg/dL
    
    Args:
        user_id: Vital user ID
        
    Returns:
        GlucoseAnalysis: Comprehensive glucose trend analysis
    """
    try:
        glucose_data = get_glucose_data(user_id)
        # print(f"Glucose data for user {user_id}: {glucose_data}")
        if not glucose_data:
            return None
        
        # For now, return a simple analysis with the data
        # TODO: Implement actual glucose trend analysis algorithms
        
        return GlucoseAnalysis(
            average_glucose_trend=BiometricTrend(
                metric_name="average_glucose",
                trend_direction=TrendDirection.INSUFFICIENT_DATA,
                confidence_score=0.0,
                average_value=0.0,
                trend_percentage=0.0,
                data_points=len(glucose_data) if glucose_data else 0,
                analysis_period_days=7,
                last_updated=datetime.now()
            ),
            time_in_range_trend=BiometricTrend(
                metric_name="time_in_range",
                trend_direction=TrendDirection.INSUFFICIENT_DATA,
                confidence_score=0.0,
                average_value=0.0,
                trend_percentage=0.0,
                data_points=len(glucose_data) if glucose_data else 0,
                analysis_period_days=7,
                last_updated=datetime.now()
            ),
            variability_trend=BiometricTrend(
                metric_name="glucose_variability",
                trend_direction=TrendDirection.INSUFFICIENT_DATA,
                confidence_score=0.0,
                average_value=0.0,
                trend_percentage=0.0,
                data_points=len(glucose_data) if glucose_data else 0,
                analysis_period_days=7,
                last_updated=datetime.now()
            ),
            dawn_phenomenon_severity=None,
            hypo_episodes=0,
            hyper_episodes=0,
            risk_factors=[]
        )
    except Exception as e:
        print(f"Error getting glucose data for user {user_id}: {e}")
        return None


def get_glucose_data(user_id: str):
    """
    Get glucose data from Vital API for a given user.
    
    Args:
        user_id: Vital user ID
        
    Returns:
        Glucose data from Vital API
    """
    try:
        glucose_data = client.Vitals.glucose(
            user_id=user_id,
            start_date=(datetime.now() - timedelta(days=7)).isoformat(),
            end_date=datetime.now().isoformat()
        )
        if not glucose_data:
             return None
         # For now, just return the raw data
        return glucose_data
    except Exception as e:
        print(f"Error getting glucose data for user {user_id}: {e}")
        return None


def get_heartrate_data(user_id: str):
    """
    Get heartrate data from Vital API for a given user.
    
    Args:
        user_id: Vital user ID
        
    Returns:
        Heartrate data from Vital API
    """
    try:
        heartrate_data = client.Vitals.heartrate(
            user_id=user_id,
            start_date=(datetime.now() - timedelta(days=7)).isoformat(),
            end_date=datetime.now().isoformat()
        )
        if not heartrate_data:
            return None
        # For now, just return the raw data
        return heartrate_data
    except Exception as e:
        print(f"Error getting heartrate data for user {user_id}: {e}")
        return None