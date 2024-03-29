try:
    import os
    import tls_client
    import random
    import string
    import requests
    import json
except ModuleNotFoundError:
    i = 0
    imports = [
        "requests",
        "tls_client",
    ]
    for _import in imports:
        i += 1
        print(f"Installing dependencies... ({i}/2)")
        print(f"installing {_import}")
        os.system(f'pip install {_import} > nul')
    import tls_client
    import random
    import string
    import requests


class Files:
    @staticmethod
    def write_config():
        if not os.path.exists("config.json"):
            data = {
                "Proxies": False,
                "Custom_Password": False,
                "Password": ""
            }
            with open("config.json", "w") as f:
                json.dump(data, f, indent=4)

    @staticmethod
    def write_files():
        files = [
            "combo.txt", 
            "proxies.txt",
            "new_combo.txt"
        ]
        for file in files:
            if not os.path.exists(file):
                with open(f"{file}", "a") as f:
                    f.close()

    @staticmethod
    def run_tasks():
        tasks = [Files.write_config, Files.write_files]
        for task in tasks:
            task()

Files.run_tasks()

session = tls_client.Session(client_identifier="chrome_120",random_tls_extension_order=True)

with open("proxies.txt") as f:
    proxies = f.read().splitlines()

with open("config.json") as f:
    Config = json.load(f)

proxy = Config["Proxies"]
Password = Config["Password"]
Custom_Password = Config["Custom_Password"]

if proxy:
    session.proxies = {
        "http": f"http://{random.choice(proxies)}",
        "https": f"http://{random.choice(proxies)}",
    }

class Change:
    def get_random_str(self, length: int) -> str:
        return "".join(
            random.choice(string.ascii_letters + string.digits) for _ in range(length)
        )

    def get_discord_cookies(self):
        try:
            response = requests.get("https://canary.discord.com")
            match response.status_code:
                case 200:
                    return "; ".join(
                        [f"{cookie.name}={cookie.value}" for cookie in response.cookies]
                    ) + "; locale=en-US"
                case _:
                    return "__dcfduid=4e0a8d504a4411eeb88f7f88fbb5d20a; __sdcfduid=4e0a8d514a4411eeb88f7f88fbb5d20ac488cd4896dae6574aaa7fbfb35f5b22b405bbd931fdcb72c21f85b263f61400; __cfruid=f6965e2d30c244553ff3d4203a1bfdabfcf351bd-1699536665; _cfuvid=rNaPQ7x_qcBwEhO_jNgXapOMoUIV2N8FA_8lzPV89oM-1699536665234-0-604800000; locale=en-US"
        except Exception as e:
            print(e)
        
    def Headers(self, token):
        return {
            'authority': 'discord.com',
            'accept': '*/*',
            'accept-language': 'en',
            'authorization': token,
            'content-type': 'application/json',
            'cookie': self.get_discord_cookies(),
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
            'x-debug-options': 'bugReporterEnabled',
            'x-discord-locale': 'en',
            'x-discord-timezone': 'Europe/Warsaw',
            'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6InBsIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEyMC4wLjAuMCBTYWZhcmkvNTM3LjM2IEVkZy8xMjAuMC4wLjAiLCJicm93c2VyX3ZlcnNpb24iOiIxMjAuMC4wLjAiLCJvc192ZXJzaW9uIjoiMTAiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MjU2MjMxLCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ==',
        }
    
    def Changer(self, token, password, email, new_pass):
        try:
            
            headers = self.Headers(token)

            data = {
                'password': password,
                'new_password': new_pass,
            }

            response = session.patch('https://discord.com/api/v9/users/@me', headers=headers, json=data)
            if response.status_code == 200:
                new_token = response.json()['token']
                print(f"(+): Changed ({email}) → {new_token}")
                return f'69:{email}:{new_pass}:{new_token}'
            elif response.status_code == 40002:
                print(f"(!): Couldn't Change {email} → {token} is locked")
                return f'07:{email}:{password}:{token}'
            else:
                print(f"(!): Failed to change for → ({email})")
                return f'07:{email}:{password}:{token}'
        except Exception as e: 
            print(e)   
    
if __name__ == "__main__":
    with open(f"combo.txt") as f:
        combo = f.read().splitlines()
    combo = list(set(combo))
    if len(combo) == 0:
        input("bruh paste combo into combo.txt lol")

    if Custom_Password:
        new_pass = Password
    else:
        new_pass = Change().get_random_str(20)

    for account in combo:
        email = account.split(':')[0]
        password = account.split(':')[1]
        token = account.split(':')[2]

        new_combo = Change().Changer(token, password, email, new_pass)
        if new_combo.split(':')[0] == '69':
            with open('new_combo.txt', 'a') as f:
                f.write(new_combo.split(':')[1] + ':' + new_combo.split(':')[2] + ':' + new_combo.split(':')[3] + '\n')
        else:
            with open('failed.txt', 'a') as f:
                f.write(new_combo.split(':')[1] + ':' + new_combo.split(':')[2] + ':' + new_combo.split(':')[3] + '\n')
    input("done")
