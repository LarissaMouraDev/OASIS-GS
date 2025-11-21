"""
OÁSÎS Backend - API Principal
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import numpy as np
from datetime import datetime, timedelta
import uvicorn

# Importações locais
from ml.burnout_predictor import BurnoutPredictor
from services.calendar_service import CalendarService
from services.notification_service import NotificationService
from services.ai_generator import AIMessageGenerator

# Inicialização
app = FastAPI(
    title="OÁSÎS API",
    description="API de Equilíbrio Híbrido Inteligente",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serviços
burnout_predictor = BurnoutPredictor()
calendar_service = CalendarService()
notification_service = NotificationService()
ai_generator = AIMessageGenerator()

# ==================== MODELS ====================

class UserWorkData(BaseModel):
    """Dados de trabalho do usuário"""
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
    """Resposta da predição"""
    score: int
    status: str
    confidence: float
    recommendations: List[str]
    trend: str

class FocusBlockRequest(BaseModel):
    """Request para bloco de foco"""
    user_id: str
    preferred_time: Optional[str] = "morning"
    duration_minutes: int = 90
    frequency: str = "daily"

class RitualRequest(BaseModel):
    """Request para ritual"""
    user_id: str
    priorities: List[str]
    activity_choice: str
    silence_duration_hours: int = 12

# ==================== ENDPOINTS ====================

@app.get("/")
async def root():
    """Health check"""
    return {
        "app": "OÁSÎS API",
        "status": "running",
        "version": "1.0.0"
    }

@app.post("/api/ml/predict", response_model=BurnoutPredictionResponse)
async def predict_burnout(work_data: UserWorkData):
    """
    Prediz risco de burnout
    """
    try:
        # Prepara features
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
        
        # Predição
        prediction = burnout_predictor.predict(features)
        
        # Status
        score = prediction['score']
        if score < 30:
            status = "Saudável"
        elif score < 60:
            status = "Atenção"
        elif score < 80:
            status = "Risco"
        else:
            status = "Crítico"
        
        # Recomendações
        recommendations = ai_generator.generate_recommendations(
            score=score,
            work_pattern=work_data.dict()
        )
        
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
    """Retorna histórico"""
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
    
    return {
        "user_id": user_id,
        "period_days": days,
        "predictions": history
    }

@app.post("/api/calendar/protect-time")
async def create_focus_blocks(request: FocusBlockRequest):
    """Cria blocos de foco"""
    try:
        calendar = calendar_service.get_user_calendar(request.user_id)
        suggested_times = calendar_service.analyze_best_focus_times(calendar)
        
        created_blocks = []
        for time_slot in suggested_times[:5]:
            block = calendar_service.create_focus_block(
                user_id=request.user_id,
                start_time=time_slot['start'],
                duration=request.duration_minutes
            )
            created_blocks.append(block)
        
        return {
            "success": True,
            "blocks_created": len(created_blocks),
            "details": created_blocks
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/nudges/{user_id}")
async def get_nudge(user_id: str):
    """Retorna nudge personalizado"""
    # Simula dados do usuário
    score = 65
    work_pattern = {
        'hours_worked': 9.5,
        'meetings_count': 7,
        'night_work': True
    }
    
    nudge = ai_generator.generate_nudge(score, work_pattern)
    
    return {
        "nudge": nudge['message'],
        "type": nudge['type'],
        "action": nudge.get('suggested_action'),
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/ritual/start")
async def start_ritual(request: RitualRequest):
    """Inicia ritual de transição"""
    activity = {
        "breathing": {
            "type": "breathing",
            "duration_minutes": 3,
            "instructions": "Respire: 4s inspirar, 4s segurar, 4s expirar"
        },
        "soundscape": {
            "type": "soundscape",
            "duration_minutes": 5,
            "options": ["Floresta", "Chuva", "Oceano"]
        }
    }
    
    return {
        "ritual_id": f"ritual_{datetime.now().timestamp()}",
        "step": "1_priorities_saved",
        "next_step": "decompress_activity",
        "activity": activity.get(request.activity_choice, activity["breathing"]),
        "message": " Prioridades salvas! Vamos relaxar..."
    }

@app.post("/api/ritual/complete")
async def complete_ritual(ritual_id: str, user_id: str, silence_hours: int = 12):
    """Completa ritual"""
    silenced = []
    
    slack = notification_service.silence_slack(user_id, silence_hours)
    if slack['success']:
        silenced.append('Slack')
    
    teams = notification_service.silence_teams(user_id, silence_hours)
    if teams['success']:
        silenced.append('Teams')
    
    email = notification_service.set_auto_responder(user_id, silence_hours)
    if email['success']:
        silenced.append('Email')
    
    return {
        "success": True,
        "ritual_completed": True,
        "silenced_services": silenced,
        "reactivation_time": (datetime.now() + timedelta(hours=silence_hours)).isoformat(),
        "message": "🌙 Perfeito! Aproveite seu descanso!"
    }

@app.get("/api/team/health/{team_id}")
async def get_team_health(team_id: str):
    """Dashboard de equipe"""
    # Simula dados da equipe
    team_data = [
        {'score': 25, 'status': 'Saudável'},
        {'score': 45, 'status': 'Atenção'},
        {'score': 72, 'status': 'Risco'},
        {'score': 30, 'status': 'Saudável'},
        {'score': 55, 'status': 'Atenção'},
    ]
    
    overall_score = int(np.mean([m['score'] for m in team_data]))
    
    distribution = {
        "Saudável": sum(1 for m in team_data if m['status'] == 'Saudável'),
        "Atenção": sum(1 for m in team_data if m['status'] == 'Atenção'),
        "Risco": sum(1 for m in team_data if m['status'] == 'Risco'),
        "Crítico": 0
    }
    
    alerts = []
    if distribution["Risco"] > 0:
        alerts.append({
            "severity": "high",
            "message": f"{distribution['Risco']} membro(s) em risco",
            "action": "Considere redistribuir carga"
        })
    
    recommendations = ai_generator.generate_team_recommendations(
        overall_score, distribution
    )
    
    return {
        "overall_score": overall_score,
        "status_distribution": distribution,
        "alerts": alerts,
        "recommendations": recommendations
    }

# ==================== STARTUP ====================

@app.on_event("startup")
async def startup():
    """Inicialização"""
    print(" Iniciando OÁSÎS API...")
    burnout_predictor.load_model()
    calendar_service.initialize()
    notification_service.initialize()
    print(" OÁSÎS API pronta!")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)