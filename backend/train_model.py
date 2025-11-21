"""
Script de Treinamento do Modelo LSTM
Execute: python train_model.py
"""

import numpy as np
import os

# Verificar se TensorFlow está disponível
try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import LSTM, Dense, Dropout
    from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
    from sklearn.model_selection import train_test_split
    import matplotlib.pyplot as plt
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
    print(" TensorFlow não disponível - instale com: pip install tensorflow")
    exit(1)

# Criar pasta de modelos
os.makedirs("models", exist_ok=True)

print("=" * 60)
print(" OÁSÎS - TREINAMENTO DO MODELO LSTM")
print("=" * 60)

# ==================== GERAÇÃO DE DATASET ====================

def generate_dataset(n_samples=5000, sequence_length=30, n_features=8):
    """
    Gera dataset sintético para treinamento
    
    Classes:
    0 - Saudável (40%)
    1 - Atenção (30%)
    2 - Risco (20%)
    3 - Crítico (10%)
    """
    print("\n📊 Gerando dataset sintético...")
    
    X = []
    y = []
    
    for _ in range(n_samples):
        # Escolhe classe aleatória
        class_id = np.random.choice([0, 1, 2, 3], p=[0.4, 0.3, 0.2, 0.1])
        
        # Gera sequência de 30 dias
        sequence = []
        
        for day in range(sequence_length):
            if class_id == 0:  # Saudável
                features = [
                    np.random.uniform(6, 8),        # horas_trabalhadas
                    np.random.randint(2, 5),        # reunioes
                    np.random.uniform(90, 120),     # tempo_pausas
                    0,                               # trabalho_noturno
                    0,                               # fim_de_semana
                    np.random.uniform(30, 45),      # duracao_reunioes
                    np.random.uniform(0, 0.1),      # sobreposicao
                    np.random.uniform(60, 120)      # tempo_resposta
                ]
            elif class_id == 1:  # Atenção
                features = [
                    np.random.uniform(8, 9.5),
                    np.random.randint(5, 7),
                    np.random.uniform(60, 90),
                    np.random.choice([0, 1], p=[0.7, 0.3]),
                    np.random.choice([0, 1], p=[0.8, 0.2]),
                    np.random.uniform(45, 60),
                    np.random.uniform(0.1, 0.3),
                    np.random.uniform(30, 60)
                ]
            elif class_id == 2:  # Risco
                features = [
                    np.random.uniform(9.5, 11),
                    np.random.randint(7, 10),
                    np.random.uniform(30, 60),
                    np.random.choice([0, 1], p=[0.4, 0.6]),
                    np.random.choice([0, 1], p=[0.5, 0.5]),
                    np.random.uniform(60, 90),
                    np.random.uniform(0.3, 0.5),
                    np.random.uniform(10, 30)
                ]
            else:  # Crítico
                features = [
                    np.random.uniform(11, 14),
                    np.random.randint(10, 15),
                    np.random.uniform(10, 30),
                    np.random.choice([0, 1], p=[0.2, 0.8]),
                    np.random.choice([0, 1], p=[0.3, 0.7]),
                    np.random.uniform(90, 120),
                    np.random.uniform(0.5, 0.8),
                    np.random.uniform(5, 10)
                ]
            
            sequence.append(features)
        
        X.append(sequence)
        
        # One-hot encode
        label = [0, 0, 0, 0]
        label[class_id] = 1
        y.append(label)
    
    X = np.array(X)
    y = np.array(y)
    
    print(f"✅ Dataset gerado: {X.shape}")
    print(f"   - Amostras: {n_samples}")
    print(f"   - Sequência: {sequence_length} dias")
    print(f"   - Features: {n_features}")
    print(f"   - Classes: 4 (Saudável, Atenção, Risco, Crítico)")
    
    return X, y

# ==================== CONSTRUÇÃO DO MODELO ====================

def build_model(sequence_length=30, n_features=8):
    """Constrói arquitetura LSTM"""
    print("\n🏗️ Construindo modelo LSTM...")
    
    model = Sequential([
        # Camada LSTM 1
        LSTM(128, return_sequences=True, input_shape=(sequence_length, n_features)),
        Dropout(0.3),
        
        # Camada LSTM 2
        LSTM(64, return_sequences=True),
        Dropout(0.3),
        
        # Camada LSTM 3
        LSTM(32),
        
        # Camadas Densas
        Dense(64, activation='relu'),
        Dropout(0.2),
        Dense(32, activation='relu'),
        
        # Saída
        Dense(4, activation='softmax')
    ])
    
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss='categorical_crossentropy',
        metrics=['accuracy', 'precision', 'recall']
    )
    
    print(" Modelo construído")
    print(f"   - Total de parâmetros: {model.count_params():,}")
    
    model.summary()
    
    return model

# ==================== TREINAMENTO ====================

def train_model(model, X_train, y_train, X_val, y_val, epochs=50):
    """Treina o modelo"""
    print("\n Iniciando treinamento...")
    
    # Callbacks
    early_stop = EarlyStopping(
        monitor='val_loss',
        patience=10,
        restore_best_weights=True,
        verbose=1
    )
    
    checkpoint = ModelCheckpoint(
        'models/burnout_predictor.h5',
        monitor='val_accuracy',
        save_best_only=True,
        verbose=1
    )
    
    # Treinamento
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=epochs,
        batch_size=32,
        callbacks=[early_stop, checkpoint],
        verbose=1
    )
    
    return history

# ==================== AVALIAÇÃO ====================

def evaluate_model(model, X_test, y_test):
    """Avalia o modelo"""
    print("\n Avaliando modelo...")
    
    results = model.evaluate(X_test, y_test, verbose=0)
    
    print("\n" + "=" * 60)
    print(" RESULTADOS FINAIS")
    print("=" * 60)
    print(f"Loss: {results[0]:.4f}")
    print(f"Accuracy: {results[1]:.4f} ({results[1]*100:.2f}%)")
    print(f"Precision: {results[2]:.4f}")
    print(f"Recall: {results[3]:.4f}")
    
    # Calcula F1-Score
    f1 = 2 * (results[2] * results[3]) / (results[2] + results[3])
    print(f"F1-Score: {f1:.4f}")
    print("=" * 60)
    
    return results

# ==================== VISUALIZAÇÃO ====================

def plot_history(history):
    """Plota histórico de treinamento"""
    print("\n Gerando gráficos...")
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Loss
    axes[0].plot(history.history['loss'], label='Train Loss')
    axes[0].plot(history.history['val_loss'], label='Val Loss')
    axes[0].set_title('Loss ao Longo do Treinamento')
    axes[0].set_xlabel('Época')
    axes[0].set_ylabel('Loss')
    axes[0].legend()
    axes[0].grid(True)
    
    # Accuracy
    axes[1].plot(history.history['accuracy'], label='Train Accuracy')
    axes[1].plot(history.history['val_accuracy'], label='Val Accuracy')
    axes[1].set_title('Accuracy ao Longo do Treinamento')
    axes[1].set_xlabel('Época')
    axes[1].set_ylabel('Accuracy')
    axes[1].legend()
    axes[1].grid(True)
    
    plt.tight_layout()
    plt.savefig('models/training_history.png', dpi=300, bbox_inches='tight')
    print(" Gráficos salvos em: models/training_history.png")

# ==================== MAIN ====================

if __name__ == "__main__":
    # Gerar dataset
    X, y = generate_dataset(n_samples=5000)
    
    # Split
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.33, random_state=42, stratify=y_temp
    )
    
    print(f"\n Split de dados:")
    print(f"   - Treino: {len(X_train)} amostras")
    print(f"   - Validação: {len(X_val)} amostras")
    print(f"   - Teste: {len(X_test)} amostras")
    
    # Construir modelo
    model = build_model()
    
    # Treinar
    history = train_model(model, X_train, y_train, X_val, y_val, epochs=50)
    
    # Avaliar
    results = evaluate_model(model, X_test, y_test)
    
    # Plotar
    plot_history(history)
    
    print("\n Treinamento concluído!")
    print(" Modelo salvo em: models/burnout_predictor.h5")
    print("\n OÁSÎS está pronto para uso!")