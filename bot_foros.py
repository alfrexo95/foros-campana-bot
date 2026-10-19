import requests
import random
from datetime import datetime

# --- CONFIGURACIÓN ---
PAYMENT_ADDRESSES = """
₿ BTC: bc1qt3rukpe7qp737zj5j5xpxxmcqv90cfefhg5e00
Ξ ETH: 0xA5E6eB31868A85127B1ED82b8C760193356206ED
Ł LTC: ltc1qdyyg99l8ehp9aj4ehzvmefglmpl9750226k7ne
⚡ Lightning: chieftrait089@walletofsatoshi.com
"""

MENSAJES = [
    f"""🚨 Help Cuban Families Survive the Crisis 🇨🇺

The economic crisis is pushing vulnerable families to the brink. Famine and lack of medicine are daily realities. We are using decentralized tech to deliver food and medical supplies directly to those in need, bypassing traditional blockades.

If you can help, here are our official donation addresses:
{PAYMENT_ADDRESSES}

Every sat and every fraction of a coin helps. Thank you for your solidarity. 🙏""",

    f"""🌍 Decentralized Solidarity for Cuba

Traditional international aid is often blocked or delayed. We are using Bitcoin and other cryptocurrencies to create a direct, peer-to-peer channel to send relief to families facing severe shortages of food and medicine.

Accepted donations:
{PAYMENT_ADDRESSES}

Transparency is key. We document everything. Follow our journey and see the impact of your support. #Bitcoin #Cuba #Solidarity""",

    f"""🇨🇺 Direct Relief for Vulnerable Communities

Poverty and hunger should not exist in the 21st century. In Cuba, vulnerable families are struggling for basic necessities. We bypass the middlemen to ensure aid goes directly to those who need it most.

You can support our mission here:
{PAYMENT_ADDRESSES}

Please upvote or share to help us reach more people. Thank you! ⚡"""
]

def publicar_en_botchan(mensaje):
    print("  📤 Publicando en Botchan (intcount)...")
    url = "https://free.intcount.com/api/botchan/post"
    payload = {"content": mensaje, "tag": "meta"}
    try:
        res = requests.post(url, json=payload, timeout=15)
        if res.status_code in [200, 201]:
            print("  ✅ Publicado con éxito en Botchan.")
            return True
        else:
            print(f"  ❌ Error en Botchan: {res.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ Error de conexión Botchan: {e}")
        return False

def publicar_en_anystation(mensaje):
    print("  📤 Publicando en AnyStation...")
    url = "https://anystation.net/"
    try:
        # AnyStation suele aceptar form-data o texto plano
        res = requests.post(url, data={"content": mensaje}, timeout=15)
        if res.status_code in [200, 201, 302]:
            print("  ✅ Publicado con éxito en AnyStation.")
            return True
        else:
            print(f"  ❌ Error en AnyStation: {res.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ Error de conexión AnyStation: {e}")
        return False

def main():
    print(f"🚀 Iniciando ciclo de publicación - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Elegir un mensaje aleatorio para no ser detectado como spam
    mensaje_elegido = random.choice(MENSAJES)
    print(f"📝 Mensaje seleccionado (primeros 50 caracteres): {mensaje_elegido[:50]}...")
    
    # Publicar en las plataformas
    exito_botchan = publicar_en_botchan(mensaje_elegido)
    exito_anystation = publicar_en_anystation(mensaje_elegido)
    
    if exito_botchan or exito_anystation:
        print("✅ Ciclo completado con al menos una publicación exitosa.")
    else:
        print("⚠️ No se pudo publicar en ninguna plataforma en este ciclo.")

if __name__ == "__main__":
    main()
