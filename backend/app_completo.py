"""
OÁSÎS - Aplicação Completa em Arquivo Único
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
import numpy as np
from datetime import datetime, timedelta
import uvicorn
import os

# ==================== TENSORFLOW ====================
# No início do arquivo, adicione:
try:
    from transformers import pipeline
    HUGGINGFACE_AVAILABLE = True
    generator = pipeline('text-generation', model='gpt2')
except:
    HUGGINGFACE_AVAILABLE = False
    generator = None

# Na função generate_nudge, substitua por:
def generate_nudge_with_ai(score, work_pattern):
    if HUGGINGFACE_AVAILABLE and generator:
        prompt = f"Generate a short motivational message for someone with burnout score {score}:"
        result = generator(prompt, max_length=50, num_return_sequences=1)
        return result[0]['generated_text']
    else:
        # Fallback para templates
        return random.choice(templates[category])
    
try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras.models import Sequential, load_model
    from tensorflow.keras.layers import LSTM, Dense, Dropout
    from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
    from sklearn.preprocessing import StandardScaler
    import joblib
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
    print(" TensorFlow não disponível - usando modo simulado")

# ==================== BURNOUT PREDICTOR ====================

class BurnoutPredictor:
    """Modelo LSTM para predição de burnout"""
    
    def __init__(self, model_path: str = "models/burnout_predictor.h5"):
        self.model_path = model_path
        self.model = None
        self.scaler = StandardScaler()
        self.sequence_length = 30
        self.n_features = 8
        
        os.makedirs("models", exist_ok=True)
        
    def build_model(self):
        """Constrói modelo LSTM"""
        if not TENSORFLOW_AVAILABLE:
            print(" Modo simulado - modelo não será criado")
            return None
            
        model = Sequential([
            LSTM(128, return_sequences=True, input_shape=(self.sequence_length, self.n_features)),
            Dropout(0.3),
            LSTM(64, return_sequences=True),
            Dropout(0.3),
            LSTM(32),
            Dense(64, activation='relu'),
            Dropout(0.2),
            Dense(32, activation='relu'),
            Dense(4, activation='softmax')
        ])
        
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        self.model = model
        print(" Modelo construído")
        return model
    
    def predict(self, features: np.ndarray) -> Dict:
        """Faz predição"""
        # Modo simulado se não tiver modelo
        if self.model is None:
            score = int(features[0] * 10 + features[1] * 5)  # Fórmula simples
            score = max(20, min(90, score))
            
            confidence = 0.85
            
            if score < 30:
                probs = [0.8, 0.15, 0.05, 0.0]
            elif score < 60:
                probs = [0.2, 0.6, 0.15, 0.05]
            elif score < 80:
                probs = [0.05, 0.2, 0.6, 0.15]
            else:
                probs = [0.0, 0.05, 0.3, 0.65]
            
            return {
                'score': score,
                'confidence': confidence,
                'probabilities': {
                    'Saudável': probs[0],
                    'Atenção': probs[1],
                    'Risco': probs[2],
                    'Crítico': probs[3]
                },
                'trend': 'stable'
            }
        
        # Modo real com modelo
        sequence = []
        for i in range(30):
            noise = np.random.normal(0, 0.05, 8)
            day_features = features + noise
            sequence.append(day_features)
        
        sequence = np.array([sequence])
        prediction = self.model.predict(sequence, verbose=0)
        probs = prediction[0]
        predicted_class = np.argmax(probs)
        confidence = float(probs[predicted_class])
        
        class_to_score = {0: 15, 1: 45, 2: 70, 3: 90}
        score = class_to_score[predicted_class]
        score = int(score * (0.8 + 0.4 * confidence))
        
        return {
            'score': min(score, 100),
            'confidence': confidence,
            'probabilities': {
                'Saudável': float(probs[0]),
                'Atenção': float(probs[1]),
                'Risco': float(probs[2]),
                'Crítico': float(probs[3])
            },
            'trend': 'stable'
        }
    
    def load_model(self):
        """Carrega modelo"""
        if not TENSORFLOW_AVAILABLE:
            print(" Modo simulado ativado")
            return
            
        if os.path.exists(self.model_path):
            self.model = load_model(self.model_path)
            print(f" Modelo carregado de {self.model_path}")
        else:
            print(" Modelo não encontrado - usando modo simulado")

# ==================== AI GENERATOR ====================

class AIMessageGenerator:
    """Gera mensagens personalizadas"""
    
    def __init__(self):
        self.templates = {
            'low': [
                "Você está mantendo um ótimo equilíbrio! Continue assim. ",
                "Seu padrão de trabalho está saudável. Parabéns! "
            ],
            'medium': [
                "Percebi que você tem tido dias intensos. Que tal uma pausa? ",
                "Seu ritmo está acelerado. Considere bloquear tempo para respirar. "
            ],
            'high': [
                "Você teve muitas reuniões hoje. Que tal bloquear 2h amanhã para trabalho focado? ",
                "Seu padrão indica sobrecarga. Hora de redistribuir tarefas. "
            ],
            'critical': [
                "ALERTA: Seu padrão indica risco alto de burnout! ",
                "Situação crítica detectada. Considere falar com seu gestor. "
            ]
        }
    
    def generate_nudge(self, score: int, work_pattern: Dict) -> Dict:
        """Gera nudge"""
        import random
        
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
        
        message = random.choice(self.templates[category])
        
        return {
            'message': message,
            'type': nudge_type,
            'suggested_action': 'create_focus_block' if score > 50 else 'continue_monitoring'
        }
    
    def generate_recommendations(self, score: int, work_pattern: Dict) -> List[str]:
        """Gera recomendações"""
        recommendations = []
        
        if work_pattern.get('hours_worked', 0) > 9:
            recommendations.append("Reduza jornada para 8h ou menos")
        
        if work_pattern.get('meetings_count', 0) > 6:
            recommendations.append("Reduza reuniões em pelo menos 2")
        
        if work_pattern.get('night_work', False):
            recommendations.append("Evite trabalhar após 19h")
        
        if not recommendations:
            recommendations.append("Mantenha o bom trabalho!")
        
        return recommendations[:3]
    
    def generate_team_recommendations(self, overall_score: int, distribution: Dict) -> List[str]:
        """Recomendações para equipe"""
        recommendations = []
        
        risk_count = distribution.get('Risco', 0) + distribution.get('Crítico', 0)
        
        if risk_count > 0:
            recommendations.append(f"{risk_count} membros em risco - redistribuir carga")
        
        if overall_score > 60:
            recommendations.append("Promova pausas regulares")
        else:
            recommendations.append("Equipe saudável!")
        
        return recommendations

# ==================== SERVICES ====================

class CalendarService:
    """Serviço de calendário"""
    def initialize(self):
        print(" Calendário inicializado")

class NotificationService:
    """Serviço de notificações"""
    def initialize(self):
        print(" Notificações inicializadas")
    
    def silence_slack(self, user_id: str, hours: int):
        return {'success': True, 'service': 'Slack'}
    
    def silence_teams(self, user_id: str, hours: int):
        return {'success': True, 'service': 'Teams'}
    
    def set_auto_responder(self, user_id: str, hours: int):
        return {'success': True, 'service': 'Email'}

# ==================== FASTAPI ====================

app = FastAPI(title="OÁSÎS API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar serviços
burnout_predictor = BurnoutPredictor()
ai_generator = AIMessageGenerator()
calendar_service = CalendarService()
notification_service = NotificationService()

# ==================== MODELS ====================

class UserWorkData(BaseModel):
    user_id: str
    hours_worked: float
    meetings_count: int
    avg_time_between_breaks: float
    night_work: bool
    weekend_work: bool
    avg_meeting_duration: float
    meeting_overlap_rate: float
    response_time_after_hours: float

class BurnoutPredictionResponse(BaseModel):
    score: int
    status: str
    confidence: float
    recommendations: List[str]
    trend: str

# ==================== ENDPOINTS ====================

@app.get("/")
async def root():
    return {
        "app": "OÁSÎS API",
        "status": "running",
        "version": "1.0.0",
        "mode": "simulated" if not TENSORFLOW_AVAILABLE else "full"
    }

@app.post("/api/ml/predict", response_model=BurnoutPredictionResponse)
async def predict_burnout(work_data: UserWorkData):
    """Prediz risco de burnout"""
    try:
        features = np.array([
            work_data.hours_worked,
            work_data.meetings_count,
            work_data.avg_time_between_breaks,
            float(work_data.night_work),
            float(work_data.weekend_work),
            work_data.avg_meeting_duration,
            work_data.meeting_overlap_rate,
            work_data.response_time_after_hours
        ])
        
        prediction = burnout_predictor.predict(features)
        score = prediction['score']
        
        if score < 30:
            status = "Saudável"
        elif score < 60:
            status = "Atenção"
        elif score < 80:
            status = "Risco"
        else:
            status = "Crítico"
        
        recommendations = ai_generator.generate_recommendations(score, work_data.dict())
        
        return BurnoutPredictionResponse(
            score=score,
            status=status,
            confidence=prediction['confidence'],
            recommendations=recommendations,
            trend=prediction['trend']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/ml/history/{user_id}")
async def get_history(user_id: str, days: int = 30):
    """Histórico de predições"""
    history = []
    for i in range(days):
        date = datetime.now() - timedelta(days=days - i)
        score = 40 + i + np.random.randint(-5, 5)
        
        if score < 30:
            status = "Saudável"
        elif score < 60:
            status = "Atenção"
        elif score < 80:
            status = "Risco"
        else:
            status = "Crítico"
        
        history.append({
            'date': date.strftime('%Y-%m-%d'),
            'score': min(score, 100),
            'status': status
        })
    
    return {"user_id": user_id, "period_days": days, "predictions": history}

@app.get("/api/nudges/{user_id}")
async def get_nudge(user_id: str):
    """Nudge personalizado"""
    score = 65
    work_pattern = {'hours_worked': 9.5, 'meetings_count': 7, 'night_work': True}
    nudge = ai_generator.generate_nudge(score, work_pattern)
    
    return {
        "nudge": nudge['message'],
        "type": nudge['type'],
        "action": nudge.get('suggested_action'),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/team/health/{team_id}")
async def get_team_health(team_id: str):
    """Dashboard de equipe"""
    team_data = [
        {'score': 25}, {'score': 45}, {'score': 72}, 
        {'score': 30}, {'score': 55}
    ]
    
    overall_score = int(np.mean([m['score'] for m in team_data]))
    
    distribution = {"Saudável": 2, "Atenção": 2, "Risco": 1, "Crítico": 0}
    
    alerts = []
    if distribution["Risco"] > 0:
        alerts.append({
            "severity": "high",
            "message": "1 membro em risco",
            "action": "Redistribuir carga"
        })
    
    recommendations = ai_generator.generate_team_recommendations(overall_score, distribution)
    
    return {
        "overall_score": overall_score,
        "status_distribution": distribution,
        "alerts": alerts,
        "recommendations": recommendations
    }

@app.post("/api/ritual/complete")
async def complete_ritual(ritual_id: str, user_id: str, silence_hours: int = 12):
    """Completa ritual"""
    silenced = ['Slack', 'Teams', 'Email']
    
    return {
        "success": True,
        "silenced_services": silenced,
        "reactivation_time": (datetime.now() + timedelta(hours=silence_hours)).isoformat(),
        "message": " Perfeito! Aproveite seu descanso!"
    }

@app.on_event("startup")
async def startup():
    print(" Iniciando OÁSÎS API...")
    burnout_predictor.load_model()
    calendar_service.initialize()
    notification_service.initialize()
    print(" OÁSÎS API pronta!")

if __name__ == "__main__":
    uvicorn.run("app_completo:app", host="0.0.0.0", port=8000, reload=True)