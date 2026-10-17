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
    "max_diferencia_escalon": 50000,     # Máximo salto permitido entre puestos consecutivos
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

async def main():
    print("Iniciando motor de @xMythos_bot...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
