"""
Professional Profile Photo Crop Dialog
"""

import os
import uuid
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
    QGraphicsView, QGraphicsScene, QGraphicsPixmapItem,
    QLabel, QFrame, QWidget
)
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPixmap, QPainter, QPainterPath, QColor, QFont, QPen

class CropOverlay(QWidget):
    """Semi-transparent overlay with a clear circular hole, placed on top of the view."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.circle_radius = 150 # 300px diameter

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Dim background
        path = QPainterPath()
        path.addRect(self.rect())
        
        # The hole
        center = self.rect().center()
        path.addEllipse(center, self.circle_radius, self.circle_radius)
        
        painter.setBrush(QColor(0, 0, 0, 180))
        painter.setPen(Qt.NoPen)
        painter.drawPath(path)
        
        # Border for the hole
        painter.setPen(QPen(QColor(255, 255, 255, 150), 2))
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(center, self.circle_radius, self.circle_radius)

class CropDialog(QDialog):
    def __init__(self, image_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Crop Profile Photo")
        self.setFixedSize(500, 650)
        self.setStyleSheet("background-color: #111827;")
        
        self.image_path = image_path
        self.final_path = None
        
        self.setup_ui()
        self.load_image()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 20)
        layout.setSpacing(0)

        # Header
        header = QLabel("Adjust Profile Photo")
        header.setFont(QFont("SF Pro Display", 18, QFont.Bold))
        header.setStyleSheet("color: white; padding: 20px; background: #1F2937;")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)

        # Viewport container
        self.view_container = QWidget()
        self.view_container.setFixedHeight(450)
        v_lay = QVBoxLayout(self.view_container)
        v_lay.setContentsMargins(0, 0, 0, 0)

        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        self.view.setDragMode(QGraphicsView.ScrollHandDrag)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setStyleSheet("background: #000000; border: none;")
        self.view.setFrameShape(QFrame.NoFrame)
        v_lay.addWidget(self.view)
        
        # Add overlay
        self.overlay = CropOverlay(self.view_container)
        self.overlay.setGeometry(0, 0, 500, 450)
        
        layout.addWidget(self.view_container)

        # Instructions
        hint = QLabel("Drag to move • Scroll to zoom")
        hint.setFont(QFont("Inter", 10))
        hint.setStyleSheet("color: #9CA3AF; margin-top: 10px;")
        hint.setAlignment(Qt.AlignCenter)
        layout.addWidget(hint)

        # Footer Actions
        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(40, 20, 40, 10)
        btn_layout.setSpacing(20)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFixedHeight(44)
        cancel_btn.setCursor(Qt.PointingHandCursor)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #374151;
                color: #F9FAFB;
                border-radius: 22px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #4B5563; }
        """)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn, stretch=1)

        save_btn = QPushButton("Apply Photo")
        save_btn.setFixedHeight(44)
        save_btn.setCursor(Qt.PointingHandCursor)
        save_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 #7C3AED, stop:1 #6D28D9);
                color: white;
                border-radius: 22px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 #8B5CF6, stop:1 #7C3AED);
            }
        """)
        save_btn.clicked.connect(self.on_save)
        btn_layout.addWidget(save_btn, stretch=1)

        layout.addLayout(btn_layout)

    def load_image(self):
        pixmap = QPixmap(self.image_path)
        if pixmap.isNull():
            self.reject()
            return

        self.pixmap_item = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(self.pixmap_item)
        
        # Initial scale: circle diameter is 300px. Make image fill it.
        circle_d = 300
        min_dim = min(pixmap.width(), pixmap.height())
        scale = (circle_d + 50) / min_dim
        self.pixmap_item.setScale(scale)
        
        # Center image in scene
        self.pixmap_item.setPos(-pixmap.width()*scale/2, -pixmap.height()*scale/2)
        self.view.centerOn(0, 0)

    def wheelEvent(self, event):
        zoom_in_factor = 1.15
        zoom_out_factor = 1 / zoom_in_factor
        
        if event.angleDelta().y() > 0:
            self.view.scale(zoom_in_factor, zoom_in_factor)
        else:
            self.view.scale(zoom_out_factor, zoom_out_factor)

    def on_save(self):
        # We need the portion of the scene directly under the 300px circle in the center of the viewport
        viewport_center = self.view.viewport().rect().center()
        
        # Radius in viewport pixels
        r = self.overlay.circle_radius # 150
        
        # Create result at high res
        target_size = 512
        result = QPixmap(target_size, target_size)
        result.fill(Qt.transparent)
        
        painter = QPainter(result)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        
        # The region of the scene we want is what's visible in the viewport's circle
        # Map viewport rect to scene
        vp_circle_rect = QRectF(viewport_center.x() - r, viewport_center.y() - r, r*2, r*2)
        scene_rect = self.view.mapToScene(vp_circle_rect.toRect()).boundingRect()
        
        self.scene.render(painter, QRectF(0, 0, target_size, target_size), scene_rect)
        painter.end()
        
        # Save to data directory
        save_dir = os.path.join(os.getcwd(), "data", "profiles")
        os.makedirs(save_dir, exist_ok=True)
        
        file_name = f"avatar_{uuid.uuid4().hex[:8]}.png"
        path = os.path.join(save_dir, file_name)
        result.save(path, "PNG")
        
        self.final_path = path
        self.accept()
