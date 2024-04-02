import subprocess
from tabulate import tabulate

class WebServerSocketInspector:
    def __init__(self, web_server_name):
        self.web_server_name = web_server_name

    def get_web_server_sockets(self):
        # Выполняем команду ss и фильтруем результаты
        try:
            ss_output = subprocess.check_output(['ss', '-tuln']).decode('utf-8').strip().split('\n')[1:]
            web_server_sockets = [line.split() for line in ss_output if self.web_server_name in line]
            return web_server_sockets
        except subprocess.CalledProcessError as e:
            print(f"Ошибка при выполнении команды: {e}")
            return []

    def print_web_server_sockets(self):
        sockets = self.get_web_server_sockets()
        headers = ["State", "Recv-Q", "Send-Q", "Local Address:Port", "Peer Address:Port", "Process"]
        print(tabulate(sockets, headers=headers))

# Использование класса
web_server_name = 'apache'  # Замените на имя вашего веб-сервера, если оно отличается
inspector = WebServerSocketInspector(web_server_name)
inspector.print_web_server_sockets()