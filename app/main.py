python"""
Android File Explorer - Versión Simple
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.utils import platform

# Import Android-specific modules if on Android
if platform == 'android':
    from android.permissions import request_permissions, Permission
    from android.storage import primary_external_storage_path
    request_permissions([
        Permission.READ_EXTERNAL_STORAGE,
        Permission.WRITE_EXTERNAL_STORAGE,
        Permission.INTERNET
    ])

class FileExplorerWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        
        # Simple test UI
        header = Label(
            text='File Explorer Test', 
            size_hint_y=None, 
            height=50
        )
        self.add_widget(header)
        
        status = Label(
            text='App funcionando correctamente!', 
            size_hint_y=None, 
            height=50
        )
        self.add_widget(status)
        
        btn = Button(
            text='Test Button', 
            size_hint_y=None, 
            height=50
        )
        btn.bind(on_press=lambda x: status.__setattr__('text', 'Botón presionado!'))
        self.add_widget(btn)

class FileExplorerApp(App):
    def build(self):
        return FileExplorerWidget()

if __name__ == '__main__':
    FileExplorerApp().run()
