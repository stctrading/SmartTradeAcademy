/**
 * STC Trading System - TradingView Lightweight Charts Integration
 * Adaptado para IQ Option con soporte completo de gráficos
 */

class STCChartManager {
    constructor(containerId, options = {}) {
        this.containerId = containerId;
        this.container = document.getElementById(containerId);
        this.chart = null;
        this.candleSeries = null;
        this.volumeSeries = null;
        this.currentSymbol = 'EURUSD-OTC';
        this.isConnected = false;
        
        // Configuración por defecto
        this.config = {
            theme: 'dark',
            locale: 'es',
            layout: {
                background: { color: '#1e1e1e' },
                textColor: '#ffffff',
            },
            autoSize: true,
            watermark: 'STC Trading',
            ...options
        };
        
        this.initChart();
    }

    /**
     * Inicializar el gráfico TradingView
     */
    initChart() {
        if (!this.container) {
            console.error('Container not found:', this.containerId);
            return;
        }

        const chartOptions = {
            width: this.container.clientWidth,
            height: this.container.clientHeight,
            layout: {
                background: { 
                    type: LightweightCharts.ColorType.Solid,
                    color: this.config.theme === 'dark' ? '#1a1a1a' : '#ffffff'
                },
                textColor: this.config.theme === 'dark' ? '#ffffff' : '#000000',
            },
            grid: {
                vertLines: {
                    color: this.config.theme === 'dark' ? '#2a2a2a' : '#e0e0e0',
                },
                horzLines: {
                    color: this.config.theme === 'dark' ? '#2a2a2a' : '#e0e0e0',
                }
            },
            crosshair: {
                mode: LightweightCharts.CrosshairMode.Normal,
                vertLine: {
                    width: 1,
                    color: '#9598A1',
                    style: LightweightCharts.LineStyle.Dashed,
                },
                horzLine: {
                    width: 1,
                    color: '#9598A1',
                    style: LightweightCharts.LineStyle.Dashed,
                }
            },
            timeScale: {
                borderColor: '#485c7b',
                timeVisible: true,
                secondsVisible: false,
            },
            watermark: {
                color: 'rgba(11, 94, 29, 0.4)',
                visible: true,
                text: 'STC Trading',
                fontSize: 24,
                horzAlign: 'left',
                vertAlign: 'bottom',
            },
        };

        // Crear el gráfico
        this.chart = LightweightCharts.createChart(this.container, chartOptions);
        
        // Crear serie de velas
        this.candleSeries = this.chart.addCandlestickSeries({
            upColor: '#26a69a',
            downColor: '#ef5350',
            borderVisible: false,
            wickUpColor: '#26a69a',
            wickDownColor: '#ef5350',
        });

        console.log('✅ Chart initialized successfully');
        this.isConnected = true;
    }

    /**
     * Actualizar datos del gráfico
     */
    updateData(symbol, timeframe = 'M5', limit = 200) {
        if (!this.chart || !this.candleSeries) {
            console.error('Chart not initialized');
            return;
        }

        const endpoint = `/api/iq/candles?symbol=${symbol}&timeframe=${timeframe}&limit=${limit}`;
        
        fetch(endpoint)
            .then(response => response.json())
            .then(data => {
                if (data && Array.isArray(data) && data.length > 0) {
                    console.log(`📊 Received ${data.length} candles for ${symbol}`);
                    
                    // Limpiar datos previos
                    this.candleSeries.setData([]);
                    
                    // Formatear datos para TradingView
                    const formattedData = data.map(candle => ({
                        time: Math.floor(candle.time / 1000), // Convertir a segundos
                        open: parseFloat(candle.open),
                        high: parseFloat(candle.high),
                        low: parseFloat(candle.low),
                        close: parseFloat(candle.close)
                    }));

                    // Ordenar por tiempo (ascendente)
                    formattedData.sort((a, b) => a.time - b.time);
                    
                    // Cargar todas las velas
                    this.candleSeries.setData(formattedData);
                    
                    console.log(`✅ Chart updated with ${formattedData.length} candles`);
                    
                    // Ajustar vista para mostrar todas las velas
                    this.chart.timeScale().fitContent();
                    
                } else {
                    console.warn('No data received or invalid format');
                }
            })
            .catch(error => {
                console.error('Error fetching candles:', error);
            });
    }

    /**
     * Cambiar símbolo
     */
    changeSymbol(symbol) {
        this.currentSymbol = symbol;
        this.updateData(symbol);
    }

    /**
     * Actualización automática cada 5 segundos
     */
    startAutoUpdate() {
        setInterval(() => {
            this.updateData(this.currentSymbol);
        }, 5000);
    }
}

// Variable global para el chart manager
window.STCChartManager = STCChartManager;