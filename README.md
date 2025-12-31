# NewsAPI Automation App

A visual Python application that searches NewsAPI.org using comma-separated terms, classifies articles with GLM-4, generates LinkedIn posts, and creates AI images.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Features

- 🔍 **Search NewsAPI.org** - Search for news articles using multiple terms
- 🤖 **AI Classification** - Classify articles using GLM-4 AI model
- 📝 **LinkedIn Post Generation** - Generate professional LinkedIn posts
- 🖼️ **AI Image Generation** - Create images using Replicate API (Flux)
- 👁️ **Preview Modal** - Preview posts in a LinkedIn-style modal with copy options
- 📋 **Copy to Clipboard** - Copy text and images with one click

## Screenshots

The application features a clean, modern GUI with:

- Search input with multiple modes
- Real-time results display
- Action buttons for classification, post generation, and image creation
- LinkedIn-style preview modal with scrollable content

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (usually comes with Python)

### Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/newsapi-automation.git
cd newsapi-automation
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure API keys:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
NEWS_API_KEY=your_newsapi_key_here
ZAI_API_KEY=your_zai_api_key_here
REPLICATE_API_TOKEN=your_replicate_token_here
```

## Usage

### Running the App

```bash
python gui_app.py
```

Or run the main entry point:

```bash
python main.py
```

### Workflow

1. **Search** - Enter search terms (comma-separated) and click Search
2. **Classify** - Click "🤖 Classificar com GLM" to classify articles with AI
3. **Generate Post** - Click "📝 Gerar Notícia" to create a LinkedIn post
4. **Generate Image** - Click "🖼️ Gerar Imagem" to create an AI image
5. **Preview** - Click "👁️ Mostrar no Modal" to preview in LinkedIn style

### Search Modes

- **everything** - Search all news articles
- **top-headlines** - Get top headlines
- **sources** - Search news sources by category

## Building Windows Executable

### Quick Build

Double-click `build.bat` or run:

```bash
python build.py
```

The executable will be created in `dist/NewsAPI_Automation.exe` with:

- Custom icon
- Embedded `.env` file (no need to copy it separately)
- All dependencies included

### Debug Build

For debugging, create an executable with console:

```bash
python build.py --debug
```

Or double-click `build_debug.bat`

### Distribution

Only the `NewsAPI_Automation.exe` file is needed for distribution - the `.env` is embedded!

To override API keys, place an external `.env` file in the same directory as the `.exe`.

## Project Structure

```
newsapi-automation/
├── gui_app.py              # Main GUI application
├── gui_components.py        # GUI components (Header, Input, Results, Modal)
├── gui_styles.py           # GUI styling
├── tuning_search.py         # NewsAPI client
├── zai_classifier.py       # GLM-4 AI classifier
├── image_generator.py       # Image generation (Replicate)
├── zai_prompts.py          # AI prompts
├── config.py               # Configuration management
├── main.py                 # CLI entry point
├── requirements.txt         # Python dependencies
├── .env.example            # Example environment variables
├── build.py                # Build script for .exe
├── build.bat               # Windows build script
├── build_debug.bat          # Debug build script
├── create_icon.py          # Icon generator
└── README.md               # This file
```

## API Keys Required

### NewsAPI.org

- Get your free API key at: https://newsapi.org/register

### ZAI (GLM-4)

- Get your API key at: https://open.bigmodel.cn/

### Replicate (Flux Image Generation)

- Get your token at: https://replicate.com/account/api-tokens

## Configuration

Edit `.env` file to configure:

```env
# NewsAPI Configuration
NEWS_API_KEY=your_key_here
NEWS_API_BASE=https://newsapi.org/v2

# ZAI GLM API Configuration
ZAI_API_KEY=your_key_here
ZAI_API_BASE=https://api.z.ai/api/coding/paas/v4
ZAI_MODEL=GLM-4.5-Air

# Replicate API Configuration
REPLICATE_API_TOKEN=your_token_here

# News Sources Configuration
DEFAULT_LANGUAGE=pt
MAX_NEWS_PER_SOURCE=10
DEFAULT_CATEGORY=general
```

## Troubleshooting

### "NEWS_API_KEY is not set" error

Make sure your `.env` file is in the same directory as the executable (or embedded during build).

### Image not showing in modal

1. Check that the image was generated successfully
2. Verify the image path in the results area
3. Try generating the image again

### Build errors

If PyInstaller fails, try:

```bash
pip install --upgrade pyinstaller
python build.py --debug
```

## Development

### Running Tests

```bash
# Run the GUI
python gui_app.py

# Run the CLI version
python main.py
```

### Adding Features

The application is modular:

- GUI components in `gui_components.py`
- API clients in `tuning_search.py`
- AI integration in `zai_classifier.py` and `image_generator.py`

## License

MIT License - feel free to use this project for personal or commercial purposes.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions:

- Open an issue on GitHub
- Check the troubleshooting section above

## Acknowledgments

- NewsAPI.org for news data
- ZAI for GLM-4 AI model
- Replicate for Flux image generation
- Tkinter for GUI framework
- PyInstaller for executable creation
