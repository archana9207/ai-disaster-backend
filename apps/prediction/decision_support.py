"""
Decision support rules mapped to each disaster type.
Used to provide actionable recommendations based on prediction.
"""

DECISION_SUPPORT_MAP = {
    'Flood': {
        'recommendation': 'Immediate flood alert. Evacuate low‑lying areas. Activate emergency response teams.',
        'actions': [
            'Monitor river and reservoir levels every hour',
            'Deploy sandbags and temporary barriers',
            'Arrange rescue boats and shelters',
            'Issue public warning via SMS/radio',
            'Prepare relief supplies (food, water, medicine)'
        ]
    },
    'Drought': {
        'recommendation': 'Implement water conservation measures. Restrict non‑essential water usage.',
        'actions': [
            'Enforce water use restrictions',
            'Check reservoir and groundwater levels',
            'Launch public awareness campaign',
            'Arrange water tankers for affected areas',
            'Assess crop damage and plan subsidies'
        ]
    },
    'Storm': {
        'recommendation': 'Secure all loose objects. Advise citizens to stay indoors. Cancel outdoor events.',
        'actions': [
            'Issue high‑wind warning',
            'Trim trees and secure power lines',
            'Close schools and public gatherings',
            'Activate storm shelters',
            'Prepare emergency medical services'
        ]
    },
    'Normal': {
        'recommendation': 'No immediate action required. Continue routine weather monitoring.',
        'actions': [
            'Standard weather observation',
            'Update local forecast database',
            'No public alert needed'
        ]
    }
}


def get_decision_support(disaster_type: str) -> dict:
    """
    Returns recommendation and actions for a given disaster type.
    Defaults to 'Normal' if type is unknown.
    """
    return DECISION_SUPPORT_MAP.get(disaster_type, DECISION_SUPPORT_MAP['Normal'])