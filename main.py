"""
TuningSearch Automation App - Main Entry Point
A local Python app that searches TuningSearch.com using comma-separated terms.
"""

import sys
import io
from typing import List
from tuning_search import TuningSearchClient

# Set UTF-8 encoding for Windows console
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def parse_input(input_string: str) -> List[str]:
    """
    Parse comma-separated input string into a list of search terms.
    
    Args:
        input_string: String containing comma-separated search terms
        
    Returns:
        List of cleaned search terms
    """
    # Split by comma and strip whitespace
    terms = [term.strip() for term in input_string.split(",")]
    # Filter out empty strings
    terms = [term for term in terms if term]
    return terms


def main():
    """Main function to run the TuningSearch automation app."""
    print("=" * 80)
    print("TUNINGSEARCH AUTOMATION APP")
    print("=" * 80)
    print()
    print("Search TuningSearch.com using comma-separated terms.")
    print("Example: 'car tuning, engine performance, suspension'")
    print()
    print("Type 'exit' or 'quit' to close the application.")
    print("=" * 80)
    print()
    
    # Initialize the TuningSearch client
    try:
        client = TuningSearchClient()
        print("✓ Connected to TuningSearch API")
        print()
    except ValueError as e:
        print(f"✗ Configuration Error: {e}")
        print("Please check your .env file and ensure TUNINGSEARCH_API_KEY is set.")
        sys.exit(1)
    
    # Main loop
    while True:
        try:
            # Get user input
            user_input = input("Enter search terms (comma-separated): ").strip()
            
            # Check for exit command
            if user_input.lower() in ["exit", "quit"]:
                print("\nGoodbye!")
                break
            
            # Parse input
            search_terms = parse_input(user_input)
            
            if not search_terms:
                print("⚠ No valid search terms provided. Please try again.\n")
                continue
            
            print(f"\nSearching for: {', '.join(search_terms)}")
            print("Please wait...\n")
            
            # Perform search
            results = client.search_multiple(search_terms)
            
            # Display results
            formatted_output = client.format_results(results)
            print(formatted_output)
            print()
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\n✗ An error occurred: {e}\n")


if __name__ == "__main__":
    main()
