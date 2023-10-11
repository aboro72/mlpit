import sys
import sqlite3
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap
import numpy as np

# SQLAlchemy setup
Base = declarative_base()
engine = create_engine('sqlite:///db.sqlite3')
Session = sessionmaker(bind=engine)
session = Session()

# Define Server and Schiene models
class Server(Base):
    __tablename__ = 'Server'
    id = Column(Integer, primary_key=True)
    status = Column(String)

class Schiene(Base):
    __tablename__ = 'Schiene'
    id = Column(Integer, primary_key=True)
    status = Column(String)

# Create tables if they do not exist
Base.metadata.create_all(engine)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.update_pie_chart()  # Initial pie chart update
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_pie_chart)
        self.timer.start(120000)  # Update pie chart every 2 minutes

    def initUI(self):
        self.setWindowTitle('Your App Title')
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        # Create a QLabel for displaying the pie chart
        self.pie_chart_label = QLabel()
        layout.addWidget(self.pie_chart_label)

        # Create a button for manual pie chart update
        generate_pie_chart_button = QPushButton('Generate Pie Chart')
        generate_pie_chart_button.clicked.connect(self.update_pie_chart)
        layout.addWidget(generate_pie_chart_button)

        # Add other widgets and functionality as needed

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def update_pie_chart(self):
        # Retrieve data from the database and generate pie charts using matplotlib
        # You can implement this functionality here

        # Example data for demonstration
        data = [30, 20, 10, 40]
        labels = ['Label1', 'Label2', 'Label3', 'Label4']

        plt.clf()  # Clear the previous plot
        plt.pie(data, labels=labels, autopct='%1.1f%%')
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle

        # Save the pie chart to an image file or display it in the QLabel
        image_path = 'pie_chart.png'
        plt.savefig(image_path)  # Save it to a file
        pixmap = QPixmap(image_path)  # Convert it to QPixmap

        self.pie_chart_label.setPixmap(pixmap)

def main():
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

if __name__ == '__main__':
    main()


class Schiene(Base):
    __tablename__ = 'Schiene'
    id = Column(Integer, primary_key=True)
    status = Column(String)


# Create tables if they do not exist
Base.metadata.create_all(engine)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Your App Title')
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        # Create buttons for generating pie charts, adding data, etc.
        generate_pie_chart_button = QPushButton('Generate Pie Chart')
        generate_pie_chart_button.clicked.connect(self.generate_pie_chart)
        layout.addWidget(generate_pie_chart_button)

        add_data_button = QPushButton('Add Data')
        add_data_button.clicked.connect(self.add_data)
        layout.addWidget(add_data_button)

        # Add other widgets and functionality as needed

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def generate_pie_chart(self):
        # Retrieve data from the database and generate pie charts using matplotlib
        # You can implement this functionality here

        # Example data for demonstration
        data = [30, 20, 10, 40]
        labels = ['Label1', 'Label2', 'Label3', 'Label4']

        plt.pie(data, labels=labels, autopct='%1.1f%%')
        plt.show()

    def add_data(self):
        # Implement data insertion functionality here
        # You can use PyQt5 widgets to take user input and insert it into the database

        # Example: Insert data into Server table
        new_server_status = 'Lager'
        new_server = Server(status=new_server_status)
        session.add(new_server)
        session.commit()

        # You can add error handling and validation as needed


def main():
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
