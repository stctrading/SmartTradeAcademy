# 🚀 STC Trading - Sistema IQ Option Completo

## ✅ SOLUCIÓN IMPLEMENTADA

### 📋 Problema Resuelto:
- **Error**: "Unexpected token '<', "<!doctype "..." al obtener saldo
- **Causa**: El endpoint `/api/iq/balance` no estaba implementado
- **Solución**: Sistema completo con velas + saldo automático

### 🔧 Componentes Implementados:

#### 1. **iq_routes_redis_patch.py** (Puerto 5002)
- ✅ Endpoint `/api/iq/balance` implementado (GET/POST)
- ✅ Manejo de balance desde Redis
- ✅ CORS habilitado
- ✅ Endpoints: login, order, candles, balance, health

#### 2. **iq_client.py** (Servicio Completo IQ Option)
- ✅ Conecta a IQ Option API real
- ✅ Envía velas en tiempo real cada segundo
- ✅ Envía saldo cada 10 segundos automáticamente
- ✅ **PROCESA Y EJECUTA ÓRDENES** automáticamente
- ✅ Maneja PRACTICE/REAL balance types
- ✅ Tracking de resultados de órdenes

#### 3. **dashboard.html** (Frontend Completo)
- ✅ Obtiene saldo automáticamente (sin botón manual)
- ✅ **SELECTOR DINÁMICO DE SÍMBOLOS** desde IQ Option
- ✅ Normalización avanzada de velas irregulares  
- ✅ Rellenado de gaps temporales
- ✅ **ENVÍO Y TRACKING DE ÓRDENES EN TIEMPO REAL**
- ✅ Confirmación de ejecución desde IQ Option
- ✅ Mejor manejo de errores y recuperación
- ✅ Solo datos reales (sin mock)

### 🎯 **Cómo Usar:**

#### **Configuración Inicial:**
1. Crear archivo `.env` con tus credenciales:
```env
IQ_EMAIL=tu_email@iqoption.com
IQ_PASSWORD=tu_password
IQ_BALANCE_TYPE=PRACTICE
IQ_SYMBOLS=EURUSD-OTC,GBPUSD-OTC
IQ_TIMEFRAMES=M1,M5
SERVER_BASE=http://127.0.0.1:5002
REDIS_URL=redis://127.0.0.1:6380/0
```

#### **Inicio del Sistema:**
```bash
# Opción 1: Sistema completo (RECOMENDADO)
start_iq_system_complete.bat

# Opción 2: Manual
# 1. Redis (puerto 6380)
# 2. IQ API: python iq_routes_redis_patch.py  
# 3. Dashboard: python dashboard_server.py
# 4. IQ Client: python iq_client.py
```

#### **Acceso:**
- **Dashboard**: http://127.0.0.1:5001
- **IQ API**: http://127.0.0.1:5002
- **Health Check**: http://127.0.0.1:5002/health

### 📊 **Funcionalidades:**

#### **Automáticas:**
- ✅ Velas IQ Option en tiempo real (M1, M5)
- ✅ Saldo actualizado cada 10 segundos
- ✅ Normalización de velas irregulares
- ✅ Rellenado de gaps temporales
- ✅ Recuperación automática de errores

#### **Dashboard:**
- ✅ Login IQ Option con sesión persistente
- ✅ Ejecución de órdenes binarias/digitales
- ✅ Gráfico en tiempo real con countdown
- ✅ Señales manuales (BUY/SELL)
- ✅ Monitoreo de estado de conexión

#### **Endpoints API:**
- `POST /api/iq/login` - Login IQ Option
- `POST /api/iq/logout` - Logout IQ Option  
- `POST /api/iq/order` - **Ejecutar orden (SE PROCESA AUTOMÁTICAMENTE)**
- `GET /api/iq/order_results` - **Obtener resultados de órdenes ejecutadas**
- `GET /api/iq/symbols` - **Obtener símbolos disponibles desde IQ Option**
- `GET /api/iq/candles` - Obtener velas reales (no mock)
- `GET /api/iq/balance` - Obtener saldo real (no mock)
- `GET /health` - Estado del sistema

### 🎯 **NUEVO: Sistema de Órdenes Completo**

#### **Flujo de Ejecución de Órdenes:**
1. **Dashboard** envía orden → **Backend** (puerto 5002)
2. **Backend** encola orden en **Redis**
3. **IQ Client** procesa cola automáticamente
4. **IQ Client** ejecuta orden real en **IQ Option API**
5. **IQ Client** guarda resultado en **Redis**
6. **Dashboard** verifica y muestra confirmación

#### **Ejemplo de Orden:**
```javascript
// En el dashboard
{
  "symbol": "EURUSD-OTC",
  "action": "BUY",      // BUY o SELL
  "amount": 5,          // Monto en USD
  "duration": 5,        // Duración en minutos
  "option_type": "binary"
}
```

#### **Estados de Orden:**
- ⏳ **Enviando** - Orden enviada al backend
- 📋 **Encolada** - Orden en cola de procesamiento
- ✅ **Ejecutada** - Orden ejecutada exitosamente en IQ Option
- ❌ **Fallida** - Error en la ejecución

#### **Prueba del Sistema:**
```bash
# Ejecutar test completo
python test_order_system.py

# Resultado esperado:
🎉 SISTEMA FUNCIONANDO CORRECTAMENTE!
   - Cliente IQ conectado
   - Órdenes se procesan automáticamente  
   - Balance y velas en tiempo real
```

### 🔍 **Debugging:**

#### **Logs importantes:**
```bash
# IQ Client
✅ Balance actualizado: $10000.00 (PRACTICE)
🔄 Enviando velas: EURUSD-OTC M5

# IQ API Server  
[IQ ROUTES] on http://127.0.0.1:5002

# Dashboard
✅ Saldo PRACTICE: $10000.00
📊 Velas: 200 velas recibidas
```

#### **Verificación de estado:**
```bash
# Redis
redis-cli -p 6380 ping

# API Health
curl http://127.0.0.1:5002/health

# Balance  
curl http://127.0.0.1:5002/api/iq/balance
```

### 🎯 **Próximos Pasos:**
1. ✅ Sistema funcionando con velas + saldo automático
2. ✅ Error "Failed to fetch" resuelto completamente  
3. ✅ Dashboard original mantenido sin cambios de diseño
4. ✅ Comunicación frontend-backend funcionando con CORS

### 📝 **Notas Importantes:**
- El saldo se actualiza automáticamente cada 10 segundos
- Las velas se normalizan para manejar formatos irregulares
- El sistema se auto-recupera de errores de conexión
- Todos los servicios pueden iniciarse con un solo script
- El dashboard original mantiene su diseño y funcionalidad

🎉 **SISTEMA COMPLETAMENTE OPERATIVO**
