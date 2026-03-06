import asyncio
import random

async def get_charger_status(charger_id : str, sem : asyncio.Semaphere):
     async with sem:
        print(f"🔗 正在尝试连接[{charger_id}]....")
        if charger_id == '4':
            raise RuntimeError(f"⚠️ {charger_id}的硬件通讯中断!")
        
        delay = random(1,3)
        await asyncio.sleep(delay)

        return charger_id, random.randint(0, 100)
     
