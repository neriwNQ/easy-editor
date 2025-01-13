import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QListWidget, QFileDialog
from PyQt5.QtGui import QPixmap
from PIL import Image
from PIL import ImageFilter
from PyQt5 import QtGui, QtCore


app = QApplication([])

main_win = QWidget()
main_win.setWindowTitle('Easy Editor')
main_win.resize(1200, 800)
main_win.setMaximumSize(QtCore.QSize(1200, 800))
main_win.setMinimumSize(QtCore.QSize(1200, 800))
main_win.setStyleSheet("background-color: rgb(100, 133, 202);")

app.setWindowIcon(QtGui.QIcon("angry_cat.jpg"))
main_win.setWindowIcon(QtGui.QIcon("angry_cat.jpg"))

picture_list = QListWidget()
folder = QPushButton('Папка')
right_btn = QPushButton('Лево')
left_btn = QPushButton('Право')
mirror_btn = QPushButton('Зеркало')
sharpness_btn = QPushButton('Резкость')
b_w_btn = QPushButton('Ч/Б')
blur_btn = QPushButton('Блюр')
rotate_btn = QPushButton('Перевернуть')
edge_enchance = QPushButton('Ч/Б с выделением краев')
picture = QLabel('Картинка')

v_line = QVBoxLayout()
v_line.addWidget(folder)
v_line.addWidget(picture_list)

v_line2 = QVBoxLayout()
v_line2.addWidget(picture)

h_line = QHBoxLayout()
h_line.addWidget(right_btn)
h_line.addWidget(left_btn)
h_line.addWidget(mirror_btn)
h_line.addWidget(sharpness_btn)
h_line.addWidget(b_w_btn)
h_line.addWidget(blur_btn)
h_line.addWidget(rotate_btn)
h_line.addWidget(edge_enchance)

v_line2.addLayout(h_line)

h_line_main = QHBoxLayout()
h_line_main.addLayout(v_line, 35)
h_line_main.addLayout(v_line2, 65)

main_win.setLayout(h_line_main)

workdir = ''

def open_folder():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def filter(workdir, extensions):
    result = []
    for filename in workdir:
        for extension in extensions:
            if filename.endswith(extension):
                result.append(filename)
    return result

def showFilenamesList():
    extensions = ['.png', '.jpeg', '.gif', '.raw', '.tiff', '.bmp', '.psd', '.webp', '.jpg']
    open_folder()
    filtered_files = filter(os.listdir(workdir), extensions)
    picture_list.clear()
    for filename in filtered_files:
        picture_list.addItem(filename)

folder.clicked.connect(showFilenamesList)

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.file_name = None
        self.dir = None
        self.save_dir = 'pictures/'
    
    def load_image(self, file_name, dir):
        self.file_name = file_name
        self.dir = dir
        file_path = os.path.join(self.dir, self.file_name)
        self.image = Image.open(file_path)
    
    def showImage(self, path):
        picture.hide()
        pixmapimage = QPixmap(path)
        w, h = picture.width(), picture.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        picture.setPixmap(pixmapimage)
        picture.show()
    
    def do_bw(self):
        self.image = self.image.convert('L')
        self.saveImage()
        path = os.path.join(self.dir, self.save_dir, self.file_name)
        self.showImage(path)

    def sharpness(self):
        self.image = self.image.filter(ImageFilter.SHARPEN)
        self.saveImage()
        path = os.path.join(self.dir, self.save_dir, self.file_name)
        self.showImage(path)

    def pic_blured(self):
        self.image = self.image.filter(ImageFilter.BLUR)
        self.saveImage()
        path = os.path.join(self.dir, self.save_dir, self.file_name)
        self.showImage(path)

    def pic_filp_to_bottom(self):
        self.image = self.image.transpose(Image.ROTATE_180)
        self.saveImage()
        path = os.path.join(self.dir, self.save_dir, self.file_name)
        self.showImage(path)

    def pic_mirror(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        path = os.path.join(self.dir, self.save_dir, self.file_name)
        self.showImage(path)

    def pic_90L(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        path = os.path.join(self.dir, self.save_dir, self.file_name)
        self.showImage(path)

    def pic_90R(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        path = os.path.join(self.dir, self.save_dir, self.file_name)
        self.showImage(path)

    def pic_edge_enchance(self):
        self.image = self.image.filter(ImageFilter.EDGE_ENHANCE)
        self.saveImage()
        path = os.path.join(self.dir, self.save_dir, self.file_name)
        self.showImage(path)

    def saveImage(self):
        path = os.path.join(workdir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.file_name)
        self.image.save(image_path)


workimage = ImageProcessor()

def showChosenImage():
    if picture_list.currentRow() >= 0:
        filename = picture_list.currentItem().text()
        workimage.load_image(filename, workdir)
        image_path = os.path.join(workimage.dir, workimage.file_name)
        workimage.showImage(image_path)

picture_list.currentRowChanged.connect(showChosenImage)

b_w_btn.clicked.connect(workimage.do_bw)
sharpness_btn.clicked.connect(workimage.sharpness)
blur_btn.clicked.connect(workimage.pic_blured)
rotate_btn.clicked.connect(workimage.pic_filp_to_bottom)
mirror_btn.clicked.connect(workimage.pic_mirror)
right_btn.clicked.connect(workimage.pic_90R)
left_btn.clicked.connect(workimage.pic_90L)
edge_enchance.clicked.connect(workimage.pic_edge_enchance)




























main_win.show()
app.exec_()
