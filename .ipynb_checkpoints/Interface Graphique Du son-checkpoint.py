import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel
from pydub import AudioSegment
from pydub.playback import play
from pydub import AudioSegment
from pydub.playback import play
import warnings
warnings.filterwarnings('ignore')
audio = None
file_path = ""

def load_file():
    global audio, file_path
    # Open file dialog to select an audio file
    file_path, _ = QFileDialog.getOpenFileName(None, "Ouvrir le fichier audio", "", "Audio Files (*.wav *.mp3 *.flac *.ogg)")

    if file_path:
        # Load the audio file using Pydub
        audio = AudioSegment.from_file(file_path)
        file_label.setText(f"Loaded: {file_path}")

def play_audio():
    if audio:
        play(audio)
    else:
        file_label.setText("Aucun fichier audio n'a été chargé")

def export_file():
    if audio:
        save_path, _ = QFileDialog.getSaveFileName(None, "Exporter le fichier sous plusieurs formats", "", "Audio Files (*.mp3 *.wav *.flac,*.wma,*.ogg,*.aac)")

        if save_path:
            audio.export(save_path, format=save_path.split('.')[-1])
            file_label.setText(f"Exported to: {save_path}")
    else:
        file_label.setText("Aucun  fichier n'est chargé pour l'exporter")

app = QApplication(sys.argv)
if not QApplication.instance():
    app = QApplication(sys.argv)
else:
    app = QApplication.instance()

window = QWidget()
window.setWindowTitle("Project TNIM exercice 3")
window.setGeometry(100, 100, 1000, 500)
window.setStyleSheet("""
    QWidget {
        background-color: #2E2E2E;  
        color: #FFFFFF;             
        font-family: Arial, sans-serif;
        font-size: 14px;
        text-align:center;
    }
    QLabel {
        font-size: 16px;
        margin-bottom: 10px;
        text-align: center;  

    }
    QPushButton {
        background-color:transparent ;
        color: #8EBCFF;
        border-radius: 18px;
        padding: 20px;
        font-size: 14px;
        width:60%;
        margin-top:30px;
    }
    QPushButton:hover {
        background-color: #8EBCFF;
        color:white;
        
    }
""")

layout = QVBoxLayout()

file_label = QLabel("Aucun fichier n'est sélectionner")
layout.addWidget(file_label)

load_button = QPushButton("Sélectionner le fichier audio")
load_button.clicked.connect(load_file)
layout.addWidget(load_button)

play_button = QPushButton("écouter le fichier sélectionné")
play_button.clicked.connect(play_audio)
layout.addWidget(play_button)

export_button = QPushButton("Exporter le fichier audio")
export_button.clicked.connect(export_file)
layout.addWidget(export_button)

window.setLayout(layout)

window.show()

sys.exit(app.exec())
