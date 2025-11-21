"""
IA Generativa REAL usando Hugging Face
"""

import random
from typing import Dict, List

# Importar Hugging Face
try:
    from transformers import pipeline
    print(" Carregando modelo GPT-2... (pode demorar na primeira vez)")
    
    # Inicializa pipeline de geração de texto
    text_generator = pipeline(
        "text-generation",
        model="gpt2",
        device=-1  # CPU (use 0 para GPU)
    )
    
    HUGGINGFACE_AVAILABLE = True
    print(" Modelo GPT-2 carregado com sucesso!")
    
except Exception as e:
    print(f" Erro ao carregar Hugging Face: {e}")
    HUGGINGFACE_AVAILABLE = False
    text_generator = None


class AIGeneratorReal:
    """
    Gerador de mensagens usando IA Generativa REAL (Hugging Face GPT-2)
    """
    
    def __init__(self):
        self.available = HUGGINGFACE_AVAILABLE
        
        # Templates de fallback (caso IA falhe)
        self.templates = {
            'low': [
                "Você está mantendo um ótimo equilíbrio! Continue assim. ",
                "Seu padrão de trabalho está saudável. Parabéns! ",
                "Excelente! Seu ritmo está ideal para produtividade sustentável. "
            ],
            'medium': [
                "Percebi que você tem tido dias intensos. Que tal uma pausa de 15 minutos? ",
                "Seu ritmo está acelerado. Considere bloquear tempo para respirar. ",
                "Atenção ao seu padrão de trabalho. Pausas regulares ajudam! "
            ],
            'high': [
                "Você teve muitas reuniões hoje. Que tal bloquear 2h amanhã para trabalho focado? ",
                "Seu padrão indica sobrecarga. Hora de redistribuir tarefas. ",
                "Alerta: detectei sinais de estresse elevado. Vamos ajustar sua agenda? "
            ],
            'critical': [
                "ALERTA: Seu padrão indica risco alto de burnout! Precisamos agir agora. ",
                "Situação crítica detectada. Considere falar com seu gestor imediatamente. ",
                "URGENTE: Seu bem-estar está em risco. Vamos buscar ajuda? "
            ]
        }
    
    def generate_with_ai(self, prompt: str) -> str:
        """
        Gera texto usando GPT-2 da Hugging Face
        """
        if not self.available or text_generator is None:
            return None
        
        try:
            # Gera texto com GPT-2
            result = text_generator(
                prompt,
                max_length=100,
                num_return_sequences=1,
                temperature=0.8,
                top_p=0.9,
                do_sample=True,
                pad_token_id=50256
            )
            
            # Extrai texto gerado
            generated = result[0]['generated_text']
            
            # Remove o prompt original
            generated = generated.replace(prompt, "").strip()
            
            # Pega até 3 frases
            sentences = []
            for sentence in generated.split('.'):
                sentence = sentence.strip()
                if sentence and len(sentence) > 10:
                    sentences.append(sentence)
                if len(sentences) >= 2:
                    break
            
            if sentences:
                message = '. '.join(sentences) + '.'
                # Limpa caracteres estranhos
                message = message.replace('\n', ' ').strip()
                return message if len(message) > 20 else None
            
            return None
            
        except Exception as e:
            print(f" Erro na geração: {e}")
            return None
    
    def generate_nudge(self, score: int, work_pattern: Dict) -> Dict:
        """
        Gera nudge personalizado usando IA Generativa
        """
        
        # Determina categoria
        if score < 30:
            category = 'low'
            nudge_type = 'motivation'
            tone = "positive and encouraging"
        elif score < 60:
            category = 'medium'
            nudge_type = 'reminder'
            tone = "gentle and supportive"
        elif score < 80:
            category = 'high'
            nudge_type = 'alert'
            tone = "concerned but helpful"
        else:
            category = 'critical'
            nudge_type = 'urgent'
            tone = "urgent but caring"
        
        # Constrói prompt para IA
        hours = work_pattern.get('hours_worked', 8)
        meetings = work_pattern.get('meetings_count', 5)
        night_work = work_pattern.get('night_work', False)
        
        # Prompt otimizado para GPT-2
        prompt = f"As a workplace wellness advisor, write a {tone} message for an employee with burnout score {score}/100. They work {hours} hours daily with {meetings} meetings. Message:"
        
        # Tenta gerar com IA
        ai_message = self.generate_with_ai(prompt)
        
        if ai_message and len(ai_message) > 30:
            print(f" Mensagem gerada com IA Generativa (GPT-2)")
            return {
                'message': ai_message,
                'type': nudge_type,
                'suggested_action': self._get_action(score),
                'generated_by': ' Hugging Face GPT-2'
            }
        
        # Fallback: usa templates
        print(f" IA não gerou mensagem válida, usando template")
        template_message = random.choice(self.templates[category])
        
        # Personaliza template com dados reais
        if '{meetings}' in template_message:
            template_message = template_message.format(meetings=meetings)
        if '{hours}' in template_message:
            template_message = template_message.format(hours=hours)
        
        return {
            'message': template_message,
            'type': nudge_type,
            'suggested_action': self._get_action(score),
            'generated_by': ' Template Personalizado'
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
        """
        Gera recomendações personalizadas
        """
        recommendations = []
        
        hours = work_pattern.get('hours_worked', 0)
        meetings = work_pattern.get('meetings_count', 0)
        night_work = work_pattern.get('night_work', False)
        weekend_work = work_pattern.get('weekend_work', False)
        breaks = work_pattern.get('avg_time_between_breaks', 120)
        
        # Análise inteligente
        if hours > 10:
            recommendations.append(f" Reduza jornada de {hours}h para máximo 8h por dia")
        elif hours > 8:
            recommendations.append(f" Tente reduzir de {hours}h para 8h diárias")
        
        if meetings > 8:
            recommendations.append(f" Reduza reuniões de {meetings} para máximo 6 por dia")
        elif meetings > 6:
            recommendations.append(f" Considere consolidar algumas das {meetings} reuniões")
        
        if night_work:
            recommendations.append(" Evite trabalhar após 19h - estabeleça limites claros")
        
        if weekend_work:
            recommendations.append(" Preserve seus finais de semana para descanso")
        
        if breaks < 60:
            recommendations.append(f" Aumente pausas de {int(breaks)}min para pelo menos 90min")
        
        # Se tudo estiver bem
        if not recommendations:
            recommendations.append(" Mantenha esse excelente padrão de trabalho!")
            recommendations.append(" Continue priorizando seu bem-estar")
        
        # Limita a 3 recomendações mais importantes
        return recommendations[:3]
    
    def generate_team_recommendations(self, overall_score: int, distribution: Dict) -> List[str]:
        """
        Gera recomendações para gestores da equipe
        """
        recommendations = []
        
        total_members = sum(distribution.values())
        risk_count = distribution.get('Risco', 0) + distribution.get('Crítico', 0)
        critical_count = distribution.get('Crítico', 0)
        
        # Situação crítica
        if critical_count > 0:
            recommendations.append(f" URGENTE: {critical_count} membro(s) em estado crítico - ação imediata necessária")
        
        # Membros em risco
        if risk_count > 0:
            percentage = (risk_count / total_members) * 100
            recommendations.append(f" {risk_count} membro(s) em risco ({percentage:.0f}% da equipe) - redistribuir carga")
        
        # Score geral alto
        if overall_score > 70:
            recommendations.append(" Score geral elevado - promova pausas regulares e reduza reuniões em 20%")
        elif overall_score > 50:
            recommendations.append(" Atenção ao bem-estar da equipe - implemente blocos de foco")
        else:
            recommendations.append(" Equipe saudável! Mantenha as práticas atuais")
        
        # Recomendações gerais
        if total_members > 5:
            recommendations.append(" Considere check-ins 1:1 semanais para monitorar bem-estar")
        
        return recommendations[:4]


# Singleton para não recarregar modelo
_ai_generator_instance = None

def get_ai_generator():
    """Retorna instância única do gerador"""
    global _ai_generator_instance
    if _ai_generator_instance is None:
        _ai_generator_instance = AIGeneratorReal()
    return _ai_generator_instance