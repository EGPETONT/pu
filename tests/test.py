import psutil
import argparse
from tabulate import tabulate

class PortInfo:
    def __init__(self, port):
        self.port = port

    @property
    def pid(self):
        try:
            for conn in psutil.net_connections(kind='inet'):
                if conn.laddr.port == self.port and conn.status == 'LISTEN':
                    return conn.pid
        except Exception as e:
            print(f"Error getting PID for port {self.port}: {e}")
        return None

    @property
    def name(self):
        pid = self.pid
        if pid is not None:
            try:
                process = psutil.Process(pid)
                return process.name()
            except psutil.NoSuchProcess:
                return 'Unknown'
        return 'Unknown'

    @property
    def path_to_bin(self):
        pid = self.pid
        if pid is not None:
            try:
                process = psutil.Process(pid)
                return process.exe()
            except psutil.NoSuchProcess:
                return 'Unknown'
        return 'Unknown'

    def __str__(self):
        return f"Port: {self.port}, PID: {self.pid}, Process Name: {self.name}, Path to Binary: {self.path_to_bin}"



class PortScanner:
    def __init__(self):
        self.port_dict = {}

    def scan_ports(self):
        for conn in psutil.net_connections(kind='inet'):
            if conn.status == 'LISTEN':
                port = conn.laddr.port
                if port not in self.port_dict:
                    self.port_dict[port] = PortInfo(port)

    def get_port_dict(self):
        return self.port_dict

# # Пример использования класса
# scanner = PortScanner()
# scanner.scan_ports()
# port_dict = scanner.get_port_dict()
# print(port_dict)
# # Вывод результатов
# for port, info in port_dict.items():
#     print(info)

class TerminalInterface:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog='pu',
            description='Scan ports and display information.',
            epilog='Example: pu --scan'
        )
        self.parser.add_argument('--scan', action='store_true', help='Scan ports and display information')
        self.parser.add_argument('--version', action='version', version='%(prog)s 1.0')

    def run(self):
        args = self.parser.parse_args()

        if args.scan:
            scanner = PortScanner()
            scanner.scan_ports()
            port_dict = scanner.get_port_dict()

            # Формируем данные для таблицы
            table_data = []
            for port, info in port_dict.items():
                table_data.append([port, info.pid, info.name, info.path_to_bin])

            # Заголовки таблицы
            headers = ['Port', 'PID', 'Process Name', 'Path to Binary']

            # Выводим таблицу
            print(tabulate(table_data, headers, tablefmt="grid"))
        else:
            self.parser.print_help()

if __name__ == "__main__":
    terminal = TerminalInterface()
    terminal.run()