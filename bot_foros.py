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

# 10 Mensajes persuasivos en inglés para rotar
MENSAJES = [
    f"""🚨 **Help Cuban Families Survive the Crisis** 🇨🇺\n\nThe economic crisis is pushing vulnerable families to the brink. Famine and lack of medicine are daily realities. We use decentralized tech to deliver food and medical supplies directly to those in need.\n\n{PAYMENT_ADDRESSES}\n\nEvery sat helps. Please share. 🙏""",
    f"""🌍 **Decentralized Solidarity in Action**\n\nTraditional international aid is often blocked. We use Bitcoin and crypto to create a direct, peer-to-peer channel for relief. Transparency is key: we document everything.\n\n{PAYMENT_ADDRESSES}\n\nThank you for your support! ⚡""",
    f"""🇨🇺 **Direct Relief for Vulnerable Communities**\n\nPoverty and hunger should not exist in the 21st century. We bypass the middlemen to ensure aid goes directly to families struggling for basic necessities in Cuba.\n\n{PAYMENT_ADDRESSES}\n\nPlease upvote or share to help us reach more people. 💪""",
    f"""💡 **Why Crypto for Cuba?**\n\nBecause banks fail, but peer-to-peer networks don't. When traditional transfers are blocked, Bitcoin and Lightning Network keep the flow of aid moving. We are building a lifeline from the global community to those who need it most.\n\n{PAYMENT_ADDRESSES}\n\nSupport freedom tech. 🔑""",
    f"""🔥 **The Reality on the Ground**\n\nFamilies in Cuba are facing severe shortages of food and medicine. We are using decentralized networks to bypass censorship and deliver help directly to them.\n\n{PAYMENT_ADDRESSES}\n\nIf you can't donate, a repost helps us immensely. 🌍""",
    f"""⚡ **Lightning Fast Relief**\n\nThanks to the Lightning Network, we can send funds to Cuba in seconds with near-zero fees. Your sats become food and medicine for vulnerable families.\n\n{PAYMENT_ADDRESSES}\n\nJoin the mission. 🚀""",
    f"""🤝 **Community Over Everything**\n\nThis is what decentralized solidarity looks like. A global community coming together to help those facing a local crisis. We document every step of the way.\n\n{PAYMENT_ADDRESSES}\n\nThank you for standing with Cuba. 🇨🇺""",
    f"""🛡️ **Building a Lifeline**\n\nWhen the internet is censored and banks are blocked, crypto is the only way out. We are using BTC, ETH, LTC, and Lightning to deliver direct aid to Cuban families.\n\n{PAYMENT_ADDRESSES}\n\nBe part of the solution. ⚡""",
    f"""🔗 **Transparency and Proof**\n\nWe don't just ask for money; we show you the reality. Every donation is documented and goes directly to families in need. Check the evidence below.\n\n{PAYMENT_ADDRESSES}\n\nHelp us keep the momentum going. 🙏""",
    f"""🌐 **A Global Effort**\n\nFrom the US to Europe to Latin America, people are using crypto to help Cuba. You can make a difference from anywhere in the world.\n\n{PAYMENT_ADDRESSES}\n\nEvery donation counts. Thank you! 💙"""
]

def obtener_media_aleatoria():
    """Busca archivos en la carpeta media de FondosAngor y devuelve una URL RAW."""
    print("  🔍 Buscando evidencia multimedia en FondosAngor...")
    api_url = "https://api.github.com/repos/alfrexo95/FondosAngor/contents/media"
    try:
        res = requests.get(api_url, timeout=10)
        if res.status_code == 200:
            files = res.json()
            media_files = [f for f in files if f['name'].lower().endswith(('.jpg', '.jpeg', '.png', '.mp4'))]
            if media_files:
                selected = random.choice(media_files)
                url = selected['download_url']
                print(f"  ✅ Evidencia encontrada: {selected['name']}")
                # Formato Markdown (si es video, se muestra como enlace, si es imagen, se incrusta)
                if selected['name'].lower().endswith('.mp4'):
                    return f"[▶️ **Watch Video Evidence Here**]({url})"
                else:
                    return f"![Evidence]({url})"
    except Exception as e:
        print(f"  ⚠️ Error buscando media: {e}")
    return "" # Si falla, devuelve vacío

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
    
    # 1. Elegir mensaje y obtener media
    mensaje_base = random.choice(MENSAJES)
    media_markdown = obtener_media_aleatoria()
    
    # 2. Unir todo
    mensaje_final = f"{mensaje_base}\n\n{media_markdown}"
    
    print(f"📝 Mensaje preparado (primeros 60 caracteres): {mensaje_base[:60]}...")
    if media_markdown:
        print(f"📸 Evidencia adjunta: {media_markdown[:50]}...")
    
    # 3. Publicar
    exito_botchan = publicar_en_botchan(mensaje_final)
    exito_anystation = publicar_en_anystation(mensaje_final)
    
    if exito_botchan or exito_anystation:
        print("✅ Ciclo completado con al menos una publicación exitosa.")
    else:
        print("⚠️ No se pudo publicar en ninguna plataforma en este ciclo.")

if __name__ == "__main__":
    main()
