"""
Android File Explorer with Remote Access
Main Application File using Kivy Framework
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.utils import platform
import os
import threading
import json
from datetime import datetime
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import socket

# Import Android-specific modules if on Android
if platform == 'android':
    from android.permissions import request_permissions, Permission
    from android.storage import primary_external_storage_path
    request_permissions([
        Permission.READ_EXTERNAL_STORAGE,
        Permission.WRITE_EXTERNAL_STORAGE,
        Permission.INTERNET
    ])


class FileExplorerServer:
    """Flask server for remote file access"""
    
    def __init__(self, file_explorer):
        self.file_explorer = file_explorer
        self.app = Flask(__name__)
        CORS(self.app)
        self.setup_routes()
        self.server_thread = None
        self.port = 8080
        
    def setup_routes(self):
        """Setup Flask routes for file operations"""
        
        @self.app.route('/api/status', methods=['GET'])
        def get_status():
            return jsonify({
                'status': 'online',
                'device': 'Android File Explorer',
                'current_path': self.file_explorer.current_path
            })
        
        @self.app.route('/api/list', methods=['GET'])
        def list_directory():
            path = request.args.get('path', self.file_explorer.current_path)
            try:
                items = self.file_explorer.get_directory_contents(path)
                return jsonify({
                    'success': True,
                    'path': path,
                    'items': items
                })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 400
        
        @self.app.route('/api/file/info', methods=['GET'])
        def get_file_info():
            path = request.args.get('path')
            if not path:
                return jsonify({'success': False, 'error': 'Path required'}), 400
            
            try:
                info = self.file_explorer.get_file_info(path)
                return jsonify({
                    'success': True,
                    'info': info
                })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 400
        
        @self.app.route('/api/file/download', methods=['GET'])
        def download_file():
            path = request.args.get('path')
            if not path or not os.path.isfile(path):
                return jsonify({'success': False, 'error': 'Invalid file path'}), 400
            
            try:
                return send_file(path, as_attachment=True)
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 400
        
        @self.app.route('/api/file/read', methods=['GET'])
        def read_file():
            path = request.args.get('path')
            if not path or not os.path.isfile(path):
                return jsonify({'success': False, 'error': 'Invalid file path'}), 400
            
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                return jsonify({
                    'success': True,
                    'content': content
                })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 400
        
        @self.app.route('/api/file/create', methods=['POST'])
        def create_file():
            data = request.json
            path = data.get('path')
            content = data.get('content', '')
            
            try:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return jsonify({
                    'success': True,
                    'message': 'File created successfully'
                })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 400
        
        @self.app.route('/api/directory/create', methods=['POST'])
        def create_directory():
            data = request.json
            path = data.get('path')
            
            try:
                os.makedirs(path, exist_ok=True)
                return jsonify({
                    'success': True,
                    'message': 'Directory created successfully'
                })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 400
        
        @self.app.route('/api/delete', methods=['DELETE'])
        def delete_item():
            path = request.args.get('path')
            
            try:
                if os.path.isfile(path):
                    os.remove(path)
                elif os.path.isdir(path):
                    import shutil
                    shutil.rmtree(path)
                return jsonify({
                    'success': True,
                    'message': 'Item deleted successfully'
                })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 400
    
    def get_local_ip(self):
        """Get the local IP address of the device"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"
    
    def start_server(self):
        """Start the Flask server in a separate thread"""
        if self.server_thread and self.server_thread.is_alive():
            return
        
        self.server_thread = threading.Thread(
            target=lambda: self.app.run(
                host='0.0.0.0',
                port=self.port,
                debug=False,
                use_reloader=False
            ),
            daemon=True
        )
        self.server_thread.start()
    
    def stop_server(self):
        """Stop the Flask server"""
        # Note: Flask doesn't have a built-in stop method
        # The server will stop when the app closes
        pass


class FileExplorerWidget(BoxLayout):
    """Main file explorer widget"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        
        # Initialize path
        if platform == 'android':
            self.current_path = primary_external_storage_path()
        else:
            self.current_path = os.path.expanduser('~')
        
        # Initialize server
        self.server = FileExplorerServer(self)
        
        # Build UI
        self.build_ui()
        
        # Start server
        self.start_server()
    
    def build_ui(self):
        """Build the user interface"""
        
        # Header with server info
        header = BoxLayout(size_hint_y=None, height=120, orientation='vertical', padding=10)
        
        self.server_status = Label(
            text='Server: Starting...',
            size_hint_y=None,
            height=30,
            color=(0.2, 0.8, 0.2, 1)
        )
        header.add_widget(self.server_status)
        
        self.server_url = Label(
            text='URL: Initializing...',
            size_hint_y=None,
            height=30,
            color=(0.3, 0.6, 1, 1)
        )
        header.add_widget(self.server_url)
        
        # Current path display
        self.path_label = Label(
            text=f'Path: {self.current_path}',
            size_hint_y=None,
            height=30,
            color=(1, 1, 1, 1)
        )
        header.add_widget(self.path_label)
        
        # Navigation buttons
        nav_layout = BoxLayout(size_hint_y=None, height=30, spacing=5)
        
        back_btn = Button(text='← Back', size_hint_x=0.3)
        back_btn.bind(on_press=self.go_back)
        nav_layout.add_widget(back_btn)
        
        refresh_btn = Button(text='⟳ Refresh', size_hint_x=0.3)
        refresh_btn.bind(on_press=lambda x: self.refresh_view())
        nav_layout.add_widget(refresh_btn)
        
        home_btn = Button(text='⌂ Home', size_hint_x=0.4)
        home_btn.bind(on_press=self.go_home)
        nav_layout.add_widget(home_btn)
        
        header.add_widget(nav_layout)
        
        self.add_widget(header)
        
        # File list scroll view
        scroll = ScrollView()
        self.file_grid = GridLayout(cols=1, spacing=5, size_hint_y=None, padding=10)
        self.file_grid.bind(minimum_height=self.file_grid.setter('height'))
        scroll.add_widget(self.file_grid)
        self.add_widget(scroll)
        
        # Initial load
        self.refresh_view()
    
    def start_server(self):
        """Start the remote access server"""
        self.server.start_server()
        Clock.schedule_once(self.update_server_info, 2)
    
    def update_server_info(self, dt):
        """Update server status display"""
        ip = self.server.get_local_ip()
        port = self.server.port
        self.server_status.text = f'Server: ✓ Online'
        self.server_url.text = f'Access at: http://{ip}:{port}'
    
    def get_directory_contents(self, path):
        """Get contents of a directory"""
        items = []
        try:
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                try:
                    stat = os.stat(item_path)
                    items.append({
                        'name': item,
                        'path': item_path,
                        'is_dir': os.path.isdir(item_path),
                        'size': stat.st_size if not os.path.isdir(item_path) else 0,
                        'modified': datetime.fromtimestamp(stat.st_mtime).isoformat()
                    })
                except:
                    pass
        except PermissionError:
            pass
        
        # Sort: directories first, then files
        items.sort(key=lambda x: (not x['is_dir'], x['name'].lower()))
        return items
    
    def get_file_info(self, path):
        """Get detailed information about a file"""
        stat = os.stat(path)
        return {
            'name': os.path.basename(path),
            'path': path,
            'is_dir': os.path.isdir(path),
            'size': stat.st_size,
            'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
            'created': datetime.fromtimestamp(stat.st_ctime).isoformat()
        }
    
    def refresh_view(self):
        """Refresh the file list view"""
        self.file_grid.clear_widgets()
        self.path_label.text = f'Path: {self.current_path}'
        
        items = self.get_directory_contents(self.current_path)
        
        if not items:
            no_files = Label(
                text='No files or permission denied',
                size_hint_y=None,
                height=40
            )
            self.file_grid.add_widget(no_files)
            return
        
        for item in items:
            btn = Button(
                text=f"{'📁' if item['is_dir'] else '📄'} {item['name']}",
                size_hint_y=None,
                height=50,
                halign='left',
                text_size=(None, None)
            )
            btn.bind(on_press=lambda x, p=item['path'], d=item['is_dir']: 
                     self.on_item_click(p, d))
            self.file_grid.add_widget(btn)
    
    def on_item_click(self, path, is_dir):
        """Handle item click"""
        if is_dir:
            self.current_path = path
            self.refresh_view()
        else:
            self.show_file_info(path)
    
    def show_file_info(self, path):
        """Show file information popup"""
        info = self.get_file_info(path)
        
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        content.add_widget(Label(text=f"Name: {info['name']}"))
        content.add_widget(Label(text=f"Size: {self.format_size(info['size'])}"))
        content.add_widget(Label(text=f"Modified: {info['modified'][:19]}"))
        
        close_btn = Button(text='Close', size_hint_y=None, height=50)
        content.add_widget(close_btn)
        
        popup = Popup(
            title='File Information',
            content=content,
            size_hint=(0.9, 0.5)
        )
        close_btn.bind(on_press=popup.dismiss)
        popup.open()
    
    def format_size(self, size):
        """Format file size in human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} TB"
    
    def go_back(self, instance):
        """Navigate to parent directory"""
        parent = os.path.dirname(self.current_path)
        if parent and parent != self.current_path:
            self.current_path = parent
            self.refresh_view()
    
    def go_home(self, instance):
        """Navigate to home directory"""
        if platform == 'android':
            self.current_path = primary_external_storage_path()
        else:
            self.current_path = os.path.expanduser('~')
        self.refresh_view()


class FileExplorerApp(App):
    """Main application class"""
    
    def build(self):
        return FileExplorerWidget()


if __name__ == '__main__':
    FileExplorerApp().run()
