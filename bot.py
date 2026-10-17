import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

# ── CONFIGURACIÓN GENERAL Y CREDENCIALES ──
TOKEN_TELEGRAM = "8959520494:AAEjYsnz81f6KD5HDlII_05PH-I3-CAydQs"

# Parámetros de Estrategia, Banca y Filtros Avanzados
CONFIG_ESTRATEGIA = {
    "monto_apuesta_base": 1000,          # Apuesta constante por jugada (Bs)
    "capital_inicial": 10000,            # Capital de partida (Bs)
    "meta_capital_stop": 50000,          # Meta de sesión: Al llegar aquí, el bot se detiene
    
    # Filtros de Sala y Secuencia
    "min_jugadores": 1650,               # Mínimo de personas en sala
    "min_multiplicador_1": 2.16,         # Verde 1 mínimo
    
    # Análisis de Distancia Top 8 (Ordenado Mayor a Menor)
    "analizar_top_8": True,
    "max_diferencia_escalon": 50000,     # Máximo salto permitido entre puestos consecutivos (P_n - P_{n+1})
    "min_monto_p8": 10000,               # El puesto 8 debe tener al menos 10k Bs
    
    # Control de Salidas y Cashout Dinámico
    "cashout_estandar": 2.00,            # Retiro base (1.85x - 2.10x)
    "cashout_extendido_liquidez": 3.45,  # Meta ampliada si el Top 8 es denso y pesado
    
    # Modo Sniper Esporádico (3.94x)
    "activar_sniper_394": True,
    "target_sniper": 3.94,
    "min_jugadores_sniper": 2000,
    
    # Seguridad
    "pausa_por_3_rojos": True           # Pausa si ocurren 3 crash seguidos (< 2.00x)
}

bot = Bot(token=TOKEN_TELEGRAM)
dp = Dispatcher()

# Variables de Estado de la Sesión
estado_sesion = {
    "capital_actual": 10000,
    "activo": True,
    "intentos_sniper_hoy": 0
}

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "🤖 **Bot Triunfobet @xMythos_bot Operativo**\n\n"
        f"• **Capital Actual:** {estado_sesion['capital_actual']} Bs\n"
        f"• **Meta de Sesión:** {CONFIG_ESTRATEGIA['meta_capital_stop']} Bs\n"
        "• **Modo:** Apuestas constantes (Sin pausas arbitrarias, operando bajo filtros Top 8).\n\n"
        "Usa `/estado` para ver el balance o `/detener` para pausar."
    )

@dp.message(Command("estado"))
async def cmd_estado(message: types.Message):
    await message.answer(
        f"📊 **Estado del Bot**\n"
        f"• Capital: `{estado_sesion['capital_actual']} Bs`\n"
        f"• Estado del Sistema: `{'ACTIVO 🟢' if estado_sesion['activo'] else 'DETENIDO 🔴'}`"
    )

@dp.message(Command("detener"))
async def cmd_detener(message: types.Message):
    estado_sesion["activo"] = False
    await message.answer("🛑 Bot detenido manualmente por el usuario.")

# Función lógica central de análisis y ejecución
async def evaluar_y_operar():
    if not estado_sesion["activo"]:
        return

    # Verificación de la meta de capital (10k a 50k)
    if estado_sesion["capital_actual"] >= CONFIG_ESTRATEGIA["meta_capital_stop"]:
        estado_sesion["activo"] = False
        # Aquí puedes disparar una alerta a Telegram notificando que se llegó a los 50k
        return

    # 1. Simulación de lectura del entorno de Triunfobet
    # (El script de Playwright leerá en tiempo real: Jugadores, Top 8, Historial de Verdes)
    jugadores_activos = 1800  # Ejemplo obtenido de pantalla
    verdes_previos = [2.25, 2.80] # Dos verdes ascendentes mayores a 2.16x
    top_8_apuestas = [120000, 95000, 70000, 50000, 35000, 25000, 18000, 12000] # Ordenados mayor a menor

    # 2. Validación de Filtros y Top 8 (Escalón por Escalón)
    if jugadores_activos < CONFIG_ESTRATEGIA["min_jugadores"]:
        return # Salta si no hay suficiente gente

    # Validación de Distancia Top 8
    valido_top_8 = True
    for i in range(len(top_8_apuestas) - 1):
        gap = top_8_apuestas[i] - top_8_apuestas[i+1]
        if gap > CONFIG_ESTRATEGIA["max_diferencia_escalon"]:
            valido_top_8 = False
            break

    if not valido_top_8 or top_8_apuestas[-1] < CONFIG_ESTRATEGIA["min_monto_p8"]:
        return # Si hay saltos muy bruscos o el puesto 8 es muy débil, no entra

    # 3. Decisión de Entrada Constante (Sin restricciones de mínimo de apuestas)
    monto_apuesta = CONFIG_ESTRATEGIA["monto_apuesta_base"]
    
    # Determinar objetivo de salida (Estandar o Extendido por Liquidez del Top 8)
    meta_cashout = CONFIG_ESTRATEGIA["cashout_estandar"]
    if top_8_apuestas[0] >= 150000 and jugadores_activos >= 2000:
        meta_cashout = CONFIG_ESTRATEGIA["cashout_extendido_liquidez"] # Deja correr si hay mucha masa pesada

    # Ejecución de la jugada constante en plataforma
    print(f"Ejecutando apuesta constante de {monto_apuesta} Bs. Meta de cobro: {meta_cashout}x")

async def main():
    print("Iniciando motor de @xMythos_bot...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
