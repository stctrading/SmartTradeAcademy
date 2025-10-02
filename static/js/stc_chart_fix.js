/**
 * STC Trading System - TradingView LightWeight Charts Integration
 * Adaptador para IQ Option con soporte completo de gráficos
 */

window.STCChartFix = (function() {
    
    let chart = null;
    let candleSeries = null;
    let config = {};
    let intervalId = null;

    /**
     * Inicializar el sistema de gráficos
     */
    function init(options = {}) {
        config = {
            containerId: 'chart',
            endpoint: '/api/iq/candles?symbol=EURUSD-OTC&timeframe=M5&limit=200',
            timeframe: 'M5',
            pollMs: 2000,
            max: 200,
            ...options
        };

        console.log('🎯 Inicializando STCChartFix con config:', config);
        
        initChart();
        loadInitialData();
        startPolling();
    }

    /**
     * Crear el gráfico con LightweightCharts
     */
    function initChart() {
        const container = document.getElementById(config.containerId);
        if (!container) {
            console.error('❌ Container no encontrado:', config.containerId);
            return;
        }

        // Crear gráfico
        chart = LightweightCharts.createChart(container, {
            width: container.clientWidth,
            height: container.clientHeight || 400,
            layout: {
                background: { type: 'solid', color: '#131722' },
                textColor: '#d1d4dc',
            },
            grid: {
                vertLines: { color: '#1f2937' },
                horzLines: { color: '#1f2937' },
            },
            rightPriceScale: {
                borderColor: '#1f2937',
            },
            timeScale: {
                borderColor: '#1f2937',
                timeVisible: true,
                secondsVisible: false,
            },
            crosshair: {
                mode: LightweightCharts.CrosshairMode.Normal,
            },
        });

        // Crear serie de velas
        candleSeries = chart.addCandlestickSeries({
            upColor: '#00D09C',
            downColor: '#FF5B5A',
            borderVisible: false,
            wickUpColor: '#00D09C', 
            wickDownColor: '#FF5B5A',
        });

        // Auto-resize
        new ResizeObserver(entries => {
            if (entries.length === 0 || entries[0].target !== container) return;
            const newRect = entries[0].contentRect;
            chart.applyOptions({ 
                width: newRect.width, 
                height: newRect.height 
            });
        }).observe(container);

        console.log('✅ Gráfico LightweightCharts inicializado');
    }

    /**
     * Cargar datos iniciales
     */
    async function loadInitialData() {
        try {
            console.log('📊 Cargando datos iniciales desde:', config.endpoint);
            
            const response = await fetch(config.endpoint);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const data = await response.json();
            console.log('📈 Datos recibidos:', data);
            
            if (Array.isArray(data) && data.length > 0) {
                updateChart(data);
                console.log(`✅ Cargadas ${data.length} velas iniciales`);
            } else {
                console.warn('⚠️ No hay datos de velas disponibles');
            }
            
        } catch (error) {
            console.error('❌ Error cargando datos iniciales:', error);
        }
    }

    /**
     * Actualizar el gráfico con velas
     */
    function updateChart(candles) {
        if (!candleSeries || !Array.isArray(candles)) {
            console.warn('⚠️ Serie no inicializada o datos inválidos');
            return;
        }

        try {
            // Preparar datos para el gráfico
            const chartData = candles.map(candle => ({
                time: candle.time,
                open: parseFloat(candle.open),
                high: parseFloat(candle.high),
                low: parseFloat(candle.low),
                close: parseFloat(candle.close)
            }));

            // Actualizar la serie
            candleSeries.setData(chartData);
            
            // Ajustar vista
            chart.timeScale().fitContent();
            
            console.log(`📊 Procesadas ${chartData.length} velas para el gráfico`);
            
        } catch (error) {
            console.error('❌ Error actualizando gráfico:', error);
        }
    }

    /**
     * Iniciar polling para actualizaciones
     */
    function startPolling() {
        if (intervalId) {
            clearInterval(intervalId);
        }
        
        intervalId = setInterval(async () => {
            try {
                const response = await fetch(config.endpoint);
                if (response.ok) {
                    const data = await response.json();
                    if (Array.isArray(data) && data.length > 0) {
                        updateChart(data);
                    }
                }
            } catch (error) {
                console.error('❌ Error en polling:', error);
            }
        }, config.pollMs);
        
        console.log(`🔄 Polling iniciado cada ${config.pollMs}ms`);
    }

    /**
     * Detener polling
     */
    function stopPolling() {
        if (intervalId) {
            clearInterval(intervalId);
            intervalId = null;
            console.log('⏹️ Polling detenido');
        }
    }

    /**
     * Destruir el gráfico
     */
    function destroy() {
        stopPolling();
        if (chart) {
            chart.remove();
            chart = null;
            candleSeries = null;
        }
    }

    // Exponer API pública
    return {
        init,
        destroy,
        startPolling,
        stopPolling,
        updateChart
    };
})();

// Inicializar automáticamente cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    console.log('🎯 DOM listo, inicializando STC Charts...');
    
    // Configuración por defecto
    const symbol = 'EURUSD-OTC';
    window.STCChartFix.init({
        containerId: 'chart',
        endpoint: `/api/iq/candles?symbol=${symbol}&timeframe=M5&limit=200`,
        timeframe: 'M5',
        pollMs: 2000,
        max: 200
    });
});
