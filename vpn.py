import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QMessageBox, QComboBox
import subprocess
import time
import os


class VPNApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('VPN Control')
        self.setGeometry(100, 100, 300, 250)  # Increased height to accommodate the new button
        layout = QVBoxLayout()
        self.country_combobox = QComboBox(self)
        self.country_combobox.addItems(["US VPN", "Canada VPN", "Germany VPN", "France VPN", "Poland VPN", "UK VPN"])
        layout.addWidget(self.country_combobox)
        start_button = QPushButton('Start VPN', self)
        start_button.clicked.connect(self.start_vpn)
        layout.addWidget(start_button)
        stop_button = QPushButton('Stop VPN', self)
        stop_button.clicked.connect(self.stop_vpn)
        layout.addWidget(stop_button)
        delete_button = QPushButton('Delete VPN File', self)
        delete_button.clicked.connect(self.delete_vpn_file)  # Connect button to delete_vpn_file method
        layout.addWidget(delete_button)
        self.setLayout(layout)

    def get_username(self):
        self.name = os.environ['USERPROFILE']
        self.splitted_name = self.name.split('\\')
        return self.splitted_name[-1]

    def delete_vpn_file(self):
        try:
            if os.path.isfile(
                    f"C:\\Users\\{self.get_username()}\\AppData\\Roaming\\Microsoft\\Network\\Connections\\Pbk\\rasphone.pbk"):
                os.remove(
                    f"C:\\Users\\{self.get_username()}\\AppData\\Roaming\\Microsoft\\Network\\Connections\\Pbk\\rasphone.pbk")
                QMessageBox.information(self, 'VPN Status', 'VPN file deleted successfully.')
            else:
                QMessageBox.information(self, 'VPN Status', 'File not found.')
        except Exception as e:
            QMessageBox.critical(self, 'VPN Error', f'Error deleting VPN file: {str(e)}')

    def start_vpn(self):
        selected_country = self.country_combobox.currentText()
        QMessageBox.information(self, 'VPN Status', f'Starting {selected_country} VPN. Please wait...')
        try:
            self.create_and_connect_vpn(selected_country)
            QMessageBox.information(self, 'VPN Status', f'{selected_country} VPN connected successfully.')
        except Exception as e:
            QMessageBox.critical(self, 'VPN Error', f'Error starting VPN: {str(e)}')
            self.delete_vpn_file()  # Delete VPN file on unsuccessful connection

    def stop_vpn(self):
        QMessageBox.information(self, 'VPN Status', 'Stopping VPN. Please wait...')
        try:
            if os.path.isfile(
                    f"C:\\Users\\{self.get_username()}\\AppData\\Roaming\\Microsoft\\Network\\Connections\\Pbk\\rasphone.pbk"):
                self.disconnect_from_vpn()
                QMessageBox.information(self, 'VPN Status', 'VPN disconnected.')
            else:
                QMessageBox.information(self, 'VPN Status', 'Error in disconnection. Check if VPN is enabled.')
        except Exception as e:
            QMessageBox.critical(self, 'VPN Error', f'Error stopping VPN: {str(e)}')

    def create_and_connect_vpn(self, selected_country):
        country_servers = {
            "US VPN": "US2.vpnbook.com",
            "Canada VPN": "CA149.vpnbook.com",
            "Germany VPN": "DE20.vpnbook.com",
            "France VPN": "FR200.vpnbook.com",
            "Poland VPN": "PL134.vpnbook.com",
            "UK VPN": "UK205.vpnbook.com"
        }

        server_address = country_servers.get(selected_country, "")
        if not server_address:
            QMessageBox.warning(self, 'VPN Status', 'Select a country to connect to VPN.')
            return

        try:
            self.create_vpn_connection(selected_country, server_address)
            self.connect_to_vpn(selected_country, "vpnbook", "emw79zs")
        except Exception as e:
            raise RuntimeError(f"Failed to create and connect VPN: {str(e)}")

    def create_vpn_connection(self, connection_name, server_address):
        temp_content = f"[{connection_name}]\nMEDIA=rastapi\nPort=VPN2-0\nDevice=WAN Miniport (IKEv2)\nDEVICE=vpn\nPhoneNumber={server_address}"
        # Create temp.txt
        with open("temp.txt", "w") as temp_file:
            temp_file.write(temp_content)
        # Append temp.txt to rasphone.pbk
        subprocess.run(["type", "temp.txt", ">>",
                        f"C:\\Users\\{self.get_username()}\\AppData\\Roaming\\Microsoft\\Network\\Connections\\Pbk\\rasphone.pbk"],
                       shell=True)
        # Delete temp.txt
        subprocess.run(["del", "temp.txt"], shell=True)
        time.sleep(5)

    def connect_to_vpn(self, connection_name, username, password):
        subprocess.run(["rasdial", connection_name, username, password], shell=True)

    def disconnect_from_vpn(self):
        subprocess.run(["rasdial", "/DISCONNECT"], shell=True)
        if os.path.isfile(
                f"C:\\Users\\{self.get_username()}\\AppData\\Roaming\\Microsoft\\Network\\Connections\\Pbk\\rasphone.pbk"):
            os.remove(
                f"C:\\Users\\{self.get_username()}\\AppData\\Roaming\\Microsoft\\Network\\Connections\\Pbk\\rasphone.pbk")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VPNApp()
    window.show()
    sys.exit(app.exec_())
