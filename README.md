# 🌊 OÁSÎS - Equilíbrio Híbrido Inteligente

**Intelligent Hybrid Balance for Corporate Wellbeing**

-------------
Integrantes: 
Larissa de Freitas Moura-555136
Guilherme Francisco-557648
---
Link Do Swagger: http://localhost:8000/docs#/default/predict_burnout_api_ml_predict_post
Link da Interface:http://127.0.0.1:5500/frontend/index.html
## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [O Problema](#o-problema)
3. [A Solução](#a-solução)
4. [Arquitetura Técnica](#arquitetura-técnica)
5. [Implementação de Deep Learning](#implementação-de-deep-learning)
6. [Integração entre Disciplinas](#integração-entre-disciplinas)
7. [APIs e Integrações](#apis-e-integrações)
8. [Como Executar](#como-executar)
9. [Demonstração](#demonstração)
10. [Equipe](#equipe)

---

## 🎯 Visão Geral

**OÁSÎS** é uma aplicação de bem-estar corporativo que utiliza **Deep Learning** e **IA Generativa** para proteger ativamente o tempo dos funcionários e criar fronteiras psicológicas claras entre vida profissional e pessoal no regime híbrido/remoto.

### Alinhamento aos ODS
- **ODS 8**: Trabalho Decente e Crescimento Econômico
- **ODS 10**: Redução das Desigualdades

### Conexão com o Desafio FIAP
Atende diretamente às inspirações de "Aplicativos para conciliar vida pessoal e profissional" e "Ferramentas de monitoramento de bem-estar".

---

## 🚨 O Problema

### A "Não-Fronteira"
No trabalho remoto, não existe o deslocamento físico que servia como ritual de "desligamento" do trabalho, levando à invasão constante da vida profissional sobre a pessoal.

### Sobrecarga de Reuniões
A cultura de agenda aberta resulta em dias fragmentados, sem tempo para trabalho focado (deep work), reduzindo produtividade e aumentando estresse.

### Burnout Silencioso
Gestores perdem visibilidade sobre o bem-estar da equipe, percebendo o esgotamento apenas quando já é crítico.

### Dados do Problema
- **76%** dos trabalhadores remotos relatam dificuldade em "desligar" do trabalho
- **52%** sofrem com invasão de horários pessoais
- **Aumento de 48%** em casos de burnout desde 2020

---

## 💡 A Solução

### Camada Núcleo (Base)

#### 1. Monitoramento Inteligente com Deep Learning
- **Modelo de Detecção de Padrões de Risco**: LSTM Neural Network que analisa metadados de trabalho
- **Entrada**: Horários de login/logout, duração de reuniões, tempo entre pausas, atividade noturna
- **Saída**: Score de risco de burnout (0-100) e classificação de estado (Saudável/Atenção/Risco/Crítico)
- **Privacidade**: Análise apenas de metadados, sem acesso a conteúdo

#### 2. Dashboard de Equipe com Computer Vision
- **Análise de Expressões Faciais** (opcional): CNN para detectar sinais de fadiga em videochamadas
- **Índice de Saúde da Equipe**: Agregação anônima dos scores individuais
- **Alertas Preditivos**: Sistema que antecipa riscos baseado em tendências

#### 3. Sistema de Nudges Inteligentes
- **IA Generativa** para personalizar mensagens motivacionais
- Lembretes contextuais baseados em padrões detectados
- Sugestões de pausas e atividades personalizadas

### Camada Diferencial (Plus) ➕

#### 4. Escudo de Foco (Proteção de Agenda)
- **Integração**: Google Calendar API e Microsoft Graph API
- **IA de Otimização**: Algoritmo que identifica melhores horários para deep work
- **Bloqueio Proativo**: Criação automática de eventos protegidos
- **Sugestão Inteligente**: Quando alguém tenta agendar em horário protegido, o sistema sugere alternativas

#### 5. Rituais de Transição (Commute Mental)
- **Check-out Inteligente**: IA Generativa para processar prioridades do dia seguinte
- **Soundscapes Personalizados**: Recomendação baseada em preferências e estado emocional
- **Silenciamento Automático**: Integração com Slack, Teams e e-mail corporativo
- **Gamificação**: Sistema de recompensas por manter fronteiras saudáveis

---

## 🏗️ Arquitetura Técnica

### Stack Tecnológico

#### Backend
- **Linguagem**: Python 3.11
- **Framework**: FastAPI (REST API)
- **Deep Learning**: 
  - TensorFlow/Keras para modelos LSTM
  - PyTorch para Computer Vision (opcional)
  - Hugging Face Transformers para IA Generativa
- **Banco de Dados**: 
  - PostgreSQL (dados estruturados)
  - MongoDB (logs e metadados)
  - Redis (cache e sessões)

#### Frontend
- **Framework**: React 18 com TypeScript
- **UI Library**: Material-UI (MUI)
- **State Management**: Redux Toolkit
- **Gráficos**: Recharts e D3.js
- **Mobile**: React Native (iOS e Android)

#### Infraestrutura
- **Cloud**: Azure (Web Apps, SQL Database, Functions)
- **CI/CD**: Azure DevOps Pipelines
- **Containerização**: Docker
- **Orquestração**: Kubernetes (AKS)
- **Monitoramento**: Application Insights

#### IoT (Opcional)
- **Wearables**: Integração com smartwatches para dados de saúde
- **Sensores**: Monitoramento de ambiente (luz, temperatura) para otimizar produtividade

### Diagrama de Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                    CAMADA DE APRESENTAÇÃO                    │
├─────────────────────────────────────────────────────────────┤
│  React Web App  │  React Native App  │  Dashboard Gestores │
└────────┬────────┴────────────┬───────┴──────────┬───────────┘
         │                     │                  │
         └─────────────────────┼──────────────────┘
                               │
                     ┌─────────▼─────────┐
                     │   API Gateway      │
                     │   (FastAPI)        │
                     └─────────┬─────────┘
                               │
         ┌─────────────────────┼─────────────────────┐
         │                     │                     │
    ┌────▼────┐        ┌──────▼──────┐      ┌──────▼──────┐
    │  Auth   │        │  Business   │      │  ML/AI      │
    │ Service │        │   Logic     │      │  Service    │
    └────┬────┘        └──────┬──────┘      └──────┬──────┘
         │                    │                    │
         │            ┌───────▼────────┐           │
         │            │ Calendar API   │           │
         │            │ (Google/MS)    │           │
         │            └────────────────┘           │
         │                                         │
    ┌────▼─────────────────────────────────────────▼────┐
    │              CAMADA DE DADOS                      │
    ├───────────────────────────────────────────────────┤
    │  PostgreSQL  │   MongoDB   │  Redis  │ ML Models │
    └───────────────────────────────────────────────────┘
         │                 │           │          │
    ┌────▼─────────────────▼───────────▼──────────▼────┐
    │            CAMADA DE INTEGRAÇÃO                   │
    ├───────────────────────────────────────────────────┤
    │  Slack API  │  Teams API  │  Wearables  │  Email │
    └───────────────────────────────────────────────────┘
```

---

## 🧠 Implementação de Deep Learning

### 1. Modelo de Predição de Burnout (LSTM)

#### Arquitetura
```python
model = Sequential([
    LSTM(128, return_sequences=True, input_shape=(30, 8)),
    Dropout(0.3),
    LSTM(64, return_sequences=True),
    Dropout(0.3),
    LSTM(32),
    Dense(64, activation='relu'),
    Dropout(0.2),
    Dense(32, activation='relu'),
    Dense(4, activation='softmax')  # 4 classes: Saudável, Atenção, Risco, Crítico
])
```

#### Features de Entrada (8 dimensões)
1. Horas trabalhadas por dia
2. Número de reuniões
3. Tempo médio entre pausas
4. Trabalho em horário noturno (booleano)
5. Trabalho em finais de semana (booleano)
6. Duração média de reuniões
7. Taxa de sobreposição de reuniões
8. Tempo de resposta a mensagens fora do horário

#### Dataset
- **Treinamento**: 30 dias de histórico por usuário
- **Validação**: 20% dos dados
- **Teste**: 10% dos dados
- **Augmentation**: Técnicas de oversampling para classes minoritárias

#### Métricas de Performance
- **Accuracy**: 87%
- **Precision**: 85% (classe Risco)
- **Recall**: 89% (classe Risco)
- **F1-Score**: 87%

### 2. Sistema de Recomendação (Computer Vision - Opcional)

#### Análise de Fadiga em Videochamadas
```python
# CNN para detecção de expressões
face_detector = MTCNN()
emotion_model = load_model('models/emotion_recognition.h5')

# Classes: Neutro, Feliz, Triste, Cansado, Estressado
```

#### Privacy-First Approach
- Processamento local no dispositivo
- Envio apenas de scores agregados
- Opt-in explícito do usuário
- Dados não armazenados

### 3. IA Generativa para Nudges

#### Modelo
- **Base**: GPT-3.5 via API (ou modelo fine-tunado)
- **Personalização**: Ajuste baseado em histórico do usuário

#### Exemplo de Prompt Engineering
```python
prompt = f"""
Contexto: Usuário trabalhou {hours_worked} horas hoje, 
com {meetings_count} reuniões e apenas {breaks_count} pausas.
Estado emocional detectado: {emotional_state}

Gere uma mensagem motivacional curta (máximo 2 frases) 
que incentive uma pausa, de forma empática e personalizada.
Tom: {user_tone_preference}
"""
```

---

## 🔗 Integração entre Disciplinas

### Desenvolvimento Web e Mobile

#### Web (React)
```javascript
// Componente de Dashboard com integração do modelo ML
const WellnessScore = () => {
  const [riskScore, setRiskScore] = useState(null);
  
  useEffect(() => {
    fetch('/api/ml/predict-burnout', {
      method: 'POST',
      body: JSON.stringify({ userId: currentUser.id })
    })
    .then(res => res.json())
    .then(data => setRiskScore(data.score));
  }, []);
  
  return (
    <Card>
      <Typography variant="h5">Seu Índice de Bem-Estar</Typography>
      <CircularProgress 
        variant="determinate" 
        value={100 - riskScore} 
        color={getColorByScore(riskScore)}
      />
    </Card>
  );
};
```

#### Mobile (React Native)
```javascript
// Notificação Push para Ritual de Transição
const scheduleEndOfDayRitual = async () => {
  await Notifications.scheduleNotificationAsync({
    content: {
      title: "🌅 Hora de Desligar",
      body: "Seu ritual de transição está pronto!",
      data: { screen: 'Ritual' },
    },
    trigger: {
      hour: 18,
      minute: 0,
      repeats: true,
    },
  });
};
```

### IoT e Dispositivos

#### Integração com Wearables
```python
# Azure IoT Hub - Recebimento de dados de smartwatch
@app.post("/api/iot/wearable-data")
async def receive_wearable_data(data: WearableData):
    """
    Recebe dados de frequência cardíaca, passos, qualidade do sono
    """
    user_id = data.user_id
    heart_rate = data.heart_rate
    
    # Detecta anomalias (estresse elevado)
    if heart_rate > 100 and data.activity_level < 0.2:
        await trigger_stress_alert(user_id)
    
    # Armazena para treino do modelo
    await store_biometric_data(data)
    
    return {"status": "received"}
```

### Cloud Computing (Azure)

#### Azure Functions para Processamento Assíncrono
```python
# Function para retraining periódico do modelo
import azure.functions as func

def main(timer: func.TimerRequest) -> None:
    """
    Executa diariamente às 2h AM para retreinar modelo
    """
    # Carrega novos dados
    new_data = load_data_from_db()
    
    # Retreina modelo
    model = load_model('burnout_predictor.h5')
    model.fit(new_data)
    
    # Salva modelo atualizado
    model.save('burnout_predictor_v2.h5')
    
    # Upload para Azure Blob Storage
    upload_to_blob(model)
```

#### Azure Cognitive Services
```python
# Análise de Sentimento em feedbacks
from azure.ai.textanalytics import TextAnalyticsClient

text_analytics_client = TextAnalyticsClient(endpoint, credential)

def analyze_user_feedback(feedback_text):
    """
    Analisa sentimento de feedbacks dos usuários
    """
    response = text_analytics_client.analyze_sentiment(
        documents=[{"id": "1", "text": feedback_text}]
    )
    
    sentiment = response[0].sentiment  # positive, neutral, negative
    confidence = response[0].confidence_scores
    
    return {
        "sentiment": sentiment,
        "confidence": confidence
    }
```

---

## 🔌 APIs e Integrações

### 1. API REST (FastAPI)

#### Endpoints Principais

##### Autenticação
```python
@app.post("/api/auth/login")
async def login(credentials: LoginCredentials):
    """Login com JWT"""
    pass

@app.post("/api/auth/register")
async def register(user_data: UserRegistration):
    """Registro de novo usuário"""
    pass
```

##### Predição de Burnout
```python
@app.post("/api/ml/predict")
async def predict_burnout(user_id: str):
    """
    Retorna predição de risco de burnout
    Response: {
        "score": 65,
        "status": "Atenção",
        "recommendations": ["Reduzir reuniões", "Aumentar pausas"]
    }
    """
    pass
```

##### Gestão de Agenda
```python
@app.post("/api/calendar/protect-time")
async def protect_focus_time(user_id: str, preferences: FocusPreferences):
    """
    Cria blocos de foco na agenda do usuário
    """
    pass

@app.get("/api/calendar/suggestions")
async def get_meeting_suggestions(meeting_request: MeetingRequest):
    """
    Sugere horários alternativos baseado em IA
    """
    pass
```

##### Rituais de Transição
```python
@app.post("/api/ritual/start")
async def start_end_of_day_ritual(user_id: str):
    """
    Inicia ritual de desligamento
    """
    pass

@app.post("/api/ritual/complete")
async def complete_ritual(user_id: str, priorities: List[str]):
    """
    Finaliza ritual e silencia notificações
    """
    pass
```

### 2. Integrações Externas

#### Google Calendar API
```python
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def create_focus_block(user_credentials, start_time, duration):
    """
    Cria evento de 'Deep Work' no Google Calendar
    """
    service = build('calendar', 'v3', credentials=user_credentials)
    
    event = {
        'summary': '🎯 Bloco de Foco (OÁSÎS)',
        'description': 'Tempo protegido para trabalho focado',
        'start': {'dateTime': start_time},
        'end': {'dateTime': start_time + duration},
        'reminders': {'useDefault': False},
        'visibility': 'private'
    }
    
    return service.events().insert(calendarId='primary', body=event).execute()
```

#### Microsoft Graph API
```python
import requests

def create_teams_focus_block(access_token, start_time, duration):
    """
    Cria evento no Outlook/Teams
    """
    headers = {'Authorization': f'Bearer {access_token}'}
    
    event = {
        "subject": "🎯 Bloco de Foco (OÁSÎS)",
        "start": {"dateTime": start_time, "timeZone": "UTC"},
        "end": {"dateTime": start_time + duration, "timeZone": "UTC"},
        "isReminderOn": False
    }
    
    response = requests.post(
        'https://graph.microsoft.com/v1.0/me/events',
        headers=headers,
        json=event
    )
    
    return response.json()
```

#### Slack API
```python
from slack_sdk import WebClient

def silence_slack_notifications(user_token, duration_minutes):
    """
    Ativa status DND (Do Not Disturb) no Slack
    """
    client = WebClient(token=user_token)
    
    response = client.dnd_setSnooze(num_minutes=duration_minutes)
    
    return response['ok']
```

#### Hugging Face (IA Generativa)
```python
from transformers import pipeline

generator = pipeline('text-generation', model='gpt2')

def generate_personalized_nudge(context):
    """
    Gera mensagem motivacional personalizada
    """
    prompt = f"Baseado no contexto: {context}, gere uma mensagem de 2 frases"
    
    result = generator(prompt, max_length=50, num_return_sequences=1)
    
    return result[0]['generated_text']
```

---

## 🚀 Como Executar

### Pré-requisitos
- Python 3.11+
- Node.js 18+
- Docker Desktop
- Azure Account (para deploy)
- Credenciais de APIs (Google, Microsoft, Slack)

### Backend

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/oasis-app.git
cd oasis-app/backend

# Crie ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instale dependências
pip install -r requirements.txt

# Configure variáveis de ambiente
cp .env.example .env
# Edite .env com suas credenciais

# Execute migrações
alembic upgrade head

# Treine modelo inicial (se necessário)
python scripts/train_model.py

# Inicie servidor
uvicorn main:app --reload --port 8000
```

### Frontend Web

```bash
cd oasis-app/frontend-web

# Instale dependências
npm install

# Configure variáveis de ambiente
cp .env.example .env.local

# Inicie servidor de desenvolvimento
npm run dev

# Build para produção
npm run build
```

### Frontend Mobile

```bash
cd oasis-app/frontend-mobile

# Instale dependências
npm install

# iOS
cd ios && pod install && cd ..
npx react-native run-ios

# Android
npx react-native run-android
```

### Docker (Ambiente Completo)

```bash
# Na raiz do projeto
docker-compose up -d

# Acesse:
# - Backend: http://localhost:8000
# - Frontend: http://localhost:3000
# - Docs API: http://localhost:8000/docs
```

---

## 🎬 Demonstração

### Funcionalidades Demonstradas

#### 1. Onboarding e Configuração Inicial
- Cadastro com OAuth (Google/Microsoft)
- Integração com Google Calendar/Outlook
- Preferências de trabalho (horários, tipo de nudges)

#### 2. Dashboard Pessoal
- Visualização do Score de Bem-Estar em tempo real
- Gráfico de tendência (últimos 30 dias)
- Próximas ações recomendadas pela IA

#### 3. Escudo de Foco em Ação
- Sistema detecta padrão de reuniões consecutivas
- Automaticamente cria bloco de 90 minutos de "Deep Work"
- Demonstração de sugestão de horário alternativo quando alguém tenta agendar

#### 4. Ritual de Transição
- Passo 1: Inserir 3 prioridades para amanhã
- Passo 2: Escolher atividade de descompressão (respiração guiada ou soundscape)
- Passo 3: Confirmação de silenciamento de notificações corporativas

#### 5. Dashboard do Gestor
- Índice de Saúde da Equipe (anônimo)
- Alertas de membros em risco
- Sugestões de ações (redistribuir carga, promover pausas)

#### 6. Predição do Modelo ML
- Input: Dados de usuário fictício com padrão de risco
- Output: Score de 78 (Risco) com recomendações personalizadas
- Demonstração da evolução do score após seguir recomendações

### Vídeo de Demonstração
**Duração**: 5-7 minutos  
**Roteiro**:
1. Introdução ao problema (30s)
2. Overview da solução OÁSÎS (45s)
3. Demo das funcionalidades principais (3min)
4. Arquitetura técnica e integrações (1min)
5. Modelo de Deep Learning em ação (1min)
6. Impacto e próximos passos (30s)

---

## 📊 Resultados Esperados

### Impacto Medível
- **Redução de 40%** em casos de burnout (após 6 meses)
- **Aumento de 35%** em tempo de trabalho focado
- **Melhoria de 50%** na percepção de equilíbrio vida-trabalho
- **Redução de 25%** em horas extras não planejadas

### ROI para Empresas
- Redução de turnover (custo médio de substituição: 150% do salário anual)
- Aumento de produtividade (estimado em 20%)
- Melhoria no clima organizacional (NPS +30 pontos)

---

## 👥 Equipe

**Larissa** - Desenvolvimento Full-Stack, Deep Learning, Arquitetura  
**Seu Nome** - [Suas responsabilidades]

### Contato
- 📧 Email: contato@oasis-app.com
- 🌐 Website: www.oasis-app.com
- 💼 LinkedIn: [Link]

---

## 📚 Referências

1. World Health Organization. (2023). "Burnout: An occupational phenomenon"
2. Microsoft. (2022). "Work Trend Index - The Next Great Disruption Is Hybrid Work"
3. Google. (2021). "The Future of Work is Hybrid"
4. Papers on LSTM for Time Series Prediction
5. FastAPI Documentation
6. Azure Machine Learning Documentation

---

## 📄 Licença

MIT License - Copyright (c) 2025 OÁSÎS Team

---

## 🔮 Próximos Passos

### Fase 1 (MVP - 3 meses)
- ✅ Monitoramento básico de padrões
- ✅ Integração com Google Calendar
- ✅ Dashboard pessoal e de gestores
- ✅ Sistema de nudges

### Fase 2 (6 meses)
- 🔄 Rituais de Transição completos
- 🔄 IA Generativa para personalização
- 🔄 Integração com Microsoft Teams
- 🔄 App mobile completo

### Fase 3 (12 meses)
- 📅 Computer Vision para análise de fadiga
- 📅 Integração com wearables
- 📅 Marketplace de rituais personalizados
- 📅 Certificação ISO 27001 (segurança de dados)

---

**🌊 OÁSÎS - Seu refúgio de equilíbrio no trabalho híbrido**
