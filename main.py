import os
import pyfiglet
import datetime
import requests
import valclient
from termcolor import colored


client = valclient.Client(region='br')
client.activate()

token = client.fetch('/entitlements/v1/token', 'local')["accessToken"]
info = requests.get('https://auth.riotgames.com/userinfo', headers={'Authorization': f'Bearer {token}'}).json()


# Valores especificos
print()
print(pyfiglet.figlet_format("VALInfo", font="Bloody", width=100))
print(f'{colored("Name:", "grey", attrs=["bold"])} {colored(info["acct"]["game_name"], "red")}{colored("#", "light_grey")}{colored(info["acct"]["tag_line"], "light_red", "on_light_grey")}')
print(f'{colored("Player Locale:", "grey", attrs=["bold"])} {colored(info.get("player_locale", "N/ "), "cyan")}')
print(f'{colored("Created At:", "grey", attrs=["bold"])} {colored(datetime.datetime.fromtimestamp(info["acct"]["created_at"] / 1000).strftime("%Y-%m-%d %H:%M:%S"), "cyan")}')
if 'age' in info:
    age = info["age"]
    age_formatted = datetime.datetime.fromisoformat(age).strftime('%Y-%m-%d')
    print(f'{colored("Age:", attrs=["bold"])} {colored(age_formatted, "cyan")}')
else:
    print(f'{colored("Age:", "grey", attrs=["bold"])} {colored("None", "green")}')
print(f'{colored("Email Verified:", "grey", attrs=["bold"])} {colored(info["email_verified"], "green")}')
print(f'{colored("Phone Number Verified:", "grey", attrs=["bold"])} {colored(info["phone_number_verified"], "green")}')
print()


# Todos os valores
print()
print(pyfiglet.figlet_format("VALInfo", font="Bloody", width=100))
user_input = input(colored('Return all values? (yes/no): ', 'magenta'))
if user_input.lower() == 'yes':
    os.system('cls')
    print("\n" * 2)
    print(colored('ALL VALUES', 'green'))
    for field, value in info.items():
        formatted_field = colored(field.capitalize(), 'grey', attrs=['bold'])
        if field == 'acct' and 'created_at' in value:
            value['created_at'] = datetime.datetime.fromtimestamp(value['created_at'] / 1000).strftime('%Y-%m-%d %H:%M:%S')
            formatted_value = colored(value, 'cyan')
        elif field == 'pw' and 'cng_at' in value:
            value['cng_at'] = datetime.datetime.fromtimestamp(value['cng_at'] / 1000).strftime('%Y-%m-%d %H:%M:%S')
            formatted_value = colored(value, 'cyan')
        elif isinstance(value, bool) or value is None:
            formatted_value = colored(value, 'green')
        else:
            formatted_value = colored(value, 'cyan')
        print(f'{formatted_field}: {formatted_value}')
