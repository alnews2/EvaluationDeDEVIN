"""Feuille de style Qt de l'application."""

STYLE_SHEET = """
QWidget#central_widget {
    background-color: #1e222a;
}

QLabel#display {
    background-color: #12151b;
    border: 1px solid #2c323d;
    border-radius: 8px;
    color: #f2f5fa;
    padding: 12px 16px;
}

QLabel#display[state="error"] {
    color: #ff6b6b;
}

QPushButton {
    background-color: #2c323d;
    border: none;
    border-radius: 8px;
    color: #f2f5fa;
    font-size: 18px;
}

QPushButton:hover {
    background-color: #39414f;
}

QPushButton:pressed {
    background-color: #4a5464;
}

QPushButton[role="operator"] {
    background-color: #3b4453;
    font-weight: 600;
}

QPushButton[role="command"] {
    background-color: #343b47;
    color: #c8d0dc;
}

QPushButton[role="equals"] {
    background-color: #2f6fed;
    font-weight: 700;
}

QPushButton[role="equals"]:hover {
    background-color: #3d7cf5;
}
"""
