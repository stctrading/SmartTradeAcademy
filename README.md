# 🚀 STC Trading System - Sistema IQ Option Completo

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com)
[![Redis](https://img.shields.io/badge/Redis-7+-red.svg)](https://redis.io)
[![IQ Option](https://img.shields.io/badge/IQ%20Option-API-orange.svg)](https://iqoption.com)

## 📋 Descripción

**Sistema de Trading Automatizado** que integra completamente con la API de IQ Option para proporcionar:

- 🔐 **Sesión persistente** con login/logout automático
- 📊 **Símbolos reales** obtenidos dinámicamente de IQ Option 
- 📈 **Velas en tiempo real** sin datos simulados
- 💰 **Saldo actualizado** automáticamente
- 🌐 **Dashboard web** completo e intuitivo
- ⚡ **Redis** para cache y cola de mensajes
- 🔄 **Reconexión automática** ante desconexiones

## 🏗️ Arquitectura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Dashboard     │───▶│   Backend API   │───▶│     Redis       │
│  (puerto 5001)  │    │  (puerto 5002)  │    │  (puerto 6380)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
        │                       │                       ▲
        │                       │                       │
        └───────────────────────┼───────────────────────┘
                                ▼
                    ┌─────────────────┐
                    │   Cliente IQ    │
                    │ (IQ Option API) │
                    └─────────────────┘
```

## 🚀 Instalación Rápida

### 1. Clonar proyecto
```bash
git clone <repository-url>
cd STC_Trading_System
```

### 2. Configurar Python
```bash
# Crear entorno virtual
python -m venv .venv311

# Activar entorno (Windows)
.venv311\Scripts\activate

# Activar entorno (Linux/Mac)
source .venv311/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Configurar Redis
```bash
# Opción A: Docker (Recomendado)
docker-compose up -d

# Opción B: Redis nativo
# Instalar Redis y configurar puerto 6380
```

### 4. Configurar credenciales
```bash
# Editar archivo .env
IQ_EMAIL=tu_email@gmail.com
IQ_PASSWORD=tu_password
IQ_BALANCE_TYPE=PRACTICE
```

### 5. Iniciar sistema
```bash
# Windows
start_iq_system_complete.bat

# Linux/Mac
chmod +x start_iq_system_complete.sh
./start_iq_system_complete.sh
```

### 6. Acceder al dashboard
```
http://localhost:5001
```

## 📁 Estructura del Proyecto

```
STC_Trading_System/
├── 📄 iq_routes_redis_patch.py     # Backend API Flask
├── 📄 iq_client.py                 # Cliente IQ Option
├── 📄 mt5_server.py                # Servidor dashboard
├── 📁 templates/
│   └── dashboard.html              # Dashboard principal
├── 📄 .env                         # Variables de entorno
├── 📄 requirements.txt             # Dependencias Python
├── 📄 docker-compose.yml           # Redis Docker
├── 📄 start_iq_system_complete.bat # Script de inicio
├── 📁 test/
│   ├── test_symbols.py             # Test símbolos
│   └── test_complete_system.py     # Test completo
└── 📁 docs/
    ├── SISTEMA_IQ_COMPLETO.md      # Documentación técnica
    └── GUIA_MIGRACION.html         # Guía de migración
```

## ⚙️ Configuración

### Variables de Entorno (.env)

```env
# Servidor
SERVER_BASE=http://127.0.0.1:5002

# IQ Option
IQ_EMAIL=tu_email@gmail.com
IQ_PASSWORD=tu_password
IQ_BALANCE_TYPE=PRACTICE

# Trading
IQ_SYMBOLS=EURUSD-OTC
IQ_TIMEFRAMES=M5
IQ_PUSH_INTERVAL_SEC=1.0

# Sistema
HTTP_TIMEOUT=4.0
LOG_LEVEL=INFO
REDIS_URL=redis://127.0.0.1:6380/0
```

## 🌐 Endpoints API

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/api/iq/login` | Iniciar sesión IQ Option |
| `POST` | `/api/iq/logout` | Cerrar sesión |
| `GET` | `/api/iq/session` | Verificar sesión activa |
| `GET` | `/api/iq/symbols` | Obtener símbolos disponibles |
| `GET` | `/api/iq/balance` | Obtener saldo actual |
| `POST` | `/api/iq/candles` | Actualizar velas (interno) |
| `POST` | `/api/iq/order` | Enviar orden de trading |
| `GET` | `/api/iq/order_results` | Obtener resultados |

## 🎯 Características

### ✅ Implementado

- **🔐 Sesión persistente**: Login automático y manual
- **📊 Solo datos reales**: Sin símbolos hardcodeados  
- **🌐 Dashboard completo**: Interfaz web moderna
- **⚡ Redis integrado**: Cache y cola de mensajes
- **🔄 Reconexión automática**: Manejo robusto de errores
- **📈 Tiempo real**: Velas y balance actualizados
- **🧪 Testing incluido**: Scripts de verificación

### 🎯 Flujo de Uso

1. **Iniciar sistema** → `start_iq_system_complete.bat`
2. **Acceder dashboard** → http://localhost:5001  
3. **Login IQ Option** → Credenciales reales
4. **Seleccionar símbolo** → Solo símbolos disponibles
5. **Trading automático** → Órdenes en tiempo real
6. **Sesión persistente** → Se mantiene al recargar

## 🧪 Testing

```bash
# Verificar instalación completa
python verify_complete_setup.py

# Test símbolos disponibles  
python test_symbols.py

# Test sistema completo
python test_complete_system.py

# Verificar servicios manualmente
curl http://localhost:5001      # Dashboard
curl http://localhost:5002/health # API Health
```

## 🛠️ Troubleshooting

### Problemas Comunes

| Problema | Solución |
|----------|----------|
| **Redis no conecta** | `docker-compose up -d` o verificar puerto 6380 |
| **IQ Option error** | Verificar credenciales en `.env` |
| **No hay símbolos** | Esperar conexión del cliente IQ, mercado puede estar cerrado |
| **Dashboard no carga** | Verificar `mt5_server.py` corriendo en puerto 5001 |
| **API no responde** | Verificar `iq_routes_redis_patch.py` en puerto 5002 |

### Logs del Sistema

```bash
# Ver logs en tiempo real (si están configurados)
tail -f logs/*.log

# Verificar estado de servicios
python check_status.py
```

## 📚 Documentación Adicional

- 📄 [**SISTEMA_IQ_COMPLETO.md**](SISTEMA_IQ_COMPLETO.md) - Documentación técnica completa
- 🌐 [**GUIA_MIGRACION.html**](GUIA_MIGRACION.html) - Guía visual de migración
- 📋 [**INSTRUCCIONES_EJECUCION.md**](INSTRUCCIONES_EJECUCION.md) - Manual de uso

## 🤝 Contribuir

1. Fork del proyecto
2. Crear branch de feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## ⚠️ Disclaimers

- **Riesgo financiero**: Trading con dinero real conlleva riesgos
- **Solo educativo**: Este proyecto es para fines educativos
- **IQ Option ToS**: Asegúrate de cumplir los términos de servicio de IQ Option
- **Responsabilidad**: Los usuarios son responsables de sus decisiones de trading

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver [LICENSE](LICENSE) para detalles.

## 👨‍💻 Autor

**STC Trading Team**
- 📧 Email: support@stc-trading.com
- 🌐 Website: https://stc-trading.com

---

⭐ **¡Si te gusta este proyecto, dale una estrella!** ⭐
