"""
Serviço de Notificações - Mock
"""

from typing import Dict

class NotificationService:
    """Serviço simulado de notificações"""
    
    def __init__(self):
        self.mock_mode = True
    
    def initialize(self):
        """Inicializa serviço"""
        print(" Serviço de notificações inicializado (modo mock)")
    
    def silence_slack(self, user_id: str, duration_hours: int) -> Dict:
        """Silencia Slack"""
        return {
            'success': True,
            'service': 'Slack',
            'duration_hours': duration_hours,
            'message': f'DND ativado por {duration_hours}h'
        }
    
    def silence_teams(self, user_id: str, duration_hours: int) -> Dict:
        """Silencia Teams"""
        return {
            'success': True,
            'service': 'Teams',
            'duration_hours': duration_hours,
            'message': 'Status "Offline" ativado'
        }
    
    def set_auto_responder(self, user_id: str, duration_hours: int) -> Dict:
        """Configura auto-responder de email"""
        return {
            'success': True,
            'service': 'Email',
            'duration_hours': duration_hours,
            'message': 'Resposta automática configurada'
        }