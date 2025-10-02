#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
STC Dashboard Server - Version HTTP Simple
Puerto 5001 HTTP para evitar problemas de certificados SSL
"""

import os
import re
import json
import time
import ssl
import logging
import threading
from datetime import datetime, timezone, timedelta
from collections import defaultdict, deque
from flask import Flask, request, jsonify, render_template, redirect, url_for, send_file

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("stc-dashboard")

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.jinja_env.auto_reload = True

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,X-Signature')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# ================= Config =================
DASHBOARD_PORT = 5001

# ================= Rutas Dashboard =================
@app.route("/")
def root():
    return render_template("dashboard_pro.html")

@app.route("/dashboard")
def dashboard_page():
    return render_template("dashboard_pro.html")

@app.route("/dashboard_old")
def dashboard_old():
    return render_template("dashboard.html")

@app.route("/dashboard_candles_signals.html")
def legacy_dashboard_redirect():
    return redirect(url_for('dashboard_page'), code=302)

@app.route("/stable")
def dashboard_stable():
    return render_template("dashboard_stable.html")

@app.route("/charts-test")
def charts_test():
    return render_template("dashboard_stable.html")

# ================= Info / Salud =================
@app.route('/api', methods=['GET'])
def api_info():
    return jsonify({
        "service": "STC Dashboard",
        "version": "1.0",
        "status": "running",
        "port": DASHBOARD_PORT,
        "protocol": "HTTP"
    })

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "STC Dashboard", 
        "timestamp": time.time()
    })

# ================= Rutas de API Proxy =================
import requests

@app.route('/api/iq/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
def proxy_iq_api(path):
    """Proxy requests to the main API server on port 5002"""
    try:
        api_url = f"http://localhost:5002/api/iq/{path}"
        
        if request.method == 'OPTIONS':
            return '', 200
        
        if request.method == 'GET':
            response = requests.get(api_url, params=request.args, timeout=10)
        elif request.method == 'POST':
            response = requests.post(api_url, json=request.json, timeout=10)
        elif request.method == 'PUT':
            response = requests.put(api_url, json=request.json, timeout=10)
        elif request.method == 'DELETE':
            response = requests.delete(api_url, timeout=10)
        
        return response.json(), response.status_code
    except Exception as e:
        logger.error(f"Error proxying to API: {e}")
        return jsonify({"error": "API not available", "details": str(e)}), 503

def run_dashboard():
    print(f"🌐 STC Dashboard iniciando en puerto {DASHBOARD_PORT}")
    print(f"📊 Acceso: http://localhost:{DASHBOARD_PORT}")
    app.run(host='0.0.0.0', port=DASHBOARD_PORT, debug=False)

if __name__ == '__main__':
    run_dashboard()
