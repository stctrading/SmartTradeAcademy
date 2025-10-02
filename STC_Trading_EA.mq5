//+------------------------------------------------------------------+
//|                                           STC_Trading_EA.mq5     |
//|                        Expert Advisor for STC Trading Platform   |
//|                        Sends BID/ASK data to web dashboard       |
//+------------------------------------------------------------------+
#property copyright "STC Trading Platform"
#property version   "2.02"

//--- Input parameters
input string SERVER_URL = "https://127.0.0.1:5001";  // Puerto HTTPS del servidor dual para MT5
input string    API_SECRET = "tu_clave_secreta_muy_segura_2024";  // CORREGIDO: Clave del servidor  
input string    SYMBOLS = "BTCUSD#";     
input int       SEND_INTERVAL = 2;                           
input ENUM_TIMEFRAMES TIMEFRAME = PERIOD_M5;                  
input bool      ENABLE_TICK_STREAM = true;                    
input bool      ENABLE_CANDLE_STREAM = true;                  
input bool      ENABLE_LOGGING = true;

//--- Global variables
string g_symbols[];
int g_symbol_count = 0;
datetime g_last_candle_time[];

//--- BID/ASK tracking for precise candles
struct BidAskCandle {
    datetime time;
    double bid_open, bid_high, bid_low, bid_close;
    double ask_open, ask_high, ask_low, ask_close;
    double open, high, low, close;  // Calculated midpoint
    long volume;
    double spread_avg;
};

BidAskCandle g_current_candles[];

//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
{
    Print("🚀 STC Trading EA v2.02 Starting...");
    
    // Test connectivity
    string test_url = "https://httpbin.org/get";
    string headers = "";
    uchar data[], result[];
    string result_headers;
    int timeout = 5000;
    int res = WebRequest("GET", test_url, headers, timeout, data, result, result_headers);
    
    if(res == 200) {
        Print("✅ HTTPS connectivity confirmed");
    } else {
        Print("❌ HTTPS test failed: ", res);
    }
    
    // Test SERVER connectivity
    Print("🔍 Testing server connectivity...");
    string server_test_url = SERVER_URL + "/health";
    string server_headers = "";
    uchar server_data[], server_result[];
    string server_result_headers;
    int server_timeout = 5000;
    int server_res = WebRequest("GET", server_test_url, server_headers, server_timeout, server_data, server_result, server_result_headers);
    
    if(server_res == 200) {
        Print("✅ Server connectivity confirmed: ", SERVER_URL);
    } else {
        Print("❌ Server test failed: ", server_res, " URL: ", server_test_url);
        Print("💡 Make sure server is running and URL is authorized in MT5");
        Print("💡 Go to Tools → Options → Expert Advisors → Allow WebRequest for: ", SERVER_URL);
    }
    
    // Parse symbols
    if(!ParseSymbols()) {
        return INIT_FAILED;
    }
    
    // Initialize arrays
    ArrayResize(g_last_candle_time, g_symbol_count);
    ArrayResize(g_current_candles, g_symbol_count);
    
    for(int i = 0; i < g_symbol_count; i++) {
        g_last_candle_time[i] = 0;
        InitializeCandle(i);
    }
    
    Print("✅ STC Trading EA v2.02 initialized successfully");
    Print("📊 Tracking symbols: ", SYMBOLS);
    Print("🔗 Server URL: ", SERVER_URL);
    
    // Send initial historical data (100 M5 candles)
    SendInitialHistoricalData();
    
    // Set timer
    EventSetTimer(SEND_INTERVAL);
    
    return INIT_SUCCEEDED;
}

//+------------------------------------------------------------------+
//| Expert deinitialization function                                |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
{
    EventKillTimer();
    Print("🛑 STC Trading EA stopped");
}

//+------------------------------------------------------------------+
//| Timer function                                                  |
//+------------------------------------------------------------------+
void OnTimer()
{
    for(int i = 0; i < g_symbol_count; i++) {
        string symbol = g_symbols[i];
        
        // Update BID/ASK data
        UpdateBidAskData(symbol, i);
        
        if(ENABLE_TICK_STREAM) {
            SendTickData(symbol);
        }
        if(ENABLE_CANDLE_STREAM) {
            // Enviar la vela en formación (actual, no cerrada)
            SendLiveCandle(symbol, i);
            // Si hay cambio de vela, se envía la cerrada normalmente
            CheckAndSendCandle(symbol, i);
        }
    }
}

//+------------------------------------------------------------------+
//| Parse symbols from input                                        |
//+------------------------------------------------------------------+
bool ParseSymbols()
{
    string symbol_list = SYMBOLS;
    StringReplace(symbol_list, " ", "");
    
    g_symbol_count = StringSplit(symbol_list, ',', g_symbols);
    
    if(g_symbol_count == 0) {
        Print("❌ No symbols specified");
        return false;
    }
    
    for(int i = 0; i < g_symbol_count; i++) {
        if(!SymbolSelect(g_symbols[i], true)) {
            Print("⚠️ Symbol not available: " + g_symbols[i]);
        } else {
            Print("✅ Symbol added: " + g_symbols[i]);
        }
    }
    
    return true;
}

//+------------------------------------------------------------------+
//| Initialize candle tracking                                      |
//+------------------------------------------------------------------+
void InitializeCandle(int index)
{
    string symbol = g_symbols[index];
    double bid = SymbolInfoDouble(symbol, SYMBOL_BID);
    double ask = SymbolInfoDouble(symbol, SYMBOL_ASK);
    
    // Usar tiempo de vela actual del timeframe, no TimeCurrent()
    datetime current_candle_time = iTime(symbol, TIMEFRAME, 0);
    
    g_current_candles[index].time = current_candle_time;
    g_current_candles[index].bid_open = bid;
    g_current_candles[index].bid_high = bid;
    g_current_candles[index].bid_low = bid;
    g_current_candles[index].bid_close = bid;
    
    g_current_candles[index].ask_open = ask;
    g_current_candles[index].ask_high = ask;
    g_current_candles[index].ask_low = ask;
    g_current_candles[index].ask_close = ask;
    
    // Calculate midpoint - OPEN SE FIJA AQUÍ Y NO CAMBIA
    double midpoint_open = (bid + ask) / 2.0;
    g_current_candles[index].open = midpoint_open;  // ← FIJO
    g_current_candles[index].high = midpoint_open;  // Empezar igual al OPEN
    g_current_candles[index].low = midpoint_open;   // Empezar igual al OPEN
    g_current_candles[index].close = midpoint_open; // Se actualizará
    
    g_current_candles[index].volume = 0;
    g_current_candles[index].spread_avg = ask - bid;
    
    if(ENABLE_LOGGING) {
        Print("🆕 Nueva vela iniciada - ", symbol, " OPEN fijo: ", DoubleToString(midpoint_open, 5), 
              " Time: ", TimeToString(current_candle_time));
    }
}

//+------------------------------------------------------------------+
//| Update BID/ASK data                                            |
//+------------------------------------------------------------------+
void UpdateBidAskData(string symbol, int index)
{
    double bid = SymbolInfoDouble(symbol, SYMBOL_BID);
    double ask = SymbolInfoDouble(symbol, SYMBOL_ASK);
    
    // Update BID highs and lows
    if(bid > g_current_candles[index].bid_high) 
        g_current_candles[index].bid_high = bid;
    if(bid < g_current_candles[index].bid_low) 
        g_current_candles[index].bid_low = bid;
        
    // Update ASK highs and lows
    if(ask > g_current_candles[index].ask_high) 
        g_current_candles[index].ask_high = ask;
    if(ask < g_current_candles[index].ask_low) 
        g_current_candles[index].ask_low = ask;
    
    // Update current close values (BID/ASK)
    g_current_candles[index].bid_close = bid;
    g_current_candles[index].ask_close = ask;
    
    // Calculate current midpoint close
    double current_close = (bid + ask) / 2.0;
    g_current_candles[index].close = current_close; // CLOSE se actualiza
    
    // Update HIGH/LOW basado en MIDPOINT - NUNCA cambiar OPEN
    // REGLA: HIGH >= OPEN, LOW <= OPEN
    double open_price = g_current_candles[index].open; // OPEN es FIJO
    
    if(current_close > g_current_candles[index].high)
        g_current_candles[index].high = current_close;
    if(current_close < g_current_candles[index].low)
        g_current_candles[index].low = current_close;
    
    // VALIDACIONES DE SEGURIDAD
    if(g_current_candles[index].high < open_price) {
        g_current_candles[index].high = open_price; // HIGH no puede ser < OPEN
    }
    if(g_current_candles[index].low > open_price) {
        g_current_candles[index].low = open_price;  // LOW no puede ser > OPEN
    }
    
    g_current_candles[index].volume++;
    g_current_candles[index].spread_avg = (ask - bid); // Spread promedio
}

//+------------------------------------------------------------------+
//| Send tick data                                                 |
//+------------------------------------------------------------------+
void SendTickData(string symbol)
{
    MqlTick tick;
    if(!SymbolInfoTick(symbol, tick)) return;
    
    string timestamp = TimeToString(TimeCurrent(), TIME_DATE|TIME_SECONDS) + "Z";
    string json_data = StringFormat(
        "{\"symbol\":\"%s\",\"bid\":%.5f,\"ask\":%.5f,\"last\":%.5f,\"spread\":%.5f,\"timestamp\":\"%s\"}",
        symbol, tick.bid, tick.ask, tick.last, (tick.ask - tick.bid), timestamp
    );
    
    string signature = "sha256=" + CalculateHMAC(json_data, API_SECRET);
    string server_url = SERVER_URL + "/api/mt5/tick";
    string headers = "Content-Type: application/json\r\nX-Signature: " + signature + "\r\n";
    
    uchar post[], result[];
    string result_headers;
    StringToCharArray(json_data, post, 0, StringLen(json_data));
    
    int timeout = 5000;
    int res = WebRequest("POST", server_url, headers, timeout, post, result, result_headers);
    
    if(res == 200) {
        if(ENABLE_LOGGING) {
            Print("📊 Tick sent: ", symbol, " BID:", DoubleToString(tick.bid, 5), 
                  " ASK:", DoubleToString(tick.ask, 5));
        }
    } else {
        // DEBUGGING DETALLADO
        Print("❌ Tick failed: ", symbol, " HTTP:", res);
        Print("🔗 URL: ", server_url);
        Print("🔐 Signature: ", signature);
        Print("📝 JSON length: ", StringLen(json_data));
        if(StringLen(result_headers) > 0) {
            Print("📤 Response headers: ", result_headers);
        }
        if(ArraySize(result) > 0) {
            string response = CharArrayToString(result);
            Print("📤 Response: ", response);
        }
    }
}

//+------------------------------------------------------------------+
//| Send the live (forming) candle                                  |
//+------------------------------------------------------------------+
void SendLiveCandle(string symbol, int index)
{
    BidAskCandle candle = g_current_candles[index];
    string timestamp = TimeToString(candle.time, TIME_DATE|TIME_SECONDS) + "Z";
    
    // Formato correcto para el servidor - vela individual, no array
    string json_data = StringFormat(
        "{" +
        "\"symbol\":\"%s\"," +
        "\"timeframe\":\"M5\"," +
        "\"timestamp\":\"%s\"," +
        "\"open\":%.5f,\"high\":%.5f,\"low\":%.5f,\"close\":%.5f," +
        "\"volume\":%d," +
        "\"bid_open\":%.5f,\"bid_high\":%.5f,\"bid_low\":%.5f,\"bid_close\":%.5f," +
        "\"ask_open\":%.5f,\"ask_high\":%.5f,\"ask_low\":%.5f,\"ask_close\":%.5f," +
        "\"spread_avg\":%.5f," +
        "\"candle_type\":\"enhanced\"," +
        "\"closed\":false" +
        "}",
        symbol, timestamp,
        candle.open, candle.high, candle.low, candle.close, (int)candle.volume,
        candle.bid_open, candle.bid_high, candle.bid_low, candle.bid_close,
        candle.ask_open, candle.ask_high, candle.ask_low, candle.ask_close,
        candle.spread_avg
    );
    string signature = "sha256=" + CalculateHMAC(json_data, API_SECRET);
    string server_url = SERVER_URL + "/api/mt5/candles";
    string headers = "Content-Type: application/json\r\nX-Signature: " + signature + "\r\n";
    uchar post[], result[];
    string result_headers;
    StringToCharArray(json_data, post, 0, StringLen(json_data));
    int timeout = 5000;
    int res = WebRequest("POST", server_url, headers, timeout, post, result, result_headers);
    if(res == 200) {
        if(ENABLE_LOGGING) {
            string direction = (candle.close > candle.open) ? "🟢 VERDE" : "🔴 ROJO";
            double pips = (candle.close - candle.open) * 100000;
            Print("🔄 Live candle sent: ", symbol, " ", direction, 
                  " O:", DoubleToString(candle.open, 5),
                  " H:", DoubleToString(candle.high, 5),
                  " L:", DoubleToString(candle.low, 5),
                  " C:", DoubleToString(candle.close, 5),
                  " (", DoubleToString(pips, 1), " pips)");
        }
    } else {
        // DEBUGGING DETALLADO para Live Candle
        Print("❌ Live candle failed: ", symbol, " HTTP:", res);
        Print("🔗 URL: ", server_url);
        Print("🔐 Signature: ", signature);
        if(StringLen(result_headers) > 0) {
            Print("📤 Response headers: ", result_headers);
        }
        if(ArraySize(result) > 0) {
            string response = CharArrayToString(result);
            Print("📤 Response: ", StringSubstr(response, 0, 200)); // Primeros 200 caracteres
        }
    }
}

//+------------------------------------------------------------------+
//| Check and send candle                                          |
//+------------------------------------------------------------------+
void CheckAndSendCandle(string symbol, int symbol_index)
{
    MqlRates rates[];
    if(CopyRates(symbol, TIMEFRAME, 0, 1, rates) != 1) return;
    
    datetime candle_time = rates[0].time;
    
    if(candle_time > g_last_candle_time[symbol_index]) {
        g_last_candle_time[symbol_index] = candle_time;
        
        // Send enhanced BID/ASK candle (cerrada)
        SendEnhancedCandle(symbol, symbol_index);
        
        // Reset for next candle
        InitializeCandle(symbol_index);
    }
}

//+------------------------------------------------------------------+
//| Send enhanced candle with BID/ASK data (closed)                 |
//+------------------------------------------------------------------+
void SendEnhancedCandle(string symbol, int index)
{
    BidAskCandle candle = g_current_candles[index];
    string timestamp = TimeToString(candle.time, TIME_DATE|TIME_SECONDS) + "Z";
    
    // Formato correcto para el servidor - vela individual, no array
    string json_data = StringFormat(
        "{" +
        "\"symbol\":\"%s\"," +
        "\"timeframe\":\"M5\"," +
        "\"timestamp\":\"%s\"," +
        "\"open\":%.5f,\"high\":%.5f,\"low\":%.5f,\"close\":%.5f," +
        "\"volume\":%d," +
        "\"bid_open\":%.5f,\"bid_high\":%.5f,\"bid_low\":%.5f,\"bid_close\":%.5f," +
        "\"ask_open\":%.5f,\"ask_high\":%.5f,\"ask_low\":%.5f,\"ask_close\":%.5f," +
        "\"spread_avg\":%.5f," +
        "\"candle_type\":\"enhanced\"," +
        "\"closed\":true" +
        "}",
        symbol, timestamp,
        candle.open, candle.high, candle.low, candle.close, (int)candle.volume,
        candle.bid_open, candle.bid_high, candle.bid_low, candle.bid_close,
        candle.ask_open, candle.ask_high, candle.ask_low, candle.ask_close,
        candle.spread_avg
    );
    string signature = "sha256=" + CalculateHMAC(json_data, API_SECRET);
    string server_url = SERVER_URL + "/api/mt5/candles";
    string headers = "Content-Type: application/json\r\nX-Signature: " + signature + "\r\n";
    uchar post[], result[];
    string result_headers;
    StringToCharArray(json_data, post, 0, StringLen(json_data));
    int timeout = 5000;
    int res = WebRequest("POST", server_url, headers, timeout, post, result, result_headers);
    if(res == 200) {
        if(ENABLE_LOGGING) {
            Print("🏆 Closed candle sent: ", symbol, 
                  " O:", DoubleToString(candle.open, 5),
                  " H:", DoubleToString(candle.high, 5),
                  " L:", DoubleToString(candle.low, 5),
                  " C:", DoubleToString(candle.close, 5),
                  " Vol:", (int)candle.volume);
        }
    } else {
        Print("❌ Closed candle failed: ", symbol, " HTTP:", res);
    }
}

//+------------------------------------------------------------------+
//| Calculate HMAC signature                                        |
//+------------------------------------------------------------------+
string CalculateHMAC(string data, string key)
{
    // Simple hash implementation for compatibility
    string combined = key + data;
    ulong hash = 0;
    
    for(int i = 0; i < StringLen(combined); i++) {
        hash = hash * 31 + StringGetCharacter(combined, i);
    }
    
    return IntegerToString(hash, 16);
}

//+------------------------------------------------------------------+
//| Send initial historical data for all symbols                    |
//+------------------------------------------------------------------+
void SendInitialHistoricalData()
{
    for(int i = 0; i < g_symbol_count; i++) {
        string symbol = g_symbols[i];
        
        MqlRates rates[];
        int copied = CopyRates(symbol, TIMEFRAME, 0, 100, rates);
        
        if(copied > 0) {
            Print("📜 Sending ", copied, " historical candles for ", symbol);
            
            for(int j = 0; j < copied; j++) {
                SendHistoricalCandle(symbol, rates[j]);
                Sleep(50);
            }
        }
    }
}

//+------------------------------------------------------------------+
//| Send a single historical candle with retry mechanism            |
//+------------------------------------------------------------------+
bool SendHistoricalCandle(string symbol, MqlRates &rate)
{
    // Get current spread for approximation  
    double current_bid = SymbolInfoDouble(symbol, SYMBOL_BID);
    double current_ask = SymbolInfoDouble(symbol, SYMBOL_ASK);
    double current_spread = current_ask - current_bid;
    
    double half_spread = current_spread / 2.0;
    
    // Calculate BID/ASK values from midpoint OHLC
    double bid_open = rate.open - half_spread;
    double bid_high = rate.high - half_spread;
    double bid_low = rate.low - half_spread;
    double bid_close = rate.close - half_spread;
    
    double ask_open = rate.open + half_spread;
    double ask_high = rate.high + half_spread;
    double ask_low = rate.low + half_spread;
    double ask_close = rate.close + half_spread;
    
    string timestamp = TimeToString(rate.time, TIME_DATE|TIME_SECONDS) + "Z";
    
    string json_data = StringFormat(
        "{" +
        "\"symbol\":\"%s\"," +
        "\"timeframe\":\"M5\"," +
        "\"timestamp\":\"%s\"," +
        "\"open\":%.5f,\"high\":%.5f,\"low\":%.5f,\"close\":%.5f," +
        "\"volume\":%d," +
        "\"bid_open\":%.5f,\"bid_high\":%.5f,\"bid_low\":%.5f,\"bid_close\":%.5f," +
        "\"ask_open\":%.5f,\"ask_high\":%.5f,\"ask_low\":%.5f,\"ask_close\":%.5f," +
        "\"spread_avg\":%.5f," +
        "\"candle_type\":\"historical\"," +
        "\"closed\":true" +
        "}",
        symbol, timestamp,
        rate.open, rate.high, rate.low, rate.close, (int)rate.tick_volume,
        bid_open, bid_high, bid_low, bid_close,
        ask_open, ask_high, ask_low, ask_close,
        current_spread
    );
    
    string signature = "sha256=" + CalculateHMAC(json_data, API_SECRET);
    string server_url = SERVER_URL + "/api/mt5/candles";
    string headers = "Content-Type: application/json\r\nX-Signature: " + signature + "\r\n";
    
    uchar post[], result[];
    string result_headers;
    StringToCharArray(json_data, post, 0, StringLen(json_data));
    
    int timeout = 5000;
    int res = WebRequest("POST", server_url, headers, timeout, post, result, result_headers);
    
    if(res == 200) {
        if(ENABLE_LOGGING) {
            Print("📜 Historical candle sent: ", symbol, " ", TimeToString(rate.time));
        }
        return true;
    } else {
        Print("❌ Historical candle failed: ", symbol, " HTTP:", res);
        return false;
    }
}

