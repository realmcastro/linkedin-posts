"""
GUI Components Module
Contains individual GUI components for the NewsAPI application.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
from typing import Callable, List
from gui_styles import GUIStyles
from PIL import Image, ImageTk


class HeaderComponent:
    """Header component with title and subtitle."""
    
    def __init__(self, parent: tk.Widget, styles: GUIStyles):
        """
        Initialize the header component.
        
        Args:
            parent: The parent widget
            styles: The GUI styles object
        """
        self.parent = parent
        self.styles = styles
        self.frame = ttk.Frame(parent, style='Header.TFrame')
        self._build()
    
    def _build(self) -> None:
        """Build the header UI."""
        # Title
        title_label = ttk.Label(self.frame, text="📰 NewsAPI Automation",
                              style='Title.TLabel')
        title_label.pack(pady=(15, 5))
        
        # Subtitle
        subtitle_label = ttk.Label(self.frame,
                                  text="Search NewsAPI.org using comma-separated terms",
                                  style='Subtitle.TLabel')
        subtitle_label.pack(pady=(0, 15))
    
    def pack(self, **kwargs) -> None:
        """Pack the frame."""
        self.frame.pack(**kwargs)


class InputComponent:
    """Input component for search terms."""
    
    def __init__(self, parent: tk.Widget, styles: GUIStyles,
                 on_search: Callable, on_clear: Callable):
        """
        Initialize the input component.
        
        Args:
            parent: The parent widget
            styles: The GUI styles object
            on_search: Callback function for search action
            on_clear: Callback function for clear action
        """
        self.parent = parent
        self.styles = styles
        self.on_search = on_search
        self.on_clear = on_clear
        
        self.frame = ttk.LabelFrame(parent, text="Search Terms", padding=15)
        self.search_entry = None
        self.search_button = None
        self.status_label = None
        self.mode_var = None
        self.example_label = None
        
        self._build()
    
    def _build(self) -> None:
        """Build the input UI."""
        # Mode selector frame
        mode_frame = ttk.Frame(self.frame)
        mode_frame.pack(fill='x', pady=(0, 8))
        
        # Mode label
        mode_label = ttk.Label(mode_frame, text="Search Mode:")
        mode_label.pack(side='left', padx=(0, 10))
        
        # Mode dropdown
        self.mode_var = tk.StringVar(value="everything")
        mode_combo = ttk.Combobox(mode_frame, textvariable=self.mode_var,
                                  values=["everything", "top-headlines", "sources"],
                                  state="readonly", width=15)
        mode_combo.pack(side='left')
        mode_combo.bind('<<ComboboxSelected>>', self._on_mode_change)
        
        # Page size selector
        pagesize_label = ttk.Label(mode_frame, text="Results:")
        pagesize_label.pack(side='left', padx=(20, 5))
        
        self.pagesize_var = tk.StringVar(value="10")
        pagesize_combo = ttk.Combobox(mode_frame, textvariable=self.pagesize_var,
                                      values=["5", "10", "20", "30", "50", "100"],
                                      state="readonly", width=10)
        pagesize_combo.pack(side='left')
        
        # Input label
        self.input_label = ttk.Label(self.frame,
                                    text="Enter search terms separated by commas:")
        self.input_label.pack(anchor='w', pady=(0, 8))
        
        # Input entry
        self.search_entry = ttk.Entry(self.frame, font=('Segoe UI', 11))
        self.search_entry.pack(fill='x', pady=(0, 10))
        self.search_entry.bind('<Return>', lambda e: self.on_search())
        
        # Example label
        self.example_label = ttk.Label(self.frame,
                                       text="Example: car tuning, engine performance, suspension",
                                       font=('Segoe UI', 8),
                                       foreground='gray')
        self.example_label.pack(anchor='w', pady=(0, 10))
        
        # Button frame
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill='x')
        
        # Search button
        self.search_button = ttk.Button(button_frame, text="🔎 Search",
                                       style='Primary.TButton',
                                       command=self.on_search)
        self.search_button.pack(side='left', padx=(0, 10))
        
        # Clear button
        clear_button = ttk.Button(button_frame, text="🗑 Clear",
                                 style='Secondary.TButton',
                                 command=self.on_clear)
        clear_button.pack(side='left')
        
        # Status label
        self.status_label = ttk.Label(button_frame, text="Ready",
                                     style='Status.TLabel')
        self.status_label.pack(side='right')
    
    def _on_mode_change(self, event) -> None:
        """Handle mode selection change."""
        mode = self.mode_var.get()
        if mode == "sources":
            self.input_label.config(text="Enter categories separated by commas:")
            self.example_label.config(text="Example: technology, business, sports")
        elif mode == "top-headlines":
            self.input_label.config(text="Enter search terms separated by commas:")
            self.example_label.config(text="Example: AI, technology, news")
        else:  # everything
            self.input_label.config(text="Enter search terms separated by commas:")
            self.example_label.config(text="Example: artificial intelligence, machine learning, python")
    
    def pack(self, **kwargs) -> None:
        """Pack the frame."""
        self.frame.pack(**kwargs)
    
    def get_search_terms(self) -> List[str]:
        """
        Get and parse search terms from input.
        
        Returns:
            List of search terms or categories
        """
        input_text = self.search_entry.get().strip()
        if not input_text:
            return []
        
        mode = self.mode_var.get()
        if mode == "sources":
            # For sources mode, split by commas
            terms = [term.strip() for term in input_text.split(",")]
        else:
            # For everything and top-headlines modes, split by commas
            terms = [term.strip() for term in input_text.split(",")]
        
        terms = [term for term in terms if term]
        return terms
    
    def get_search_mode(self) -> str:
        """
        Get the selected search mode.
        
        Returns:
            The selected mode ('search', 'news', or 'crawl')
        """
        return self.mode_var.get()
    
    def get_page_size(self) -> int:
        """
        Get the selected page size.
        
        Returns:
            The selected page size as integer
        """
        try:
            return int(self.pagesize_var.get())
        except (ValueError, AttributeError):
            return 10
    
    def clear(self) -> None:
        """Clear the input field."""
        self.search_entry.delete(0, tk.END)
    
    def set_status(self, text: str, foreground: str = 'black') -> None:
        """
        Set the status label text and color.
        
        Args:
            text: The status text
            foreground: The text color
        """
        self.status_label.config(text=text, foreground=foreground)
    
    def set_search_button_state(self, state: str) -> None:
        """
        Set the search button state.
        
        Args:
            state: 'normal' or 'disabled'
        """
        self.search_button.config(state=state)


class ResultsComponent:
    """Results component for displaying search results."""
    
    def __init__(self, parent: tk.Widget, styles: GUIStyles, on_classify: Callable = None, on_generate_post: Callable = None, on_abort: Callable = None, on_generate_image: Callable = None, on_show_modal: Callable = None):
        """
        Initialize the results component.
        
        Args:
            parent: The parent widget
            styles: The GUI styles object
            on_classify: Callback function for classification action
            on_generate_post: Callback function for generate post action
            on_abort: Callback function for abort action
            on_generate_image: Callback function for generate image action
            on_show_modal: Callback function for show modal action
        """
        self.parent = parent
        self.styles = styles
        self.on_classify = on_classify
        self.on_generate_post = on_generate_post
        self.on_abort = on_abort
        self.on_generate_image = on_generate_image
        self.on_show_modal = on_show_modal
        self.frame = ttk.LabelFrame(parent, text="Results", padding=15)
        self.results_text = None
        self.classify_button = None
        self.generate_post_button = None
        self.abort_button = None
        self.generate_image_button = None
        self.show_modal_button = None
        self.current_articles = []
        self.current_classification = ""
        self.current_post = ""
        self.current_image_url = ""
        self.current_local_image_path = ""
        self._build()
    
    def _build(self) -> None:
        """Build the results UI."""
        # Button frame for classification
        self.button_frame = ttk.Frame(self.frame)
        self.button_frame.pack(fill='x', pady=(0, 10))
        
        # Classify button (initially hidden)
        self.classify_button = ttk.Button(self.button_frame, text="🤖 Classificar com GLM",
                                        style='Primary.TButton',
                                        command=self._on_classify,
                                        state='disabled')
        self.classify_button.pack(side='right')
        
        # Abort button (initially hidden)
        self.abort_button = ttk.Button(self.button_frame, text="❌ Abortar",
                                       style='Danger.TButton',
                                       command=self._on_abort,
                                       state='hidden')
        self.abort_button.pack(side='right', padx=(0, 10))
        
        # Generate post button (initially hidden)
        self.generate_post_button = ttk.Button(self.button_frame, text="📝 Gerar Notícia",
                                                style='Secondary.TButton',
                                                command=self._on_generate_post,
                                                state='hidden')
        self.generate_post_button.pack(side='right', padx=(0, 10))
        
        # Generate image button (initially hidden)
        self.generate_image_button = ttk.Button(self.button_frame, text="🖼️ Gerar Imagem",
                                                  style='Secondary.TButton',
                                                  command=self._on_generate_image,
                                                  state='hidden')
        self.generate_image_button.pack(side='right', padx=(0, 10))
        
        # Show modal button (initially hidden)
        self.show_modal_button = ttk.Button(self.button_frame, text="👁️ Mostrar no Modal",
                                              style='Primary.TButton',
                                              command=self._on_show_modal,
                                              state='hidden')
        self.show_modal_button.pack(side='right', padx=(0, 10))
        
        # Results text area
        self.results_text = scrolledtext.ScrolledText(self.frame,
                                                      wrap='word',
                                                      font=('Consolas', 10),
                                                      bg='#f8f9fa')
        self.results_text.pack(fill='both', expand=True)
        
        # Configure text tags
        self.results_text.tag_config('header', font=('Consolas', 12, 'bold'))
        self.results_text.tag_config('query', font=('Consolas', 11, 'bold'))
        self.results_text.tag_config('separator', font=('Consolas', 10))
        self.results_text.tag_config('error', foreground='red')
        self.results_text.tag_config('success', foreground='green')
        self.results_text.tag_config('classification', font=('Consolas', 10, 'bold'), foreground='blue')
    
    def pack(self, **kwargs) -> None:
        """Pack the frame."""
        self.frame.pack(**kwargs)
    
    def clear(self) -> None:
        """Clear the results text area."""
        self.results_text.delete(1.0, tk.END)
    
    def append_text(self, text: str, tag: str = None) -> None:
        """
        Append text to the results area.
        
        Args:
            text: The text to append
            tag: Optional tag for styling
        """
        if tag:
            self.results_text.insert(tk.END, text, tag)
        else:
            self.results_text.insert(tk.END, text)
    
    def display_results(self, results: List[dict]) -> None:
        """
        Display search results in the text area.
        
        Args:
            results: List of search result dictionaries
        """
        self.clear()
        self.current_articles = []
        
        # Header
        self.append_text("=" * 80 + "\n", 'header')
        self.append_text("NEWSAPI.ORG RESULTS\n", 'header')
        self.append_text("=" * 80 + "\n\n", 'header')
        
        for i, result in enumerate(results, 1):
            if "error" in result:
                mode = result.get('mode', 'everything')
                mode_desc = self._get_mode_description(mode)
                self.append_text(f"[{i}] Query: {result.get('query', 'Unknown')}\n", 'query')
                self.append_text(f"    Mode: {mode_desc} ({mode})\n")
                self.append_text(f"    Status: FAILED - {result['error']}\n\n", 'error')
            elif result.get("status") == "ok":
                mode = result.get('mode', 'everything')
                query = result.get('query', 'Unknown')
                mode_desc = self._get_mode_description(mode)
                self.append_text(f"[{i}] Query: {query}\n", 'query')
                self.append_text(f"    Mode: {mode_desc} ({mode})\n")
                self.append_text("-" * 40 + "\n", 'separator')
                
                # Display total results
                total_results = result.get("totalResults", 0)
                self.append_text(f"    Total Results: {total_results}\n\n")
                
                # Display articles or sources
                if mode == "sources":
                    if "sources" in result:
                        for j, source in enumerate(result["sources"], 1):
                            self.append_text(f"    Source {j}:\n")
                            self.append_text(f"        ID: {source.get('id', 'N/A')}\n")
                            self.append_text(f"        Name: {source.get('name', 'N/A')}\n")
                            description = source.get('description') or 'N/A'
                            if description != 'N/A' and len(description) > 150:
                                description = description[:150] + "..."
                            self.append_text(f"        Description: {description}\n")
                            self.append_text(f"        Category: {source.get('category', 'N/A')}\n")
                            self.append_text(f"        Language: {source.get('language', 'N/A')}\n")
                            self.append_text(f"        Country: {source.get('country', 'N/A')}\n")
                            self.append_text("\n")
                else:
                    if "articles" in result:
                        for j, article in enumerate(result["articles"], 1):
                            self.append_text(f"    Article {j}:\n")
                            self.append_text(f"        Title: {article.get('title', 'N/A')}\n")
                            self.append_text(f"        Source: {article.get('source', {}).get('name', 'N/A')}\n")
                            self.append_text(f"        Author: {article.get('author', 'N/A')}\n")
                            self.append_text(f"        URL: {article.get('url', 'N/A')}\n")
                            self.append_text(f"        Published: {article.get('publishedAt', 'N/A')}\n")
                            description = article.get('description') or 'N/A'
                            if description != 'N/A' and len(description) > 200:
                                description = description[:200] + "..."
                            self.append_text(f"        Description: {description}\n")
                            self.append_text("\n")
                            # Store article for classification
                            self.current_articles.append(article)
            else:
                # Handle unexpected response format
                self.append_text(f"[{i}] Query: {result.get('query', 'Unknown')}\n", 'query')
                self.append_text(f"    Status: Unexpected response format\n", 'error')
                self.append_text(f"    Response: {result}\n\n")
        
        self.append_text("=" * 80 + "\n", 'header')
        
        # Enable classify button if there are articles
        if self.current_articles and self.on_classify:
            self.classify_button.config(state='normal')
        else:
            self.classify_button.config(state='disabled')
    
    def _on_classify(self) -> None:
        """Handle classify button click."""
        if self.on_classify and self.current_articles:
            self.on_classify(self.current_articles)
    
    def _on_abort(self) -> None:
        """Handle abort button click."""
        if self.on_abort:
            self.on_abort()
    
    def _on_generate_post(self) -> None:
        """Handle generate post button click."""
        if self.on_generate_post and self.current_classification:
            self.on_generate_post(self.current_classification)
    
    def _on_generate_image(self) -> None:
        """Handle generate image button click."""
        if self.on_generate_image and self.current_post:
            self.on_generate_image(self.current_post)
    
    def _on_show_modal(self) -> None:
        """Handle show modal button click."""
        if self.on_show_modal:
            self.on_show_modal(self.current_post, self.current_image_url, self.current_local_image_path)
    
    def display_classification(self, classification: str) -> None:
        """
        Display classification result.
        
        Args:
            classification: The classification result text
        """
        print(f"DEBUG: display_classification called with: {classification[:200] if classification else 'None'}")
        self.current_classification = classification
        self.append_text("\n" + "=" * 80 + "\n", 'header')
        self.append_text("CLASSIFICAÇÃO GLM\n", 'header')
        self.append_text("=" * 80 + "\n\n", 'header')
        self.append_text(classification + "\n", 'classification')
        self.append_text("=" * 80 + "\n", 'header')
        # Scroll to the end to show the classification
        self.results_text.see(tk.END)
        
        # Hide classify button, show abort and generate buttons
        self.classify_button.pack_forget()
        self.abort_button.config(state='normal')
        self.generate_post_button.config(state='normal')
    
    def reset_to_search_state(self) -> None:
        """Reset UI to initial search state."""
        # Hide all action buttons
        self.abort_button.config(state='hidden')
        self.generate_post_button.config(state='hidden')
        self.generate_image_button.config(state='hidden')
        self.show_modal_button.config(state='hidden')
        
        # Show classify button (disabled)
        self.classify_button.pack(side='right')
        self.classify_button.config(state='disabled')
        
        # Clear stored data
        self.current_articles = []
        self.current_classification = ""
        self.current_post = ""
        self.current_image_url = ""
        self.current_local_image_path = ""
    
    def display_error(self, error_msg: str) -> None:
        """
        Display an error message.
        
        Args:
            error_msg: The error message to display
        """
        self.append_text(f"Error: {error_msg}\n", 'error')
    
    def display_generated_post(self, post: str) -> None:
        """
        Display the generated LinkedIn post.
        
        Args:
            post: The generated post text
        """
        self.current_post = post
        self.append_text("\n" + "=" * 80 + "\n", 'header')
        self.append_text("LINKEDIN POST GERADO\n", 'header')
        self.append_text("=" * 80 + "\n\n", 'header')
        self.append_text(post + "\n", 'success')
        self.append_text("=" * 80 + "\n", 'header')
        # Scroll to the end to show the post
        self.results_text.see(tk.END)
        
        # Show generate image button
        self.generate_image_button.config(state='normal')
    
    def display_generated_image(self, image_url: str, local_image_path: str = "") -> None:
        """
        Display the generated image URL.
        
        Args:
            image_url: The generated image URL
            local_image_path: Local path to the downloaded image
        """
        self.current_image_url = image_url
        self.current_local_image_path = local_image_path
        self.append_text("\n" + "=" * 80 + "\n", 'header')
        self.append_text("IMAGEM GERADA\n", 'header')
        self.append_text("=" * 80 + "\n\n", 'header')
        if local_image_path:
            self.append_text(f"Local: {local_image_path}\n", 'success')
        else:
            self.append_text(f"Image URL: {image_url}\n", 'success')
        self.append_text("=" * 80 + "\n", 'header')
        # Scroll to the end to show the image URL
        self.results_text.see(tk.END)
        
        # Show modal button
        self.show_modal_button.config(state='normal')
    
    def _get_mode_description(self, mode: str) -> str:
        """
        Get description for a search mode.
        
        Args:
            mode: The mode name
            
        Returns:
            Description of the mode
        """
        descriptions = {
            "everything": "Search all news",
            "top-headlines": "Top headlines",
            "sources": "News sources"
        }
        return descriptions.get(mode, "Unknown mode")


class LinkedInModal:
    """Modal window for LinkedIn post preview."""
    
    def __init__(self, parent: tk.Widget, styles: GUIStyles, post: str, image_url: str, local_image_path: str = None):
        """
        Initialize the LinkedIn modal.
        
        Args:
            parent: The parent widget
            styles: The GUI styles object
            post: The LinkedIn post text
            image_url: The generated image URL
            local_image_path: Local path to the downloaded image
        """
        self.parent = parent
        self.styles = styles
        self.post = post
        self.image_url = image_url
        self.local_image_path = local_image_path
        self.photo = None  # Keep reference to photo
        
        # Create modal window
        self.window = tk.Toplevel(parent)
        self.window.title("LinkedIn Post Preview")
        self.window.geometry("700x800")
        self.window.transient(parent)  # Set to be on top of parent
        self.window.grab_set()  # Modal - capture all events
        
        # Handle window close
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self._build()
    
    def _build(self) -> None:
        """Build the modal UI with LinkedIn-like styling."""
        # Main container with LinkedIn-style background
        main_frame = tk.Frame(self.window, bg='#f3f2ef')
        main_frame.pack(fill='both', expand=True)
        
        # Header bar (like LinkedIn)
        header_frame = tk.Frame(main_frame, bg='#0a66c2', height=60)
        header_frame.pack(fill='x')
        
        # LinkedIn logo placeholder
        logo_label = tk.Label(header_frame, text="in", bg='#0a66c2', fg='white',
                             font=('Arial', 24, 'bold'))
        logo_label.pack(side='left', padx=20, pady=10)
        
        # Search bar placeholder
        search_frame = tk.Frame(header_frame, bg='white')
        search_frame.pack(side='left', padx=10, pady=10)
        search_entry = tk.Entry(search_frame, width=50, bg='#eef3f8', borderwidth=0)
        search_entry.pack(padx=10, pady=5)
        
        # Scrollable content area
        canvas = tk.Canvas(main_frame, bg='#f3f2ef', highlightthickness=0)
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f3f2ef')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Container for scrollable content with padding
        content_container = tk.Frame(scrollable_frame, bg='#f3f2ef')
        content_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Post card (LinkedIn style)
        post_card = tk.Frame(content_container, bg='white', relief='solid', borderwidth=1)
        post_card.pack(fill='x')
        
        # Post header (author info)
        post_header = tk.Frame(post_card, bg='white')
        post_header.pack(fill='x', padx=15, pady=10)
        
        # Avatar placeholder
        avatar_frame = tk.Frame(post_header, width=48, height=48, bg='#c5f1f5')
        avatar_frame.pack(side='left')
        avatar_label = tk.Label(avatar_frame, text="👤", bg='#c5f1f5', font=('Arial', 20))
        avatar_label.pack()
        
        # Author info
        author_frame = tk.Frame(post_header, bg='white')
        author_frame.pack(side='left', padx=10)
        tk.Label(author_frame, text="Your Name", bg='white', font=('Arial', 14, 'bold')).pack(anchor='w')
        tk.Label(author_frame, text="Professional Network", bg='white', fg='#666666', font=('Arial', 12)).pack(anchor='w')
        tk.Label(author_frame, text="1h • 🌐", bg='white', fg='#666666', font=('Arial', 11)).pack(anchor='w')
        
        # Image display (BEFORE text)
        if self.local_image_path:
            # Display local image
            image_frame = tk.Frame(post_card, bg='white')
            image_frame.pack(fill='x', padx=15, pady=(5, 10))
            
            # Copy image button (hidden by default, shown on hover)
            copy_image_btn = tk.Button(image_frame, text="📋 Copiar Imagem",
                                       command=self._copy_image,
                                       bg='#0a66c2', fg='white', font=('Arial', 10),
                                       padx=10, pady=5, borderwidth=0, relief='flat')
            
            # Try to load and display the actual image
            try:
                pil_image = Image.open(self.local_image_path)
                
                # Resize image if too large (max 500px width)
                max_width = 500
                if pil_image.width > max_width:
                    ratio = max_width / pil_image.width
                    new_height = int(pil_image.height * ratio)
                    pil_image = pil_image.resize((max_width, new_height), Image.Resampling.LANCZOS)
                
                self.photo = ImageTk.PhotoImage(pil_image)
                image_label = tk.Label(image_frame, image=self.photo, bg='white')
                image_label.pack(pady=10)
                
                # Show/hide copy button on hover
                image_label.bind('<Enter>', lambda e: copy_image_btn.pack(pady=5))
                image_label.bind('<Leave>', lambda e: copy_image_btn.pack_forget())
                image_frame.bind('<Enter>', lambda e: copy_image_btn.pack(pady=5))
                image_frame.bind('<Leave>', lambda e: copy_image_btn.pack_forget())
            except Exception as e:
                # Fallback to placeholder if image loading fails
                print(f"DEBUG: Failed to load image: {e}")
                image_label = tk.Label(image_frame, text="🖼️ Image Generated",
                                     bg='white', fg='#666666', font=('Arial', 12))
                image_label.pack(pady=10)
            
            # URL label
            url_label = tk.Label(image_frame, text=self.image_url[:80] + "..." if len(self.image_url) > 80 else self.image_url,
                               bg='white', fg='#0a66c2', font=('Arial', 9), cursor='hand2')
            url_label.pack(pady=5)
        
        # Post content
        post_content = tk.Frame(post_card, bg='white')
        post_content.pack(fill='both', expand=True, padx=15, pady=(5, 10))
        
        # Copy text button (hidden by default, shown on hover)
        copy_text_btn = tk.Button(post_content, text="📋 Copiar Texto",
                                  command=self._copy_text,
                                  bg='#0a66c2', fg='white', font=('Arial', 10),
                                  padx=10, pady=5, borderwidth=0, relief='flat')
        
        # Post text
        post_text = tk.Text(post_content, wrap='word', bg='white', borderwidth=0,
                           font=('Arial', 14), height=10)
        post_text.pack(fill='both', expand=True)
        post_text.insert(1.0, self.post)
        post_text.config(state='disabled')
        
        # Show/hide copy button on hover
        post_text.bind('<Enter>', lambda e: copy_text_btn.pack(pady=5))
        post_text.bind('<Leave>', lambda e: copy_text_btn.pack_forget())
        post_content.bind('<Enter>', lambda e: copy_text_btn.pack(pady=5))
        post_content.bind('<Leave>', lambda e: copy_text_btn.pack_forget())
        
        # Post actions (like, comment, share)
        actions_frame = tk.Frame(post_card, bg='white')
        actions_frame.pack(fill='x', padx=15, pady=(5, 10))
        
        action_buttons = [
            ("👍 Like", "#666666"),
            ("💬 Comment", "#666666"),
            ("🔄 Repost", "#666666"),
            ("📤 Send", "#666666")
        ]
        
        for text, color in action_buttons:
            btn = tk.Button(actions_frame, text=text, bg='white', fg=color,
                           borderwidth=0, font=('Arial', 14), padx=10)
            btn.pack(side='left', padx=5)
        
        # Close button at bottom (inside scrollable area)
        close_frame = tk.Frame(content_container, bg='#f3f2ef')
        close_frame.pack(fill='x', pady=(20, 0))
        close_btn = tk.Button(close_frame, text="Fechar", command=self.on_close,
                             bg='#0a66c2', fg='white', font=('Arial', 12),
                             padx=20, pady=8, borderwidth=0)
        close_btn.pack()
    
    def _copy_text(self) -> None:
        """Copy the post text to clipboard."""
        self.window.clipboard_clear()
        self.window.clipboard_append(self.post)
        self.window.update()
    
    def _copy_image(self) -> None:
        """Copy the image to clipboard."""
        if self.local_image_path:
            try:
                # Read the image file
                with open(self.local_image_path, 'rb') as f:
                    image_data = f.read()
                
                # Put image data on clipboard
                self.window.clipboard_clear()
                self.window.clipboard_append(image_data)
                self.window.update()
            except Exception as e:
                print(f"DEBUG: Failed to copy image: {e}")
    
    def on_close(self) -> None:
        """Handle window close."""
        self.window.destroy()
