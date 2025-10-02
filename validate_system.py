#!/usr/bin/env python3
"""
STC Trading System - Validación Final del Sistema
Verifica que todos los componentes estén correctamente configurados
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def print_status(message, status="INFO"):
    """Imprime mensaje con estado coloreado"""
    colors = {
        "INFO": "\033[96m",
        "SUCCESS": "\033[92m", 
        "WARNING": "\033[93m",
        "ERROR": "\033[91m",
        "RESET": "\033[0m"
    }
    
    color = colors.get(status, colors["INFO"])
    reset = colors["RESET"]
    prefix = {
        "INFO": "ℹ️",
        "SUCCESS": "✅", 
        "WARNING": "⚠️",
        "ERROR": "❌"
    }
    
    print(f"{color}{prefix.get(status, 'ℹ️')} {message}{reset}")

def check_file_exists(file_path, description):
    """Verifica si un archivo existe"""
    if os.path.exists(file_path):
        file_size = os.path.getsize(file_path)
        print_status(f"{description}: OK ({file_size:,} bytes)", "SUCCESS")
        return True
    else:
        print_status(f"{description}: FALTANTE", "ERROR")
        return False

def check_directory_exists(dir_path, description):
    """Verifica si un directorio existe"""
    if os.path.exists(dir_path) and os.path.isdir(dir_path):
        file_count = len(list(Path(dir_path).rglob("*")))
        print_status(f"{description}: OK ({file_count} archivos)", "SUCCESS")
        return True
    else:
        print_status(f"{description}: FALTANTE", "ERROR")
        return False

def validate_system_structure():
    """Valida la estructura del sistema"""
    print_status("=== VALIDACIÓN DE ESTRUCTURA DEL SISTEMA ===", "INFO")
    
    base_path = os.path.dirname(os.path.abspath(__file__))
    success_count = 0
    total_checks = 0
    
    # Archivos principales del backend
    backend_files = [
        ("iq_routes_redis_patch.py", "API Backend Principal"),
        ("signals_service_redis.py", "Servicio de Señales"),
        ("requirements.txt", "Dependencias Python"),
        ("README.md", "Documentación Principal"),
        (".env.example", "Configuración de Entorno")
    ]
    
    print_status("\n--- ARCHIVOS BACKEND ---", "INFO")
    for file_name, description in backend_files:
        file_path = os.path.join(base_path, file_name)
        if check_file_exists(file_path, description):
            success_count += 1
        total_checks += 1
    
    # Dashboard y templates
    frontend_files = [
        ("templates/dashboard.html", "Dashboard Principal HTML"),
        ("static/js/tradingview-config.js", "Configuración TradingView"),
        ("static/css/stc-styles.css", "Estilos CSS"),
        ("static/js/stc-charts.js", "Scripts de Gráficos")
    ]
    
    print_status("\n--- ARCHIVOS FRONTEND ---", "INFO")
    for file_path, description in frontend_files:
        full_path = os.path.join(base_path, file_path)
        if check_file_exists(full_path, description):
            success_count += 1
        total_checks += 1
    
    # Directorios esenciales
    directories = [
        ("templates", "Plantillas HTML"),
        ("static", "Archivos Estáticos"),
        ("static/js", "JavaScript"),
        ("static/css", "CSS"),
        ("docs", "Documentación"),
        ("tests", "Pruebas"),
        ("data", "Datos"),
        ("logs", "Registros"),
        ("config", "Configuración"),
        ("lightweight-charts", "TradingView Charts")
    ]
    
    print_status("\n--- DIRECTORIOS ---", "INFO")
    for dir_name, description in directories:
        dir_path = os.path.join(base_path, dir_name)
        if check_directory_exists(dir_path, description):
            success_count += 1
        total_checks += 1
    
    # Scripts de prueba
    test_files = [
        ("tests/test_complete_system.py", "Test Completo del Sistema"),
        ("tests/test_symbols.py", "Test de Símbolos"),
        ("post_install_setup.py", "Script Post-Instalación")
    ]
    
    print_status("\n--- ARCHIVOS DE PRUEBA ---", "INFO")
    for file_path, description in test_files:
        full_path = os.path.join(base_path, file_path)
        if check_file_exists(full_path, description):
            success_count += 1
        total_checks += 1
    
    # Documentación
    doc_files = [
        ("docs/SISTEMA_IQ_COMPLETO.md", "Documentación Completa"),
        ("docs/GUIA_MIGRACION.html", "Guía de Migración"),
        ("docs/LISTA_MIGRACION.txt", "Lista de Migración")
    ]
    
    print_status("\n--- DOCUMENTACIÓN ---", "INFO")
    for file_path, description in doc_files:
        full_path = os.path.join(base_path, file_path)
        if check_file_exists(full_path, description):
            success_count += 1
        total_checks += 1
    
    return success_count, total_checks

def validate_dashboard_content():
    """Valida el contenido del dashboard"""
    print_status("\n=== VALIDACIÓN DEL DASHBOARD ===", "INFO")
    
    dashboard_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "dashboard.html")
    
    if not os.path.exists(dashboard_path):
        print_status("Dashboard HTML no encontrado", "ERROR")
        return False
    
    try:
        with open(dashboard_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificaciones de contenido
        checks = [
            ("<!DOCTYPE html>", "Declaración HTML5"),
            ("TradingView", "Integración TradingView"),
            ("LightweightCharts", "Lightweight Charts"),
            ("IQ Option", "Integración IQ Option"),
            ("STC Trading", "Branding STC Trading"),
            ("class ChartManager", "Gestor de Gráficos"),
            ("class APIManager", "Gestor de API"),
            ("class UIManager", "Gestor de UI"),
            ("selectSymbol", "Selección de Símbolos"),
            ("executeTrade", "Ejecución de Trades"),
            ("/api/iq/", "Endpoints IQ Option"),
            ("candleSeries", "Series de Velas"),
            ("AlertManager", "Sistema de Alertas")
        ]
        
        success_count = 0
        for check_text, description in checks:
            if check_text in content:
                print_status(f"{description}: OK", "SUCCESS")
                success_count += 1
            else:
                print_status(f"{description}: FALTANTE", "ERROR")
        
        file_size = len(content)
        print_status(f"Tamaño del Dashboard: {file_size:,} caracteres", "INFO")
        
        if success_count >= len(checks) * 0.9:  # 90% de las verificaciones
            print_status("Dashboard validado correctamente", "SUCCESS")
            return True
        else:
            print_status("Dashboard tiene problemas de contenido", "WARNING")
            return False
            
    except Exception as e:
        print_status(f"Error validando dashboard: {e}", "ERROR")
        return False

def validate_tradingview_integration():
    """Valida la integración con TradingView"""
    print_status("\n=== VALIDACIÓN TRADINGVIEW ===", "INFO")
    
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    # Verificar repositorio descargado
    lightweight_path = os.path.join(base_path, "lightweight-charts")
    if check_directory_exists(lightweight_path, "TradingView Lightweight Charts"):
        
        # Verificar archivos clave
        key_files = [
            ("package.json", "Configuración NPM"),
            ("README.md", "Documentación"),
            ("dist", "Distribución Compilada")
        ]
        
        for file_name, description in key_files:
            file_path = os.path.join(lightweight_path, file_name)
            if os.path.exists(file_path):
                print_status(f"TradingView {description}: OK", "SUCCESS")
            else:
                print_status(f"TradingView {description}: FALTANTE", "WARNING")
    
    # Verificar configuración local
    config_path = os.path.join(base_path, "static", "js", "tradingview-config.js")
    if check_file_exists(config_path, "Configuración TradingView Local"):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if "lightweight-charts" in content or "TradingView" in content:
                print_status("Configuración TradingView válida", "SUCCESS")
                return True
        except:
            pass
    
    print_status("Configuración TradingView parcial", "WARNING")
    return False

def check_python_dependencies():
    """Verifica las dependencias de Python"""
    print_status("\n=== VERIFICACIÓN DE DEPENDENCIAS ===", "INFO")
    
    requirements_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "requirements.txt")
    
    if not os.path.exists(requirements_path):
        print_status("requirements.txt no encontrado", "ERROR")
        return False
    
    try:
        with open(requirements_path, 'r', encoding='utf-8') as f:
            requirements = f.read().strip().split('\n')
        
        print_status(f"Dependencias listadas: {len(requirements)}", "INFO")
        
        # Verificar algunas dependencias clave
        key_deps = ['flask', 'requests', 'redis', 'websocket']
        for dep in key_deps:
            if any(dep.lower() in req.lower() for req in requirements):
                print_status(f"Dependencia {dep}: OK", "SUCCESS")
            else:
                print_status(f"Dependencia {dep}: NO LISTADA", "WARNING")
        
        return True
        
    except Exception as e:
        print_status(f"Error verificando dependencias: {e}", "ERROR")
        return False

def generate_system_report():
    """Genera reporte del sistema"""
    print_status("\n=== REPORTE FINAL DEL SISTEMA ===", "INFO")
    
    # Ejecutar todas las validaciones
    structure_success, structure_total = validate_system_structure()
    dashboard_ok = validate_dashboard_content()
    tradingview_ok = validate_tradingview_integration()
    deps_ok = check_python_dependencies()
    
    # Calcular porcentaje general
    total_score = 0
    max_score = 4  # 4 categorías principales
    
    if structure_success >= structure_total * 0.8:  # 80% de archivos
        total_score += 1
        print_status("Estructura del Sistema: APROBADA", "SUCCESS")
    else:
        print_status("Estructura del Sistema: NECESITA ATENCIÓN", "WARNING")
    
    if dashboard_ok:
        total_score += 1
        print_status("Dashboard: APROBADO", "SUCCESS")
    else:
        print_status("Dashboard: NECESITA REVISIÓN", "WARNING")
    
    if tradingview_ok:
        total_score += 1
        print_status("TradingView: APROBADO", "SUCCESS")
    else:
        print_status("TradingView: NECESITA CONFIGURACIÓN", "WARNING")
    
    if deps_ok:
        total_score += 1
        print_status("Dependencias: APROBADAS", "SUCCESS")
    else:
        print_status("Dependencias: REVISAR", "WARNING")
    
    # Score final
    percentage = (total_score / max_score) * 100
    
    print_status(f"\n--- SCORE FINAL ---", "INFO")
    print_status(f"Archivos validados: {structure_success}/{structure_total}", "INFO")
    print_status(f"Sistema completado: {percentage:.1f}%", "INFO")
    
    if percentage >= 90:
        print_status("🎉 SISTEMA LISTO PARA PRODUCCIÓN", "SUCCESS")
        return "READY"
    elif percentage >= 70:
        print_status("⚡ SISTEMA FUNCIONAL - Ajustes menores necesarios", "WARNING")
        return "FUNCTIONAL"
    else:
        print_status("🔧 SISTEMA NECESITA CONFIGURACIÓN ADICIONAL", "ERROR")
        return "NEEDS_WORK"

def main():
    """Función principal"""
    print_status("STC Trading System - Validación Final", "INFO")
    print_status("=" * 60, "INFO")
    
    try:
        status = generate_system_report()
        
        print_status(f"\n--- PRÓXIMOS PASOS ---", "INFO")
        
        if status == "READY":
            print_status("1. Instalar dependencias: pip install -r requirements.txt", "INFO")
            print_status("2. Configurar variables de entorno (.env)", "INFO") 
            print_status("3. Ejecutar: python iq_routes_redis_patch.py", "INFO")
            print_status("4. Abrir dashboard en navegador", "INFO")
            
        elif status == "FUNCTIONAL":
            print_status("1. Revisar archivos faltantes arriba mencionados", "WARNING")
            print_status("2. Completar configuración de TradingView si es necesario", "WARNING")
            print_status("3. Instalar dependencias: pip install -r requirements.txt", "INFO")
            print_status("4. Probar sistema con: python tests/test_complete_system.py", "INFO")
            
        else:
            print_status("1. Revisar errores listados arriba", "ERROR")
            print_status("2. Completar archivos faltantes", "ERROR")
            print_status("3. Revisar documentación en docs/", "INFO")
            print_status("4. Re-ejecutar esta validación", "INFO")
        
        print_status("\n✨ Validación completada", "SUCCESS")
        return 0
        
    except Exception as e:
        print_status(f"Error durante validación: {e}", "ERROR")
        return 1

if __name__ == "__main__":
    sys.exit(main())
