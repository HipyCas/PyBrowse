import os
from PyQt5.QtCore import QUrl, QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QAction, QLabel, QLineEdit, QFileDialog, QDialog, \
    QDialogButtonBox, QVBoxLayout
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWebEngineWidgets import QWebEngineView

from sys import argv


class AboutDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)
        
        QBtn = QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        
        layout = QVBoxLayout()
        
        title = QLabel("PyBrowse")
        font = title.font()
        font.setPointSize(20)
        title.setFont(font)
        
        layout.addWidget(title)
        
        logo = QLabel()
        logo.setPixmap(QPixmap(os.path.join('images', 'ma-icon-128.png')))
        layout.addWidget(logo)

        layout.addWidget(QLabel("Version 2020.1.0p67"))
        layout.addWidget(QLabel("Copyright 2020 HipyCas"))

        for i in range(0, layout.count()):
            layout.itemAt(i).setAlignment(Qt.AlignHCenter)
        
        layout.addWidget(self.buttonBox)
        
        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))

        ### Navigation Toolbar
        navtb = QToolBar("Navigation")
        navtb.setIconSize(QSize(16, 16))
        self.addToolBar(navtb)

        # Back Action
        back_btn = QAction(QIcon('ui/black/filled/chevron_left-48dp.svg'), "Back", self)
        back_btn.setStatusTip("Back to previous page")
        back_btn.triggered.connect(self.browser.back)
        navtb.addAction(back_btn)

        # Forward Action
        next_btn = QAction(QIcon('ui/black/filled/chevron_right-48dp.svg'), "Forward", self)
        next_btn.setStatusTip("Forward to next page")
        next_btn.triggered.connect(self.browser.forward)
        navtb.addAction(next_btn)

        # Reload Action
        reload_btn = QAction(QIcon('ui/black/filled/refresh-48dp.svg'), "Reload", self)
        reload_btn.setStatusTip("Reload page")
        reload_btn.triggered.connect(self.browser.reload)
        navtb.addAction(reload_btn)

        # Home Action
        home_btn = QAction(QIcon('ui/black/filled/home-18dp.svg'), "Home", self)
        home_btn.setStatusTip("Go home")
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        # HTTPS Icon
        self.httpsicon = QAction(QIcon('ui/black/filled/no_encryption-48dp.svg'), '', self)
        self.httpsicon.setStatusTip("Page is not SSL protected")
        self.httpsicon.setEnabled(False)
        #self.httpsicon.setPixmap(QPixmap('ui/black/filled/no_encryption-18dp.svg'))
        navtb.addAction(self.httpsicon)

        # URL Bar
        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.urlbar)

        # Load stop Action
        stop_btn = QAction(QIcon('ui/black/filled/close-48dp.svg'), "Stop", self)
        stop_btn.setStatusTip("Stop loading current page")
        stop_btn.triggered.connect(self.browser.stop)
        navtb.addAction(stop_btn)

        # Updates
        self.browser.urlChanged.connect(self.update_urlbar)
        self.browser.loadFinished.connect(self.update_title)

        ### File Menu
        file_menu = self.menuBar().addMenu("&File")

        # Open Action
        open_file_action = QAction(QIcon(os.path.join('images', 'disk--arrow.png')), "Open file...", self)
        open_file_action.setStatusTip('Open from file')
        open_file_action.triggered.connect(self.open_file)
        file_menu.addAction(open_file_action)

        # Save Action
        save_file_action = QAction(QIcon(os.path.join('images', 'disk--pencil.png')), "Save file...", self)
        save_file_action.setText('Save to file')
        save_file_action.triggered.connect(self.save_file)
        file_menu.addAction(save_file_action)

        ### Help Menu
        help_menu = self.menuBar().addMenu("&Help")

        # About dialog Action
        about_action = QAction(QIcon(os.path.join('images', 'question.png')), "About PyBrowse", self)
        about_action.setStatusTip("Find out more about PyBrowse")  # Hungry!
        about_action.triggered.connect(self.about)
        help_menu.addAction(about_action)

        # Visit official site Action
        navigate_mozarella_action = QAction(QIcon(os.path.join('images', 'lifebuoy.png')),
                                            "PyBrowse Homepage", self)
        navigate_mozarella_action.setStatusTip("Go to PyBrowse Homepage")
        navigate_mozarella_action.triggered.connect(self.navigate_page)
        help_menu.addAction(navigate_mozarella_action)

        self.setCentralWidget(self.browser)

        self.show()

    def navigate_home(self):
        self.browser.setUrl(QUrl("https://www.google.com"))

    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
            q.setScheme("http")
        self.browser.setUrl(q)

    def update_urlbar(self, q):
        if q.scheme() == 'https':
            # Secure padlock icon
            self.httpsicon.setIcon(QIcon('ui/black/filled/https-48dp.svg'))
            self.httpsicon.setStatusTip('Page has SSL encryption')
            self.httpsicon.setIconText('SSL')
            self.httpsicon.setObjectName('SSL')
            self.httpsicon.setWhatsThis('SSL')
        else:
            # Insecure padlock icon
            self.httpsicon.setIcon(QIcon('ui/black/filled/no_encryption-48dp.svg'))
            self.httpsicon.setStatusTip('Page is not SSL protected')
            self.httpsicon.setIconText('No SSL')
            self.httpsicon.setObjectName('No SSL')
            self.httpsicon.setWhatsThis('No SSL')

        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

    def update_title(self):
        title = self.browser.page().title()
        self.setWindowTitle("%s - PyBrowse" % title)

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open file", "",
                                                  "Hypertext Markup Language (*.htm *html);;"
                                                  "All files (*.*)")
        if filename:
            with open(filename, 'r') as f:
                html = f.read()
            
            self.browser.setHtml(html)
            self.urlbar.setText(filename)

    def save_file(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Page As", "",
                                              "Hypertext Markup Language (*.htm *html);;"
                                              "All files (*.*)")
        if filename:
            html = self.browser.page().toHtml()
            with open(filename, 'w') as f:
                f.write(html)

    def navigate_page(self):
        self.browser.setUrl(QUrl("hipycas.github.io/PyBrowse"))

    def about(self):
        dlg = AboutDialog()
        dlg.exec_()


app = QApplication(argv)
app.setApplicationName("PyBrowse")
app.setOrganizationName("HipyCas Development")
app.setOrganizationDomain("hipycas.github.io")

win = MainWindow()

app.exec_()
