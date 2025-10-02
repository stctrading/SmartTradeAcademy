# STC Trading System - Complete README

Sistema completo de trading automatizado para IQ Option con dashboard web profesional y gráficos en tiempo real.

## 🚀 Características Principales

- **Dashboard Web Profesional**: Interface moderna y responsive
- **Gráficos en Tiempo Real**: TradingView LightweightCharts integrados  
- **Trading Automatizado**: Conexión directa con IQ Option API
- **Símbolos OTC 24/7**: EURUSD-OTC, GBPUSD-OTC, USDJPY-OTC, EURJPY-OTC
- **API REST Completa**: Endpoints para balance, símbolos, velas y órdenes
- **Almacenamiento Persistente**: Sistema de velas en CSV
- **CORS Configurado**: Compatible con múltiples orígenes

## 🛠️ Stack Tecnológico

- **Backend**: Python 3.11+ con Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Gráficos**: TradingView LightweightCharts
- **API Trading**: IQ Option API (iqoptionapi)
- **Base de Datos**: CSV + Redis en memoria

## 📦 Instalación Rápida

### 1. Requisitos
- Python 3.11+
- Cuenta IQ Option

### 2. Instalación
```bash
git clone https://github.com/TU_USUARIO/stc-trading-system.git
cd stc-trading-system
pip install -r requirements.txt
```

### 3. Configuración
Edita `.env` con tus credenciales:
```env
IQ_EMAIL=tu_email@gmail.com
IQ_PASSWORD=tu_password
```

### 4. Ejecutar
```bash
# Windows
inicio_manual.bat

# Manual
python iq_client.py
python iq_routes_redis_patch.py  
python dashboard_server.py
```

## 🌐 URLs del Sistema

- **Dashboard**: http://localhost:5001
- **API**: http://localhost:5002  
- **Health**: http://localhost:5002/health

## 📊 Uso del Sistema

1. Abre http://localhost:5001
2. Ingresa credenciales IQ Option
3. Conecta y haz trading con CALL/PUT
4. Gráficos automáticos cada 2 segundos

## ⚠️ Importante

- Solo uso educacional
- Trading conlleva riesgos
- Usar cuenta PRACTICE inicialmente

## 📄 Licencia

MIT License
