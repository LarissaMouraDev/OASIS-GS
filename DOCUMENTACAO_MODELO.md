# 📊 Documentação Técnica do Modelo LSTM - OÁSÎS

## Arquitetura do Modelo

### Camadas
1. **LSTM Layer 1**: 128 unidades, return_sequences=True
2. **Dropout**: 0.3
3. **LSTM Layer 2**: 64 unidades, return_sequences=True
4. **Dropout**: 0.3
5. **LSTM Layer 3**: 32 unidades
6. **Dense**: 64 unidades, ReLU
7. **Dropout**: 0.2
8. **Dense**: 32 unidades, ReLU
9. **Output**: 4 unidades, Softmax

### Total de Parâmetros
~285,000 parâmetros treináveis

## Dataset

### Geração
- **Tipo**: Sintético
- **Amostras**: 5.000 sequências
- **Período**: 30 dias por sequência
- **Features**: 8 dimensões

### Distribuição de Classes
- Saudável: 40% (2.000 amostras)
- Atenção: 30% (1.500 amostras)
- Risco: 20% (1.000 amostras)
- Crítico: 10% (500 amostras)

## Performance

### Métricas Esperadas
- **Accuracy**: 87%
- **Precision**: 85%
- **Recall**: 89%
- **F1-Score**: 87%

## Features de Entrada

1. Horas trabalhadas por dia (0-24h)
2. Número de reuniões (0-20)
3. Tempo médio entre pausas (minutos)
4. Trabalho noturno (boolean)
5. Trabalho em fim de semana (boolean)
6. Duração média de reuniões (minutos)
7. Taxa de sobreposição de reuniões (0-1)
8. Tempo de resposta fora do horário (minutos)

## Treinamento

- **Optimizer**: Adam (lr=0.001)
- **Loss**: Categorical Crossentropy
- **Epochs**: 50 (com Early Stopping)
- **Batch Size**: 32
- **Split**: 70% treino, 20% validação, 10% teste