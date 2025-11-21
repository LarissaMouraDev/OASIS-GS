"""
Serviço de Calendário - Mock
"""

from datetime import datetime, timedelta
from typing import Dict, List
import random

class CalendarService:
    """Serviço simulado de calendário"""
    
    def __init__(self):
        self.mock_mode = True  # Modo mock para demonstração
    
    def initialize(self):
        """Inicializa serviço"""
        print(" Serviço de calendário inicializado (modo mock)")
    
    def get_user_calendar(self, user_id: str) -> List[Dict]:
        """Retorna calendário do usuário (mock)"""
        events = []
        now = datetime.now()
        
        # Gera eventos fictícios
        for i in range(5):
            start = now + timedelta(days=i, hours=random.randint(9, 16))
            events.append({
                'id': f'event_{i}',
                'title': f'Reunião {i+1}',
                'start': start.isoformat(),
                'duration': random.randint(30, 60)
            })
        
        return events
    
    def analyze_best_focus_times(self, calendar: List[Dict], preferred_time: str = None) -> List[Dict]:
        """Analisa melhores horários para foco"""
        suggestions = []
        now = datetime.now()
        
        # Sugere manhãs (9h-11h)
        for i in range(1, 6):  # Próximos 5 dias
            start = now + timedelta(days=i)
            start = start.replace(hour=9, minute=0, second=0)
            
            suggestions.append({
                'start': start.isoformat(),
                'end': (start + timedelta(minutes=90)).isoformat(),
                'reason': 'Manhã produtiva, sem conflitos'
            })
        
        return suggestions
    
    def create_focus_block(self, user_id: str, start_time: str, duration: int) -> Dict:
        """Cria bloco de foco"""
        return {
            'id': f'focus_{datetime.now().timestamp()}',
            'title': ' Bloco de Foco (OÁSÎS)',
            'start': start_time,
            'duration': duration,
            'created': True
        }
    
    def suggest_alternatives(self, user_id: str, requested_time: str, duration: int) -> List[Dict]:
        """Sugere horários alternativos"""
        alternatives = []
        base = datetime.fromisoformat(requested_time)
        
        # Sugere 3 alternativas
        for i in range(1, 4):
            alt_time = base + timedelta(hours=i)
            alternatives.append({
                'start': alt_time.isoformat(),
                'end': (alt_time + timedelta(minutes=duration)).isoformat(),
                'available': True
            })
        
        return alternatives