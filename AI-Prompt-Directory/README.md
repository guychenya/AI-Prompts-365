# 🤖 AI Prompt Directory

A comprehensive, searchable directory of AI prompts from top open-source repositories.

## 📊 Features

- **3,438+ Prompts** from 7 top repositories
- **10 Categories** organized by use case
- **Live Search** with real-time filtering
- **Responsive Design** works on all devices
- **Fast Performance** with client-side filtering

## 🚀 Live Demo

Visit: [AI Prompt Directory](https://your-site.netlify.app)

## 📂 Categories

- 🔧 **AI Development Tools** (183 prompts)
- 🧠 **General Purpose** (2,355 prompts)
- 💻 **Software Development** (222 prompts)
- 🎨 **User Experience** (322 prompts)
- 🎭 **Role Playing** (129 prompts)
- ✍️ **Creative Writing** (131 prompts)
- ⚙️ **System Prompts** (47 prompts)
- 📋 **Product Management** (25 prompts)
- 📚 **Education & Learning** (14 prompts)
- 📈 **Marketing & Business** (10 prompts)

## 🏃‍♂️ Quick Start

### Local Development
```bash
# Clone the repository
git clone https://github.com/guychenya/AI-Prompt-Directory.git
cd AI-Prompt-Directory

# Start local server
python3 -m http.server 8888

# Open in browser
open http://localhost:8888
```

### Regenerate Database
```bash
# Update prompts from source repositories
python3 generate_prompts.py
```

## 📦 Source Repositories

This directory aggregates prompts from:

- [awesome-chatgpt-prompts](https://github.com/f/awesome-chatgpt-prompts)
- [system-prompts-and-models-of-ai-tools](https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools)
- [awesome-ai-system-prompts](https://github.com/dontriskit/awesome-ai-system-prompts)
- [AI-Prompt-Database](https://github.com/mrinasugosh/AI-Prompt-Database)
- [Awesome-Prompt-Engineering](https://github.com/promptslab/Awesome-Prompt-Engineering)
- [awesome-prompts](https://github.com/ai-boost/awesome-prompts)
- [ChatGPT-System-Prompts](https://github.com/mustvlad/ChatGPT-System-Prompts)

## 🛠️ Tech Stack

- **Frontend**: Pure HTML, CSS, JavaScript
- **Data**: JSON database generated from markdown/CSV sources
- **Hosting**: Netlify
- **CI/CD**: GitHub Actions (optional)

## 📄 License

This project is open source. Individual prompts may have their own licensing terms from source repositories.

## 🤝 Contributing

1. Fork the repository
2. Add new prompt sources to `generate_prompts.py`
3. Run the generator to update the database
4. Submit a pull request

## 🙏 Acknowledgments

Thanks to all the amazing open-source contributors who created the original prompt repositories that make this directory possible.