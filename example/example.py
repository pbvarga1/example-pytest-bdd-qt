from itertools import cycle
import sys

# from qtpy import QtWidgets, QtCore
from PyQt5 import QtWidgets, QtCore


class ExampleWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._central_widget = QtWidgets.QWidget()
        self._words = cycle([
            'foo',
            'bar',
            'baz'
        ])
        layout = QtWidgets.QHBoxLayout()
        self.btn = QtWidgets.QPushButton('Press Me')
        self.line_edit = QtWidgets.QLineEdit()
        layout.addWidget(self.btn)
        layout.addWidget(self.line_edit)
        self.btn.clicked.connect(self.clicked)
        self._central_widget.setLayout(layout)
        self.setCentralWidget(self._central_widget)
    
    def clicked(self):
        self.line_edit.setText(next(self._words))


if __name__ == "__main__":    
    app = QtWidgets.QApplication(sys.argv)
    ex = ExampleWindow()
    ex.show()
    sys.exit(app.exec_())
