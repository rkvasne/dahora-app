"""
Sistema de notificações do Dahora App
"""
import threading
import time
import logging
from typing import Optional

# Imports opcionais
try:
    from winotify import Notification
    TOAST_AVAILABLE = True
except ImportError:
    TOAST_AVAILABLE = False

try:
    import tkinter as tk
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False


class NotificationManager:
    """Gerenciador de notificações"""
    
    def __init__(self, global_icon=None):
        """
        Inicializa o gerenciador de notificações
        
        Args:
            global_icon: Referência ao ícone da bandeja (opcional)
        """
        self.global_icon = global_icon
    
    def set_icon(self, icon) -> None:
        """Define o ícone da bandeja"""
        self.global_icon = icon
    
    def show_toast(self, title: str, message: str, duration: int = 2) -> None:
        """
        Mostra notificação toast do Windows
        
        Args:
            title: Título da notificação
            message: Mensagem da notificação
            duration: Duração em segundos
        """
        def _show_notification():
            # Método 1: winotify (toast nativo)
            if TOAST_AVAILABLE:
                try:
                    mapped_duration = "short" if duration <= 5 else "long"
                    toast = Notification(
                        app_id="Dahora App",
                        title=title,
                        msg=message,
                        duration=mapped_duration
                    )
                    toast.show()
                    time.sleep(duration + 0.5)
                    return True
                except Exception:
                    pass
            
            # Método 2: notificação do pystray
            try:
                if self.global_icon:
                    self.global_icon.notify(message, title)
                    time.sleep(duration)
                    return True
            except Exception:
                pass
            
            # Último recurso: print no console
            print(f"\n{'='*50}")
            print(f"{title}")
            print(f"{message}")
            print(f"{'='*50}\n")
            return False
        
        # Executa em thread para não bloquear
        thread = threading.Thread(target=_show_notification, daemon=False)
        thread.start()
        time.sleep(0.05)
    
    def show_quick_notification(self, title: str, message: str, duration: float = 1.5) -> None:
        """
        Exibe uma notificação leve e moderna por ~1–2s usando Tkinter
        
        Args:
            title: Título da notificação
            message: Mensagem da notificação
            duration: Duração em segundos
        """
        if not TKINTER_AVAILABLE:
            return self.show_toast(title, message, int(duration))
        
        def _show_quick():
            try:
                root = tk.Tk()
                root.withdraw()
                
                top = tk.Toplevel(root)
                top.overrideredirect(True)
                try:
                    top.attributes('-topmost', True)
                except Exception:
                    pass
                
                # Dimensões e posição
                try:
                    root.update_idletasks()
                    sw = root.winfo_screenwidth()
                    sh = root.winfo_screenheight()
                except Exception:
                    sw, sh = 1366, 768
                
                width, height = 340, 110
                x = sw - width - 16
                y = sh - height - 48
                top.geometry(f"{width}x{height}+{x}+{y}")
                
                # Canvas com "card" arredondado
                canvas = tk.Canvas(top, width=width, height=height, bg='black', highlightthickness=0)
                canvas.pack(fill='both', expand=True)
                
                # Retângulo arredondado
                def round_rect(x1, y1, x2, y2, r=12, **kwargs):
                    points = [
                        x1+r, y1, x2-r, y1, x2, y1, x2, y1+r,
                        x2, y2-r, x2, y2, x2-r, y2, x1+r, y2,
                        x1, y2, x1, y2-r, x1, y1+r, x1, y1
                    ]
                    return canvas.create_polygon(points, smooth=True, **kwargs)
                
                round_rect(2, 2, width-2, height-2, r=14, fill='#2b2b2b', outline='#3c3c3c')
                
                # Fontes
                try:
                    title_font = ('Segoe UI Variable', 10, 'bold')
                    msg_font = ('Segoe UI Variable', 9)
                except Exception:
                    title_font = ('Segoe UI', 10, 'bold')
                    msg_font = ('Segoe UI', 9)
                
                # Labels
                frame = tk.Frame(top, bg='#2b2b2b')
                frame.place(x=0, y=0, width=width, height=height)
                lbl_title = tk.Label(frame, text=title, fg='#c5e1ff', bg='#2b2b2b', font=title_font)
                lbl_title.place(x=16, y=12)
                lbl_msg = tk.Label(frame, text=message, fg='#ffffff', bg='#2b2b2b', font=msg_font, justify='left')
                lbl_msg.place(x=16, y=36)
                
                # Fecha após duração
                top.after(int(max(1, duration) * 1000), root.destroy)
                root.mainloop()
            except Exception:
                # Fallback
                self.show_toast(title, message, int(duration))
        
        threading.Thread(target=_show_quick, daemon=True).start()
    
    def show_fatal_error(self, title: str, message: str) -> None:
        """
        Exibe um MessageBox modal em caso de erro fatal
        
        Args:
            title: Título do erro
            message: Mensagem de erro
        """
        try:
            import ctypes
            ctypes.windll.user32.MessageBoxW(0, str(message), str(title), 0x10)
        except Exception:
            # Sem UI disponível
            pass
