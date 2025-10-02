"""
STC Trading - Candles Storage System
Almacena y recupera velas históricas en CSV
"""
import os
import csv
import json
from datetime import datetime
from typing import List, Dict, Any
import pandas as pd

class CandlesStore:
    def __init__(self, csv_dir: str = "data"):
        self.csv_dir = csv_dir
        os.makedirs(csv_dir, exist_ok=True)
        
    def get_csv_filename(self, symbol: str, timeframe: str) -> str:
        """Genera nombre de archivo CSV para símbolo y timeframe"""
        return os.path.join(self.csv_dir, f"{symbol}_{timeframe}.csv")
    
    def store_batch(self, symbol: str, timeframe: str, candles: List[Dict]) -> Dict[str, Any]:
        """Almacena lote de velas en CSV"""
        if not candles:
            return {"inserted": 0, "size": 0}
            
        filename = self.get_csv_filename(symbol, timeframe)
        
        # Preparar datos para CSV
        rows = []
        for candle in candles:
            if isinstance(candle, dict):
                row = {
                    'timestamp': candle.get('time', 0),
                    'datetime': datetime.fromtimestamp(candle.get('time', 0)).isoformat(),
                    'open': candle.get('open', 0),
                    'high': candle.get('high', 0),
                    'low': candle.get('low', 0),
                    'close': candle.get('close', 0),
                    'volume': candle.get('volume', 0),
                    'symbol': symbol,
                    'timeframe': timeframe
                }
                rows.append(row)
        
        # Escribir al CSV
        file_exists = os.path.exists(filename)
        with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['timestamp', 'datetime', 'open', 'high', 'low', 'close', 'volume', 'symbol', 'timeframe']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            if not file_exists:
                writer.writeheader()
            
            writer.writerows(rows)
        
        return {"inserted": len(rows), "size": len(rows)}
    
    def read_last(self, symbol: str, timeframe: str, limit: int = 200) -> List[Dict]:
        """Lee las últimas N velas del CSV"""
        filename = self.get_csv_filename(symbol, timeframe)
        
        if not os.path.exists(filename):
            return []
        
        try:
            df = pd.read_csv(filename)
            df = df.sort_values('timestamp').tail(limit)
            
            candles = []
            for _, row in df.iterrows():
                candle = {
                    'time': int(row['timestamp']),
                    'open': float(row['open']),
                    'high': float(row['high']),
                    'low': float(row['low']),
                    'close': float(row['close']),
                    'volume': float(row.get('volume', 0))
                }
                candles.append(candle)
            
            return candles
        except Exception as e:
            print(f"Error leyendo CSV {filename}: {e}")
            return []

def store_batch(symbol: str, timeframe: str, candles: List[Dict]) -> Dict[str, Any]:
    """Función de conveniencia para almacenar velas"""
    store = CandlesStore()
    return store.store_batch(symbol, timeframe, candles)

def read_last(symbol: str, timeframe: str, limit: int = 200) -> List[Dict]:
    """Función de conveniencia para leer velas"""
    store = CandlesStore()
    return store.read_last(symbol, timeframe, limit)