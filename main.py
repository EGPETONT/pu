import subprocess
import re

import os
import platform
from tabulate import tabulate

class SystemInfo:
    def __init__(self):
        self.system = platform.system()
        self.node = platform.node()
        self.release = platform.release()
        self.version = platform.version()
        self.machine = platform.machine()
        self.processor = platform.processor()
        self.cpu_count = os.cpu_count()

class SystemInfoPrinter:
    def __init__(self, system_info):
        self.system_info = system_info

    def print_info(self):
        # Создаем список с информацией о системе
        table_data = [
            ["System", self.system_info.system],
            ["Node", self.system_info.node],
            ["Release", self.system_info.release],
            ["Version", self.system_info.version],
            ["Machine", self.system_info.machine],
            ["Processor", self.system_info.processor],
            ["CPU Count", self.system_info.cpu_count]
        ]

        # Выводим информацию в виде таблицы
        print(tabulate(table_data, headers=["Property", "Value"], tablefmt="grid"))



class SocketInfo:
    def __init__(self):
        self.sockets = self._get_socket_info()

    def _get_socket_info(self):
        # Запуск команды ss и получение вывода
        result = subprocess.run(['ss', '-tunap'], stdout=subprocess.PIPE)
        # Декодирование и разбиение вывода на строки
        output_lines = result.stdout.decode('utf-8').strip().split('\n')
        # Парсинг и форматирование вывода
        sockets = []
        for line in output_lines[1:]:  # Пропускаем заголовок
            parts = line.strip().split()
            sockets.append({
                'state': parts[0],
                'recv-q': parts[1],
                'send-q': parts[2],
                'local_address': parts[3],
                'peer': parts[4],
                'process': parts[5] if len(parts) > 5 else None
            })
        return sockets

    def get_all_sockets(self):
        return self.sockets

class SocketFileInfo:
    def __init__(self):
        self.socket_info = SocketInfo()

    def get_socket_file_info(self):
        sockets = self.socket_info.get_all_sockets()
        socket_file_info = []

        for sock in sockets:
            # Извлекаем PID из поля 'process'
            pid_match = re.search(r'\((\d+)\)', sock['process'])
            if pid_match:
                pid = pid_match.group(1)
                # Получаем информацию о файлах, используемых процессом
                file_info = self._get_file_info_for_pid(pid)
                socket_file_info.append({
                    'pid': pid,
                    'socket': sock,
                    'file_info': file_info
                })

        return socket_file_info

    def _get_file_info_for_pid(self, pid):
        # Запуск команды lsof и получение вывода
        result = subprocess.run(['lsof', '-p', pid], stdout=subprocess.PIPE)
        # Декодирование и разбиение вывода на строки
        output_lines = result.stdout.decode('utf-8').strip().split('\n')
        # Парсинг и форматирование вывода
        file_info = []
        for line in output_lines[1:]:  # Пропускаем заголовок
            parts = line.strip().split()
            file_info.append({
                'command': parts[0],
                'pid': parts[1],
                'user': parts[2],
                'fd': parts[3],
                'type': parts[4],
                'device': parts[5],
                'size/off': parts[6],
                'node': parts[7],
                'name': parts[8]
            })
        return file_info

# Пример использования
info = SocketFileInfo()
socket_file_info = info.get_socket_file_info()
print(socket_file_info)
for item in socket_file_info:
    print(f"PID: {item['pid']}, Socket: {item['socket']}, File Info: {item['file_info']}")

# Пример использования
info = SocketInfo()
all_sockets = info.get_all_sockets()
for sock in all_sockets:
    print(sock)

# Пример использования
system_info = SystemInfo()
printer = SystemInfoPrinter(system_info)
printer.print_info()