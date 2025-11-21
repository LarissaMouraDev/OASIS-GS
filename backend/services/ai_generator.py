"""
Gerador de IA - Mensagens Personalizadas
"""

import random
from typing import Dict, List

class AIMessageGenerator:
    """Gera mensagens personalizadas usando regras"""
    
    def __init__(self):
        self.templates = {
            'low': [
                "Você está mantendo um ótimo equilíbrio! Continue assim. ",
                "Seu padrão de trabalho está saudável. Parabéns! ",
                "Que tal aproveitar esse bom momento para planejar algo divertido? "
            ],
            'medium': [
                "Percebi que você tem tido dias intensos. Que tal uma pausa de 15 minutos? ",
                "Seu ritmo está acelerado. Considere bloquear tempo para respirar. ",
                "Atenção: você merece momentos de descanso. Vamos cuidar disso? "
            ],
            'high': [
                "Você teve {meetings} reuniões hoje. Que tal bloquear 2h amanhã para trabalho focado? ",
                "Percebi trabalho noturno recente. Vamos criar limites saudáveis? ",
                "Seu padrão indica sobrecarga. Hora de redistribuir tarefas. "
            ],
            'critical': [
                "ALERTA: Seu padrão indica risco alto de burnout. Precisamos agir agora! ",
                "Você trabalhou {hours}h hoje. Isso não é sustentável. Vamos conversar? ",
                "Situação crítica detectada. Considere falar com seu gestor. "
            ]
        }
    
    def generate_nudge(self, score: int, work_pattern: Dict) -> Dict:
        """Gera nudge personalizado"""
        
        if score < 30:
            category = 'low'
            nudge_type = 'motivation'
        elif score < 60:
            category = 'medium'
            nudge_type = 'reminder'
        elif score < 80:
            category = 'high'
            nudge_type = 'alert'
        else:
            category = 'critical'
            nudge_type = 'urgent'
        
        # Seleciona template
        template = random.choice(self.templates[category])
        
        # Substitui variáveis
        message = template.format(
            meetings=work_pattern.get('meetings_count', 0),
            hours=work_pattern.get('hours_worked', 0)
        )
        
        return {
            'message': message,
            'type': nudge_type,
            'suggested_action': self._get_action(score)
        }
    
    def _get_action(self, score: int) -> str:
        """Sugere ação baseada no score"""
        if score < 30:
            return "continue_monitoring"
        elif score < 60:
            return "schedule_break"
        elif score < 80:
            return "create_focus_block"
        else:
            return "talk_to_manager"
    
    def generate_recommendations(self, score: int, work_pattern: Dict) -> List[str]:
        """Gera recomendações"""
        recommendations = []
        
        if work_pattern.get('hours_worked', 0) > 9:
            recommendations.append("Reduza jornada para 8h ou menos")
        
        if work_pattern.get('meetings_count', 0) > 6:
            recommendations.append(f"Reduza reuniões de amanhã em pelo menos 2")
        
        if work_pattern.get('night_work', False):
            recommendations.append("Evite trabalhar após 19h")
        
        if work_pattern.get('avg_time_between_breaks', 120) < 60:
            recommendations.append("Faça pausas a cada 90 minutos")
        
        if not recommendations:
            recommendations.append("Mantenha o bom trabalho!")
        
        return recommendations[:3]  # Máximo 3
    
    def generate_team_recommendations(self, overall_score: int, distribution: Dict) -> List[str]:
        """Gera recomendações para equipe"""
        recommendations = []
        
        risk_count = distribution.get('Risco', 0) + distribution.get('Crítico', 0)
        
        if risk_count > 0:
            recommendations.append(f"{risk_count} membros em risco - considere redistribuir carga")
        
        if overall_score > 60:
            recommendations.append("Promova pausas regulares para toda equipe")
            recommendations.append("Reduza reuniões em 20%")
        
        if overall_score < 40:
            recommendations.append("Equipe saudável! Mantenha as práticas atuais")
        
        return recommendations