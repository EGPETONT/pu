
import unittest
import argparse
from unittest.mock import patch, MagicMock
from io import StringIO
import sys
import os
from contextlib import redirect_stdout

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
# Импорт ваших классов PortInfo, PortScanner, TerminalInterface
from pu.pu import PortInfo, PortScanner, TerminalInterface

class TestPortInfo(unittest.TestCase):
    def test_port_info(self):
        # Создаем экземпляр PortInfo с известным портом
        port_info = PortInfo(80)

        # Проверяем, что PID, имя процесса и путь к исполняемому файлу возвращаются
        self.assertIsNotNone(port_info.pid)
        self.assertIsNotNone(port_info.name)
        self.assertIsNotNone(port_info.path_to_bin)

class TestPortScanner(unittest.TestCase):
    def test_port_scanner(self):
        # Создаем экземпляр PortScanner
        scanner = PortScanner()

        # Проверяем, что сканирование портов работает
        scanner.scan_ports()
        port_dict = scanner.get_port_dict()

        # Проверяем, что словарь не пустой
        self.assertGreater(len(port_dict), 0)

class TestTerminalInterface(unittest.TestCase):
    @patch('sys.stdout', new_callable=StringIO)
    def test_terminal_interface_help(self, mock_stdout):
        # Создаем экземпляр TerminalInterface
        terminal = TerminalInterface()

        # Имитируем ввод аргументов командной строки
        with patch.object(sys, 'argv', ['pu', '--help']):
            # Проверяем, что вывод справки работает
            with self.assertRaises(SystemExit):
                terminal.run()

        # Проверяем, что выведена справка
        self.assertIn('usage: pu', mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_terminal_interface_scan(self, mock_stdout):
        # Создаем экземпляр TerminalInterface
        terminal = TerminalInterface()

        # Имитируем ввод аргументов командной строки
        with patch.object(sys, 'argv', ['pu', '--scan']):
            # Проверяем, что вывод информации о портах работает
            terminal.run()

            # Проверяем, что выведена таблица
            self.assertIn('Port', mock_stdout.getvalue())
            self.assertIn('PID', mock_stdout.getvalue())
            self.assertIn('Process Name', mock_stdout.getvalue())
            self.assertIn('Path to Binary', mock_stdout.getvalue())

if __name__ == "__main__":
    unittest.main()