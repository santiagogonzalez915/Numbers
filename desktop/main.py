
import sys
import copy
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QComboBox, QFrame, QGridLayout, QListWidget
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QPalette, QColor, QPainter, QBrush, QPen
from backend.core.create import createGame, applyMove

class CircularButton(QPushButton):
    def __init__(self, text="", size=60, color=QColor(70, 130, 180), text_color=QColor(255, 255, 255)):
        super().__init__(text)
        self.size = size
        self.color = color
        self.text_color = text_color
        self.setFixedSize(size, size)
        self.setStyleSheet("""
            QPushButton {
                border: none;
                border-radius: """ + str(size//2) + """px;
                background-color: """ + color.name() + """;
                color: """ + text_color.name() + """;
                font-weight: bold;
                font-size: """ + str(size//3) + """px;
            }
            QPushButton:hover {
                background-color: """ + color.lighter(120).name() + """;
            }
            QPushButton:pressed {
                background-color: """ + color.darker(120).name() + """;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)

class OperationButton(CircularButton):
    def __init__(self, text="", size=40):
        super().__init__(text, size, QColor(255, 140, 0), QColor(255, 255, 255))

class UndoButton(CircularButton):
    def __init__(self, size=40):
        super().__init__("↶", size, QColor(220, 20, 60), QColor(255, 255, 255))

class NumbersGameWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.difficulty = 1
        self.state = createGame(difficulty=self.difficulty)
        self.history_stack = []  
        self.selected_number1 = None
        self.selected_number2 = None
        self.selected_operation = None
        self.number_buttons = []
        self.operation_buttons = []
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Numbers Game (PyQt5)")
        self.setGeometry(100, 100, 1000, 600)
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                font-family: Arial, sans-serif;
            }
        """)
        
        
        main_layout = QHBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        game_layout = QVBoxLayout()
        game_layout.setSpacing(20)
        
        difficulty_frame = QFrame()
        difficulty_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        difficulty_layout = QHBoxLayout()
        difficulty_layout.setSpacing(10)
        difficulty_label = QLabel("Difficulty:")
        difficulty_layout.addWidget(difficulty_label)
        self.difficulty_buttons = {}
        for label, level in zip(["Easy", "Medium", "Hard"], [1, 2, 3]):
            btn = QPushButton(label)
            btn.setCheckable(True)
            btn.setStyleSheet(self.difficulty_button_style(selected=(level==self.difficulty)))
            btn.clicked.connect(lambda checked, lvl=level: self.set_difficulty(lvl))
            self.difficulty_buttons[level] = btn
            difficulty_layout.addWidget(btn)
        difficulty_layout.addStretch()
        difficulty_frame.setLayout(difficulty_layout)
        game_layout.addWidget(difficulty_frame)
        
        target_frame = QFrame()
        target_frame.setStyleSheet("""
            QFrame {
                background-color: #4CAF50;
                border-radius: 15px;
                padding: 20px;
            }
        """)
        target_layout = QVBoxLayout()
        self.target_label = QLabel(f"Target: {self.state['target']}")
        self.target_label.setAlignment(Qt.AlignCenter)
        self.target_label.setFont(QFont("Arial", 28, QFont.Bold))
        self.target_label.setStyleSheet("color: white;")
        target_layout.addWidget(self.target_label)
        target_frame.setLayout(target_layout)
        game_layout.addWidget(target_frame)
        
        numbers_frame = QFrame()
        numbers_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                padding: 20px;
            }
        """)
        numbers_layout = QGridLayout()
        numbers_layout.setSpacing(15)
        
        self.number_buttons = []
        for i, number in enumerate(self.state['numbers']):
            row = i // 3
            col = i % 3
            button = CircularButton(str(number), 80)
            button.clicked.connect(lambda checked, btn=button: self.on_number_clicked(btn))
            self.number_buttons.append(button)
            numbers_layout.addWidget(button, row, col)
        
        numbers_frame.setLayout(numbers_layout)
        game_layout.addWidget(numbers_frame)
        
        operations_frame = QFrame()
        operations_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                padding: 20px;
            }
        """)
        operations_layout = QHBoxLayout()
        operations_layout.setSpacing(15)
        
        operations = ['+', '-', '×', '÷']
        self.operation_buttons = []
        for op in operations:
            button = OperationButton(op, 50)
            button.clicked.connect(lambda checked, operation=op: self.on_operation_clicked(operation))
            self.operation_buttons.append(button)
            operations_layout.addWidget(button)
        
        self.undo_btn = UndoButton(50)
        self.undo_btn.clicked.connect(self.undo_move)
        self.undo_btn.setEnabled(False)
        operations_layout.addWidget(self.undo_btn)
        
        operations_layout.addStretch()
        operations_frame.setLayout(operations_layout)
        game_layout.addWidget(operations_frame)
        
        control_frame = QFrame()
        control_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        control_layout = QHBoxLayout()
        
        self.new_game_btn = QPushButton("New Game")
        self.new_game_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        self.new_game_btn.clicked.connect(self.new_game)
        control_layout.addWidget(self.new_game_btn)
        
        control_layout.addStretch()
        control_frame.setLayout(control_layout)
        game_layout.addWidget(control_frame)
        
        self.feedback_label = QLabel("Click a number, then an operation, then another number")
        self.feedback_label.setAlignment(Qt.AlignCenter)
        self.feedback_label.setFont(QFont("Arial", 14))
        self.feedback_label.setStyleSheet("""
            QLabel {
                background-color: white;
                border-radius: 10px;
                padding: 15px;
                color: #333;
            }
        """)
        game_layout.addWidget(self.feedback_label)
        
        main_layout.addLayout(game_layout, 2)  
        
        history_frame = QFrame()
        history_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                padding: 20px;
            }
        """)
        history_layout = QVBoxLayout()
        history_label = QLabel("Move History:")
        history_label.setFont(QFont("Arial", 14, QFont.Bold))
        history_layout.addWidget(history_label)
        
        self.history_list = QListWidget()
        self.history_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #ddd;
                border-radius: 5px;
                background-color: #fafafa;
                font-size: 12px;
            }
        """)
        history_layout.addWidget(self.history_list)
        history_frame.setLayout(history_layout)
        main_layout.addWidget(history_frame, 1) 
        
        self.setLayout(main_layout)

    def on_number_clicked(self, button):
        """Handle number button clicks with toggle (deselect) support"""
        number = int(button.text())
        
        if self.selected_number1 is None:
            self.selected_number1 = number
            self.highlight_button(number, True)
            self.feedback_label.setText(f"Selected {number}. Now click an operation.")
        elif self.selected_operation is None:
            if self.selected_number1 == number:
                self.highlight_button(number, False)
                self.selected_number1 = None
                self.feedback_label.setText("Click a number, then an operation, then another number")
            else:
                self.feedback_label.setText("Please click an operation first!")
        else:
            if self.selected_number2 == number:
                self.highlight_button(number, False)
                self.selected_number2 = None
                self.feedback_label.setText(f"Selected {self.selected_number1}. Now click an operation.")
            else:
                self.selected_number2 = number
                self.highlight_button(number, True)
                self.make_move()

    def on_operation_clicked(self, operation):
        """Handle operation button clicks with toggle (deselect) support"""
        if self.selected_number1 is None:
            self.feedback_label.setText("Please click a number first!")
            return
        
        if self.selected_operation == operation:
            self.highlight_operation(operation, False)
            self.selected_operation = None
            self.feedback_label.setText(f"Selected {self.selected_number1}. Now click an operation.")
            return
        
        if self.selected_operation is not None:
            self.highlight_operation(self.selected_operation, False)
        
        self.selected_operation = operation
        self.highlight_operation(operation, True)
        self.feedback_label.setText(f"Selected {operation}. Now click another number.")

    def highlight_button(self, number, highlight):
        """Highlight or unhighlight a number button"""
        for button in self.number_buttons:
            if button.text() == str(number):
                if highlight:
                    button.setStyleSheet(f"""
                        QPushButton {{
                            border: 3px solid #FFD700;
                            border-radius: {button.size//2}px;
                            background-color: {button.color.name()};
                            color: {button.text_color.name()};
                            font-weight: bold;
                            font-size: {button.size//3}px;
                        }}
                    """)
                else:
                    button.setStyleSheet(f"""
                        QPushButton {{
                            border: none;
                            border-radius: {button.size//2}px;
                            background-color: {button.color.name()};
                            color: {button.text_color.name()};
                            font-weight: bold;
                            font-size: {button.size//3}px;
                        }}
                        QPushButton:hover {{
                            background-color: {button.color.lighter(120).name()};
                        }}
                    """)
                break

    def highlight_operation(self, operation, highlight):
        """Highlight or unhighlight an operation button"""
        for button in self.operation_buttons:
            if button.text() == operation:
                if highlight:
                    button.setStyleSheet(f"""
                        QPushButton {{
                            border: 3px solid #FFD700;
                            border-radius: {button.size//2}px;
                            background-color: {button.color.name()};
                            color: {button.text_color.name()};
                            font-weight: bold;
                            font-size: {button.size//3}px;
                        }}
                    """)
                else:
                    button.setStyleSheet(f"""
                        QPushButton {{
                            border: none;
                            border-radius: {button.size//2}px;
                            background-color: {button.color.name()};
                            color: {button.text_color.name()};
                            font-weight: bold;
                            font-size: {button.size//3}px;
                        }}
                        QPushButton:hover {{
                            background-color: {button.color.lighter(120).name()};
                        }}
                    """)
                break

    def clear_selections(self):
        """Clear all current selections and highlights"""
        if self.selected_number1:
            self.highlight_button(self.selected_number1, False)
        if self.selected_number2:
            self.highlight_button(self.selected_number2, False)
        if self.selected_operation:
            self.highlight_operation(self.selected_operation, False)
        
        self.selected_number1 = None
        self.selected_number2 = None
        self.selected_operation = None

    def make_move(self):
        try:
            op_map = {'×': '*', '÷': '/'}
            operation = op_map.get(self.selected_operation, self.selected_operation)
            
            self.history_stack.append(copy.deepcopy(self.state))
            
            move = {'num1': self.selected_number1, 'num2': self.selected_number2, 'operation': operation}
            result, new_state = applyMove(self.state, move)
            self.state = new_state
            
            self.clear_selections()
            
            self.update_ui()
            self.feedback_label.setText(result['message'] or "Move applied!")
            
            if self.state['completed']:
                self.feedback_label.setText("🎉 Congratulations! You finished the puzzle! 🎉")
                
        except Exception as e:
            self.feedback_label.setText(f"Error: {str(e)}")
            self.clear_selections()

    def undo_move(self):
        if self.history_stack:
            self.state = self.history_stack.pop()
            self.clear_selections()
            self.update_ui()
            self.feedback_label.setText("Move undone!")

    def update_ui(self):
        current_numbers = self.state['numbers']
        
        for i, button in enumerate(self.number_buttons):
            if i < len(current_numbers):
                button.setText(str(current_numbers[i]))
                button.setEnabled(True)
                button.setVisible(True)
            else:
                button.setEnabled(False)
                button.setVisible(False)

        self.history_list.clear()
        for step in self.state['steps']:
            self.history_list.addItem(step)
        
        
        self.undo_btn.setEnabled(len(self.history_stack) > 0)

    def difficulty_button_style(self, selected=False):
        if selected:
            return ("""
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    padding: 8px 18px;
                    font-weight: bold;
                    font-size: 16px;
                }
            """)
        else:
            return ("""
                QPushButton {
                    background-color: #e0e0e0;
                    color: #333;
                    border: none;
                    border-radius: 5px;
                    padding: 8px 18px;
                    font-weight: bold;
                    font-size: 16px;
                }
                QPushButton:hover {
                    background-color: #bdbdbd;
                }
            """)

    def set_difficulty(self, level):
        self.difficulty = level
        for lvl, btn in self.difficulty_buttons.items():
            btn.setStyleSheet(self.difficulty_button_style(selected=(lvl==level)))
            btn.setChecked(lvl==level)
        self.new_game()

    def new_game(self):
        self.state = createGame(difficulty=self.difficulty)
        self.history_stack.clear()
        self.target_label.setText(f"Target: {self.state['target']}")
        self.clear_selections()
        self.update_ui()
        self.feedback_label.setText("Click a number, then an operation, then another number")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NumbersGameWindow()
    window.show()
    sys.exit(app.exec_())