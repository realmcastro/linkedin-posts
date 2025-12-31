"""
GUI Styles Module
Contains style configurations for the TuningSearch GUI application.
"""

import tkinter as tk
from tkinter import ttk


class GUIStyles:
    """Class to manage GUI styles and colors."""
    
    def __init__(self):
        """Initialize the GUI styles."""
        self.colors = {
            'primary': '#2c3e50',
            'secondary': '#34495e',
            'accent': '#3498db',
            'success': '#27ae60',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'light': '#ecf0f1',
            'white': '#ffffff'
        }
    
    def configure_styles(self, style: ttk.Style) -> None:
        """
        Configure custom styles for widgets.
        
        Args:
            style: The ttk.Style object to configure
        """
        # Use modern theme
        style.theme_use('clam')
        
        # Header frame style
        style.configure('Header.TFrame', background=self.colors['primary'])
        
        # Title label style
        style.configure('Title.TLabel', 
                       background=self.colors['primary'],
                       foreground=self.colors['white'],
                       font=('Segoe UI', 16, 'bold'))
        
        # Subtitle label style
        style.configure('Subtitle.TLabel',
                       background=self.colors['primary'],
                       foreground=self.colors['light'],
                       font=('Segoe UI', 9))
        
        # Input frame style
        style.configure('Input.TFrame', background=self.colors['light'])
        
        # Label style
        style.configure('TLabel',
                       background=self.colors['white'],
                       foreground=self.colors['primary'],
                       font=('Segoe UI', 10))
        
        # Button styles
        style.configure('Primary.TButton',
                       background=self.colors['accent'],
                       foreground=self.colors['white'],
                       font=('Segoe UI', 11, 'bold'),
                       borderwidth=0)
        style.map('Primary.TButton',
                 background=[('active', '#2980b9')])
        
        style.configure('Secondary.TButton',
                       background=self.colors['secondary'],
                       foreground=self.colors['white'],
                       font=('Segoe UI', 10),
                       borderwidth=0)
        style.map('Secondary.TButton',
                  background=[('active', '#2c3e50')])
        
        style.configure('Danger.TButton',
                       background=self.colors['danger'],
                       foreground=self.colors['white'],
                       font=('Segoe UI', 10),
                       borderwidth=0)
        style.map('Danger.TButton',
                  background=[('active', '#c0392b')])
        
        # Status label style
        style.configure('Status.TLabel',
                       background=self.colors['light'],
                       font=('Segoe UI', 9))
        
        # Result frame style
        style.configure('Result.TFrame', background=self.colors['white'])
    
    def get_color(self, name: str) -> str:
        """
        Get a color by name.
        
        Args:
            name: The name of the color
            
        Returns:
            The color hex code
        """
        return self.colors.get(name, '#000000')
