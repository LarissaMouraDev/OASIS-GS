"""
OÁSÎS - Modelo de Predição de Burnout
LSTM Neural Network
"""

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.preprocessing import StandardScaler
from typing import Dict, List, Tuple
import joblib
import os
from datetime import datetime, timedelta

class BurnoutPredictor:
    """
    Modelo LSTM para predição de risco de burnout
    """
    
    def __init__(self, model_path: str = "models/burnout_predictor.h5"):
        self.model_path = model_path
        self.model = None
        self.scaler = StandardScaler()
        self.sequence_length = 30  # 30 dias
        self.n_features = 8
        
        # Criar diretório de modelos se não existir
        os.makedirs("models", exist_ok=True)
        
    def build_model(self):
        """Constrói arquitetura do modelo LSTM"""
        model = Sequential([
            # Primeira camada LSTM
            LSTM(128, return_sequences=True, 
                 input_shape=(self.sequence_length, self.n_features)),
            Dropout(0.3),
            
            # Segunda camada LSTM
            LSTM(64, return_sequences=True),
            Dropout(0.3),
            
            # Terceira camada LSTM
            LSTM(32),
            
            # Camadas densas
            Dense(64, activation='relu'),
            Dropout(0.2),
            Dense(32, activation='relu'),
            
            # Saída (4 classes)
            Dense(4, activation='softmax')
        ])
        
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        self.model = model
        print("✅ Modelo construído com sucesso")
        return model
    
    def generate_synthetic_data(self, n_samples: int = 1000):
        """Gera dados sintéticos para treinamento"""
        X = []
        y = []
        
        for _ in range(n_samples):
            # Gera sequência de 30 dias
            sequence = []
            
            # Define padrão (0=Saudável, 1=Atenção, 2=Risco, 3=Crítico)
            pattern = np.random.choice([0, 1, 2, 3], p=[0.4, 0.3, 0.2, 0.1])
            
            for day in range(30):
                if pattern == 0:  # Saudável
                    features = [
                        np.random.uniform(7, 8),      # horas
                        np.random.randint(3, 5),      # reuniões
                        np.random.uniform(90, 120),   # tempo pausas
                        0,                            # night work
                        0,                            # weekend work
                        np.random.uniform(30, 45),    # duração reuniões
                        np.random.uniform(0, 0.1),    # sobreposição
                        np.random.uniform(60, 120)    # response time
                    ]
                elif pattern == 1:  # Atenção
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
                elif pattern == 2:  # Risco
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
            label[pattern] = 1
            y.append(label)
        
        return np.array(X), np.array(y)
    
    def train(self, X_train, y_train, X_val, y_val, epochs=30, batch_size=32):
        """Treina o modelo"""
        if self.model is None:
            self.build_model()
        
        # Callbacks
        early_stop = EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True
        )
        
        checkpoint = ModelCheckpoint(
            self.model_path,
            monitor='val_accuracy',
            save_best_only=True
        )
        
        # Treinamento
        history = self.model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=epochs,
            batch_size=batch_size,
            callbacks=[early_stop, checkpoint],
            verbose=1
        )
        
        # Salvar scaler
        joblib.dump(self.scaler, 'models/scaler.pkl')
        
        return history
    
    def predict(self, features: np.ndarray) -> Dict:
        """Faz predição"""
        if self.model is None:
            self.load_model()
        
        # Simula histórico de 30 dias
        sequence = []
        for i in range(30):
            noise = np.random.normal(0, 0.05, 8)
            day_features = features + noise
            sequence.append(day_features)
        
        sequence = np.array([sequence])
        
        # Predição
        prediction = self.model.predict(sequence, verbose=0)
        probs = prediction[0]
        predicted_class = np.argmax(probs)
        confidence = float(probs[predicted_class])
        
        # Converte para score
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
        if os.path.exists(self.model_path):
            self.model = load_model(self.model_path)
            print(f" Modelo carregado")
            
            if os.path.exists('models/scaler.pkl'):
                self.scaler = joblib.load('models/scaler.pkl')
        else:
            print(" Modelo não encontrado, construindo novo...")
            self.build_model()
            # Treina com dados sintéticos
            self._train_initial_model()
    
    def _train_initial_model(self):
        """Treina modelo inicial"""
        print(" Gerando dados sintéticos...")
        X, y = self.generate_synthetic_data(n_samples=1000)
        
        # Split
        train_size = int(0.8 * len(X))
        X_train, X_val = X[:train_size], X[train_size:]
        y_train, y_val = y[:train_size], y[train_size:]
        
        print(" Treinando modelo...")
        self.train(X_train, y_train, X_val, y_val, epochs=20)
        print(" Modelo treinado e salvo!")


# Script para treinar modelo inicial
if __name__ == "__main__":
    print(" Iniciando treinamento do OÁSÎS...")
    
    predictor = BurnoutPredictor()
    
    # Gera dados
    print(" Gerando dataset...")
    X, y = predictor.generate_synthetic_data(n_samples=2000)
    
    # Split
    train_size = int(0.7 * len(X))
    val_size = int(0.2 * len(X))
    
    X_train = X[:train_size]
    y_train = y[:train_size]
    X_val = X[train_size:train_size + val_size]
    y_val = y[train_size:train_size + val_size]
    X_test = X[train_size + val_size:]
    y_test = y[train_size + val_size:]
    
    print(f"Train: {len(X_train)}, Val: {len(X_val)}, Test: {len(X_test)}")
    
    # Treina
    history = predictor.train(X_train, y_train, X_val, y_val, epochs=30)
    
    # Avalia
    print("\n Avaliando...")
    loss, acc = predictor.model.evaluate(X_test, y_test, verbose=0)
    print(f" Test Accuracy: {acc:.4f}")
    print(f" Test Loss: {loss:.4f}")
    
    print("\n Treinamento concluído!")