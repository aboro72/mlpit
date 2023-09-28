import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton,
                             QFormLayout, QComboBox, QStackedWidget, QListWidget, QHBoxLayout, QMessageBox)
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Kunde, Ansprechpartner, \
    Adresse  # Importieren Sie die entsprechenden Modelle aus Ihrer models.py Datei

DATABASE_FILE_PATH = 'db.sqlite3'
engine = create_engine(f'sqlite:///{DATABASE_FILE_PATH}')
Session = sessionmaker(bind=engine)
session = Session()


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = QWidget()
        self.layout = QVBoxLayout(self.central_widget)

        self.stacked_widget = QStackedWidget()

        # Hauptmenü
        self.main_menu_widget = QWidget()
        self.main_menu_layout = QVBoxLayout(self.main_menu_widget)

        self.kunde_button = QPushButton('Kunden')
        self.kunde_button.clicked.connect(self.show_kunden_menu)

        self.main_menu_layout.addWidget(self.kunde_button)

        # Kundenmenü
        self.kunden_menu_widget = QWidget()
        self.kunden_menu_layout = QVBoxLayout(self.kunden_menu_widget)

        self.create_kunde_button = QPushButton('Kunde erstellen')
        self.create_kunde_button.clicked.connect(self.show_create_kunde_form)

        self.edit_kunde_button = QPushButton('Kunde bearbeiten')
        self.edit_kunde_button.clicked.connect(self.show_edit_kunde_form)

        self.show_kunde_button = QPushButton('Kunde anzeigen')
        self.show_kunde_button.clicked.connect(self.show_kunde)

        self.kunden_menu_layout.addWidget(self.create_kunde_button)
        self.kunden_menu_layout.addWidget(self.edit_kunde_button)
        self.kunden_menu_layout.addWidget(self.show_kunde_button)

        # Kundenformular
        self.kunde_form_widget = QWidget()
        self.kunde_form_layout = QFormLayout(self.kunde_form_widget)

        self.kunde_name_line_edit = QLineEdit()
        self.kunde_typ_combo_box = QComboBox()
        self.kunde_typ_combo_box.addItems(['Firma', 'Behörde'])

        self.kunde_form_layout.addRow('Name:', self.kunde_name_line_edit)
        self.kunde_form_layout.addRow('Typ:', self.kunde_typ_combo_box)

        self.save_kunde_button = QPushButton('Speichern')
        self.save_kunde_button.clicked.connect(self.save_kunde)

        self.kunde_form_layout.addWidget(self.save_kunde_button)

        # Stacked Widget
        self.stacked_widget.addWidget(self.main_menu_widget)
        self.stacked_widget.addWidget(self.kunden_menu_widget)
        self.stacked_widget.addWidget(self.kunde_form_widget)

        self.layout.addWidget(self.stacked_widget)

        self.setCentralWidget(self.central_widget)

    def show_kunden_menu(self):
        self.stacked_widget.setCurrentIndex(1)

    def show_create_kunde_form(self):
        self.stacked_widget.setCurrentIndex(2)

    def show_edit_kunde_form(self):
        # Hier können Sie ein Formular zum Bearbeiten von Kunden implementieren
        pass

    def show_kunde(self):
        # Hier können Sie eine Funktion implementieren, um Kundeninformationen anzuzeigen
        pass

    def save_kunde(self):
        name = self.kunde_name_line_edit.text()
        typ = self.kunde_typ_combo_box.currentText()

        if not name:
            QMessageBox.warning(self, 'Warnung', 'Name ist erforderlich!')
            return

        kunde = Kunde(name=name, typ=typ)
        session.add(kunde)
        session.commit()

        QMessageBox.information(self, 'Erfolg', 'Kunde erfolgreich gespeichert!')

        self.kunde_name_line_edit.clear()


app = QApplication(sys.argv)
window = MyApp()
window.show()
sys.exit(app.exec_())
