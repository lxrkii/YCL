import sys
import os
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QTextEdit,
    QPushButton, QListWidget, QHBoxLayout, QFileDialog, QLineEdit
)
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import QDateTime

DATA_DIR = "diary_entries"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

class DiaryApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Beautiful Diary")
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet("background-color: #1e1e2f; color: #f1f1f1;")
        self.entries = {}
        self.current_filename = None
        self.init_ui()
        self.load_all_entries()

    def init_ui(self):
        layout = QHBoxLayout()

        self.entry_list = QListWidget()
        self.entry_list.setStyleSheet("font-size: 16px; padding: 10px; background-color: #2c2c3c; color: white;")
        self.entry_list.itemClicked.connect(self.load_entry)

        right_layout = QVBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search entries...")
        self.search_input.setStyleSheet("font-size: 16px; padding: 8px; background-color: #333; color: white;")
        self.search_input.textChanged.connect(self.filter_entries)

        self.entry_text = QTextEdit()
        self.entry_text.setFont(QFont("Arial", 14))
        self.entry_text.setStyleSheet("background-color: #29293d; padding: 10px; color: #f1f1f1; border: 1px solid #444;")

        button_layout = QHBoxLayout()

        self.save_button = QPushButton("Save Entry")
        self.save_button.setStyleSheet("background-color: #5f9ea0; color: white; font-size: 16px; padding: 10px;")
        self.save_button.clicked.connect(self.save_entry)

        self.new_button = QPushButton("New Entry")
        self.new_button.setStyleSheet("background-color: #4682b4; color: white; font-size: 16px; padding: 10px;")
        self.new_button.clicked.connect(self.new_entry)

        self.export_button = QPushButton("Export to File")
        self.export_button.setStyleSheet("background-color: #708090; color: white; font-size: 16px; padding: 10px;")
        self.export_button.clicked.connect(self.export_entry)

        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.new_button)
        button_layout.addWidget(self.export_button)

        right_layout.addWidget(self.search_input)
        right_layout.addWidget(self.entry_text)
        right_layout.addLayout(button_layout)

        layout.addWidget(self.entry_list, 2)
        layout.addLayout(right_layout, 5)

        self.setLayout(layout)

    def new_entry(self):
        timestamp = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm")
        self.entry_list.addItem(timestamp)
        self.entries[timestamp] = ""
        self.entry_list.setCurrentRow(self.entry_list.count() - 1)
        self.entry_text.clear()
        self.current_filename = os.path.join(DATA_DIR, f"{timestamp}.json")

    def save_entry(self):
        current_item = self.entry_list.currentItem()
        if current_item:
            text = self.entry_text.toPlainText()
            self.entries[current_item.text()] = text
            entry_data = {
                "timestamp": current_item.text(),
                "content": text
            }
            filename = os.path.join(DATA_DIR, f"{current_item.text()}.json")
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(entry_data, f, indent=4)

    def load_entry(self, item):
        filename = os.path.join(DATA_DIR, f"{item.text()}.json")
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.entry_text.setText(data.get("content", ""))
                self.current_filename = filename

    def export_entry(self):
        current_item = self.entry_list.currentItem()
        if current_item:
            text = self.entries.get(current_item.text(), "")
            filename, _ = QFileDialog.getSaveFileName(self, "Export Entry", f"{current_item.text()}.txt", "Text Files (*.txt)")
            if filename:
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write(f"{current_item.text()}\n\n{text}")

    def load_all_entries(self):
        self.entries.clear()
        self.entry_list.clear()
        for file in sorted(os.listdir(DATA_DIR)):
            if file.endswith(".json"):
                filepath = os.path.join(DATA_DIR, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    timestamp = data.get("timestamp")
                    content = data.get("content", "")
                    self.entries[timestamp] = content
                    self.entry_list.addItem(timestamp)

    def filter_entries(self, text):
        self.entry_list.clear()
        for timestamp in sorted(self.entries):
            if text.lower() in timestamp.lower() or text.lower() in self.entries[timestamp].lower():
                self.entry_list.addItem(timestamp) 