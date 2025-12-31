"""
NewsAPI Automation App - GUI Version (Componentized)
A visual Python app that searches NewsAPI.org using comma-separated terms.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from threading import Thread
from typing import List

from gui_styles import GUIStyles
from gui_components import HeaderComponent, InputComponent, ResultsComponent, LinkedInModal
from tuning_search import NewsAPIClient
from zai_classifier import ZAIClassifier
from image_generator import ImageGenerator


class NewsAPIGUI:
    """GUI application for NewsAPI automation."""
    
    def __init__(self, root: tk.Tk):
        """
        Initialize the GUI application.
        
        Args:
            root: The root Tkinter window
        """
        self.root = root
        self.root.title("NewsAPI Automation")
        self.root.geometry("900x700")
        self.root.minsize(700, 500)
        
        # Initialize styles
        self.styles = GUIStyles()
        self.style = ttk.Style()
        self.styles.configure_styles(self.style)
        
        # Initialize client and classifier
        self.api_connected = False
        self.api_error = None
        self._init_client()
        self.classifier = ZAIClassifier()
        self.image_generator = ImageGenerator()
        
        # Initialize components
        self.header = None
        self.input_component = None
        self.results_component = None
        
        # Build UI
        self._build_ui()
        
        # Show API status
        self._show_api_status()
    
    def _init_client(self) -> None:
        """Initialize the NewsAPI client."""
        try:
            self.client = NewsAPIClient()
            self.api_connected = True
        except ValueError as e:
            self.api_connected = False
            self.api_error = str(e)
    
    def _build_ui(self) -> None:
        """Build the user interface."""
        # Header component
        self.header = HeaderComponent(self.root, self.styles)
        self.header.pack(fill='x', padx=0, pady=0)
        
        # Main content frame
        content_frame = ttk.Frame(self.root)
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Input component
        self.input_component = InputComponent(
            content_frame,
            self.styles,
            on_search=self.on_search,
            on_clear=self.on_clear,
            on_generate_direct_post=self.on_generate_direct_post
        )
        self.input_component.pack(fill='x', pady=(0, 15))
        
        # Results component
        self.results_component = ResultsComponent(content_frame, self.styles,
                                               on_classify=self.on_classify,
                                               on_generate_post=self.on_generate_post,
                                               on_abort=self.on_abort,
                                               on_generate_image=self.on_generate_image,
                                               on_show_modal=self.on_show_modal)
        self.results_component.pack(fill='both', expand=True)
    
    def _show_api_status(self) -> None:
        """Show API connection status."""
        if self.api_connected:
            self.input_component.set_status("✓ API Connected", 'green')
        else:
            self.input_component.set_status("✗ API Error: Check .env file", 'red')
            messagebox.showerror("Configuration Error",
                               f"API Configuration Error:\n{self.api_error}")
    
    def on_search(self) -> None:
        """Handle search button click."""
        search_terms = self.input_component.get_search_terms()
        
        if not search_terms:
            messagebox.showwarning("Input Required",
                                 "Please enter at least one search term.")
            return
        
        # Disable button and show searching status
        self.input_component.set_search_button_state('disabled')
        self.input_component.set_status("Searching...", 'blue')
        self.results_component.clear()
        
        # Run search in separate thread to avoid freezing UI
        thread = Thread(target=self._perform_search, args=(search_terms,))
        thread.daemon = True
        thread.start()
    
    def _perform_search(self, search_terms: List[str]) -> None:
        """
        Perform the search in a separate thread.
        
        Args:
            search_terms: List of search terms or URLs
        """
        try:
            mode = self.input_component.get_search_mode()
            page_size = self.input_component.get_page_size()
            results = self.client.search_multiple(search_terms, mode=mode, pageSize=page_size)
            
            # Update UI from main thread
            self.root.after(0, lambda: self._display_results(results))
        except Exception as e:
            self.root.after(0, lambda: self._display_error(str(e)))
    
    def _display_results(self, results: List[dict]) -> None:
        """
        Display search results.
        
        Args:
            results: List of search result dictionaries
        """
        self.results_component.display_results(results)
        
        # Re-enable button and update status
        self.input_component.set_search_button_state('normal')
        self.input_component.set_status(f"✓ Found {len(results)} result(s)", 'green')
    
    def _display_error(self, error_msg: str) -> None:
        """
        Display error message.
        
        Args:
            error_msg: The error message
        """
        self.results_component.display_error(error_msg)
        self.input_component.set_search_button_state('normal')
        self.input_component.set_status("✗ Error occurred", 'red')
    
    def on_clear(self) -> None:
        """Handle clear button click."""
        self.input_component.clear()
        self.results_component.clear()
        self.results_component.reset_to_search_state()
        self.input_component.set_status("Ready", 'black')
    
    def on_generate_direct_post(self) -> None:
        """Handle generate direct post button click."""
        input_text = self.input_component.get_input_text()
        
        if not input_text:
            messagebox.showwarning("Input Required",
                                 "Please enter text for the post.")
            return
        
        # Disable button and show generating status
        self.input_component.generate_direct_post_button.config(state='disabled')
        self.input_component.set_status("Generating LinkedIn post...", 'blue')
        
        # Run post generation in separate thread to avoid freezing UI
        thread = Thread(target=self._perform_direct_post_generation, args=(input_text,))
        thread.daemon = True
        thread.start()
    
    def on_classify(self, articles: List[dict]) -> None:
        """
        Handle classify button click.
        
        Args:
            articles: List of article dictionaries to classify
        """
        # Disable classify button and show classifying status
        self.results_component.classify_button.config(state='disabled')
        self.input_component.set_status("Classifying with GLM...", 'blue')
        
        # Run classification in separate thread to avoid freezing UI
        thread = Thread(target=self._perform_classification, args=(articles,))
        thread.daemon = True
        thread.start()
    
    def _perform_classification(self, articles: List[dict]) -> None:
        """
        Perform the classification in a separate thread.
        
        Args:
            articles: List of article dictionaries
        """
        try:
            classification = self.classifier.classify_news(articles)
            print(f"DEBUG: Classification result: {classification[:200] if classification else 'None'}")
            
            # Update UI from main thread
            self.root.after(0, lambda: self._display_classification(classification))
        except Exception as e:
            print(f"DEBUG: Classification error: {str(e)}")
            self.root.after(0, lambda: self._display_classification_error(str(e)))
    
    def _display_classification(self, classification: str) -> None:
        """
        Display classification result.
        
        Args:
            classification: The classification result text
        """
        self.results_component.display_classification(classification)
        
        # Re-enable button and update status
        self.results_component.classify_button.config(state='normal')
        self.input_component.set_status("✓ Classification complete", 'green')
    
    def _display_classification_error(self, error_msg: str) -> None:
        """
        Display classification error.
        
        Args:
            error_msg: The error message
        """
        self.results_component.display_error(f"Classification error: {error_msg}")
        self.results_component.classify_button.config(state='normal')
        self.input_component.set_status("✗ Classification error", 'red')
    
    def on_abort(self) -> None:
        """Handle abort button click - clears everything and returns to search."""
        self.input_component.clear()
        self.results_component.clear()
        self.results_component.reset_to_search_state()
        self.input_component.set_status("Ready", 'black')
    
    def on_select_article(self, article: dict) -> None:
        """
        Handle select article button click.
        
        Args:
            article: The selected article dictionary
        """
        # Get the selected article and comment
        comment = self.results_component.get_comment()
        
        # Disable buttons and show generating status
        self.results_component.generate_selected_post_button.config(state='disabled')
        self.results_component.abort_button.config(state='disabled')
        self.input_component.set_status("Generating LinkedIn post...", 'blue')
        
        # Run post generation in separate thread to avoid freezing UI
        thread = Thread(target=self._perform_article_post_generation, args=(article, comment))
        thread.daemon = True
        thread.start()
    
    def on_generate_post(self, classification: str) -> None:
        """
        Handle generate post button click.
        
        Args:
            classification: The classification result text
        """
        # Disable buttons and show generating status
        self.results_component.generate_post_button.config(state='disabled')
        self.results_component.abort_button.config(state='disabled')
        self.input_component.set_status("Generating LinkedIn post...", 'blue')
        
        # Run post generation in separate thread to avoid freezing UI
        thread = Thread(target=self._perform_post_generation, args=(classification,))
        thread.daemon = True
        thread.start()
    
    def _perform_article_post_generation(self, article: dict, comment: str = "") -> None:
        """
        Perform the LinkedIn post generation for a specific article in a separate thread.
        
        Args:
            article: The selected article dictionary
            comment: Optional comment/instruction for the AI
        """
        try:
            post = self.classifier.generate_linkedin_post_from_article(article, comment)
            print(f"DEBUG: Generated post from article: {post[:200] if post else 'None'}")
            
            # Update UI from main thread
            self.root.after(0, lambda: self._display_generated_post(post))
        except Exception as e:
            print(f"DEBUG: Post generation error: {str(e)}")
            self.root.after(0, lambda: self._display_post_generation_error(str(e)))
    
    def _perform_post_generation(self, classification: str) -> None:
        """
        Perform the LinkedIn post generation in a separate thread.
        
        Args:
            classification: The classification result text
        """
        try:
            post = self.classifier.generate_linkedin_post(classification)
            print(f"DEBUG: Generated post: {post[:200] if post else 'None'}")
            
            # Update UI from main thread
            self.root.after(0, lambda: self._display_generated_post(post))
        except Exception as e:
            print(f"DEBUG: Post generation error: {str(e)}")
            self.root.after(0, lambda: self._display_post_generation_error(str(e)))
    
    def _perform_direct_post_generation(self, input_text: str) -> None:
        """
        Perform the LinkedIn post generation directly from input text in a separate thread.
        
        Args:
            input_text: The input text to generate a post from
        """
        try:
            post = self.classifier.generate_linkedin_post_direct(input_text)
            print(f"DEBUG: Generated post from input: {post[:200] if post else 'None'}")
            
            # Update UI from main thread
            self.root.after(0, lambda: self._display_generated_post(post))
            
            # Re-enable the direct post button
            def enable_direct_post_button():
                self.input_component.generate_direct_post_button.config(state='normal')
            self.root.after(500, enable_direct_post_button)
        except Exception as e:
            print(f"DEBUG: Post generation error: {str(e)}")
            self.root.after(0, lambda: self._display_post_generation_error(str(e)))
            
            # Re-enable the direct post button on error
            def enable_direct_post_button():
                self.input_component.generate_direct_post_button.config(state='normal')
            self.root.after(500, enable_direct_post_button)
    
    def _display_generated_post(self, post: str) -> None:
        """
        Display the generated LinkedIn post.
        
        Args:
            post: The generated post text
        """
        self.results_component.display_generated_post(post)
        
        # Re-enable abort button and update status
        self.results_component.abort_button.config(state='normal')
        self.input_component.set_status("✓ LinkedIn post generated", 'green')
    
    def on_generate_image(self, post: str) -> None:
        """
        Handle generate image button click.
        
        Args:
            post: The generated LinkedIn post text
        """
        # Disable buttons and show generating status
        self.results_component.generate_image_button.config(state='disabled')
        self.results_component.abort_button.config(state='disabled')
        self.input_component.set_status("Generating image...", 'blue')
        
        # Run image generation in separate thread to avoid freezing UI
        thread = Thread(target=self._perform_image_generation, args=(post,))
        thread.daemon = True
        thread.start()
    
    def _perform_image_generation(self, post: str) -> None:
        """
        Perform the image generation in a separate thread.
        
        Args:
            post: The generated LinkedIn post text
        """
        try:
            result = self.image_generator.generate_image(post)
            print(f"DEBUG: Image generation result: {result}")
            
            # Update UI from main thread
            self.root.after(0, lambda: self._display_generated_image(result))
            
            # After a short delay, enable the modal button
            def enable_modal_button():
                if result and result.startswith("images\\"):
                    self.results_component.show_modal_button.config(state='normal')
            self.root.after(2000, enable_modal_button)
        except Exception as e:
            print(f"DEBUG: Image generation error: {str(e)}")
            self.root.after(0, lambda: self._display_image_generation_error(str(e)))
    
    def _display_generated_image(self, result: str) -> None:
        """
        Display the generated image URL and local path.
        
        Args:
            result: The generated image URL or local path
        """
        # Check if result is a local path (starts with "images/")
        if result and (result.startswith("images/") or result.startswith("images\\")):
            local_image_path = result
            image_url = result  # Use local path as URL for display
        else:
            local_image_path = ""
            image_url = result
        
        self.results_component.display_generated_image(image_url, local_image_path)
        
        # Re-enable abort button and update status
        self.results_component.abort_button.config(state='normal')
        self.input_component.set_status("✓ Image generated", 'green')
    
    def _display_image_generation_error(self, error_msg: str) -> None:
        """
        Display image generation error.
        
        Args:
            error_msg: The error message
        """
        self.results_component.display_error(f"Image generation error: {error_msg}")
        self.results_component.abort_button.config(state='normal')
        self.results_component.generate_image_button.config(state='normal')
        self.input_component.set_status("✗ Image generation error", 'red')
    
    def on_show_modal(self, post: str, image_url: str, local_image_path: str = None) -> None:
        """
        Handle show modal button click.
        
        Args:
            post: The generated LinkedIn post text
            image_url: The generated image URL
            local_image_path: Local path to the downloaded image
        """
        modal = LinkedInModal(self.root, self.styles, post, image_url, local_image_path)
    
    def _display_post_generation_error(self, error_msg: str) -> None:
        """
        Display post generation error.
        
        Args:
            error_msg: The error message
        """
        self.results_component.display_error(f"Post generation error: {error_msg}")
        self.results_component.abort_button.config(state='normal')
        self.results_component.generate_post_button.config(state='normal')
        self.input_component.set_status("✗ Post generation error", 'red')


def main() -> None:
    """Main function to run the GUI application."""
    root = tk.Tk()
    app = NewsAPIGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
