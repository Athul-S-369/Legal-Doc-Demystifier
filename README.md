# 📋 Legal Document Demystifier

<div align="center">

![Legal Document Demystifier](https://img.shields.io/badge/AI-Powered-FF6B6B?style=for-the-badge&logo=robot&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

*Making complex legal documents understandable, actionable, and safe for everyone* 🚀

<br/>

<a href="https://legal-doc-demystifier-oeul.onrender.com"><img src="https://img.shields.io/badge/Live%20Demo-legal--doc--demystifier-oeul.onrender.com-5b8cff?style=for-the-badge" alt="Live Demo"/></a>

<br/>

**🚀 Made by Team Atomic | Lead Developer: Athul S**

</div>

---

## 🎉 **Current Status - Fully Functional!**

✅ **Live Demo Available**: [https://legal-doc-demystifier-oeul.onrender.com](https://legal-doc-demystifier-oeul.onrender.com)  
✅ **Local Development**: Ready to run with `python run.py`  
✅ **Deployment**: Successfully deployed on Render  
✅ **Google Cloud Integration**: Optional AI enhancements available  
✅ **Team Branding**: Professional Team Atomic attribution  

### 🆕 **Recent Updates**
- **Fixed deployment issues** for seamless Render hosting
- **Added Team Atomic branding** throughout the application
- **Enhanced error handling** for robust operation
- **Improved Google Cloud integration** with graceful fallbacks
- **Optimized dependencies** for better performance

---

## ✨ What is Legal Document Demystifier?

Ever felt overwhelmed by dense legal jargon? Our AI-powered web application transforms complex legal documents into clear, actionable insights that anyone can understand! Whether you're reviewing a rental agreement, employment contract, or any legal document, we've got you covered.

### 🎯 Why Choose Us?

- 🔍 **No More Legal Jargon** - Get plain-English explanations
- ⚡ **Lightning Fast** - Process documents in seconds
- 🛡️ **100% Private** - Your documents stay secure with encryption
- 🤖 **AI-Powered** - Advanced machine learning for accurate analysis
- 💬 **Interactive** - Chat with your document like a legal expert

---

## 🌟 Key Features

<table>
<tr>
<td width="50%">

### 📄 **Smart Document Processing**
- Upload PDFs, images, or paste text directly
- Advanced OCR technology for scanned documents
- Support for multiple file formats

### 🧠 **Intelligent Analysis**
- AI-powered summarization in plain language
- Automatic clause segmentation and identification
- Smart risk scoring and highlighting

</td>
<td width="50%">

### 💬 **Interactive Chatbot**
- Ask questions about your document
- Get contextual answers with citations
- RAG-powered responses for accuracy
- **NEW**: AI-powered suggested questions
- **NEW**: Comprehensive document insights

### 🔒 **Privacy & Security**
- End-to-end encryption for all documents
- User-controlled data deletion
- No external API dependencies
- **NEW**: Optional Google Cloud integration
- **NEW**: Graceful fallback to local processing

</td>
</tr>
</table>

---

## 🚀 How It Works

<div align="center">

```mermaid
graph LR
    A[📤 Upload Document] --> B[🔍 OCR & Text Extraction]
    B --> C[✂️ Clause Segmentation]
    C --> D[📝 AI Summarization]
    C --> E[⚠️ Risk Analysis]
    D --> F[💬 Interactive Chat]
    E --> F
    F --> G[📊 Dashboard Results]
```

</div>

### Step-by-Step Process:

1. **📤 Upload** → Drop your PDF, image, or paste text
2. **🔍 Extract** → Advanced OCR extracts all text content
3. **✂️ Segment** → AI identifies and separates legal clauses
4. **📝 Summarize** → Generate easy-to-understand summaries
5. **⚠️ Analyze** → Score and highlight potential risks
6. **💬 Chat** → Ask questions and get instant answers
7. **📊 Export** → Download summaries and chat transcripts

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.9 or higher
- Git
- (Optional) Tesseract OCR for better PDF processing

### Quick Start

<details>
<summary><b>📋 Step-by-Step Installation</b></summary>

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Athul-S-369/Legal-Doc-Demystifier.git
   cd Legal-Doc-Demystifier
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   
   # Linux/Mac
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   # For full functionality with Google Cloud features
   pip install -r requirements.txt
   
   # OR for minimal setup (basic functionality only)
   pip install -r requirements-minimal.txt
   ```

4. **For enhanced OCR (Windows):**
   - Download and install [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki)
   - Download and install [Poppler for Windows](https://blog.alivate.com.au/poppler-windows/)
   - Set environment variables:
     ```bash
     set TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
     set POPPLER_PATH=C:\poppler\bin
     ```

5. **Optional - Google Cloud Setup:**
   - Follow the [Google Cloud Setup Guide](gcp_setup.md) for AI enhancements
   - Set up environment variables for GCP services
   - Enable required APIs in Google Cloud Console

</details>

### 🚀 Running the Application

```bash
python run.py
```



---

## 🎮 How to Use

### Method 1: Upload Documents
1. 📤 **Upload** a PDF, image, or text file
2. ⏳ **Wait** for AI processing (usually 5-10 seconds)
3. 📊 **Review** the summary and risk analysis
4. 💬 **Chat** with your document

### Method 2: Paste Text
1. 📝 **Paste** your contract text directly
2. ⚡ **Get instant** analysis and insights
3. 🔍 **Explore** risks and ask questions

### What You'll Get:
- 📋 **Plain-English Summary** - No more legal jargon!
- ⚠️ **Risk Analysis** - Highlighted potential issues
- 💬 **Interactive Chat** - Ask specific questions
- 🤖 **AI Insights** - Comprehensive document analysis
- ❓ **Suggested Questions** - Smart question recommendations
- 📥 **Export Options** - Download summaries and transcripts
- 🚀 **Team Atomic Branding** - Professional attribution

---

## 🛠️ Technology Stack

<div align="center">

| Category | Technology | Purpose |
|----------|------------|---------|
| 🐍 **Backend** | Flask (Python) | Web framework |
| 🔍 **OCR** | Tesseract, PyPDF2, pdf2image, Google Vision AI | Text extraction |
| 🤖 **AI/ML** | Google Gemini, Vertex AI, Custom TextRank | Advanced AI processing |
| 📝 **Text Processing** | Google Document AI, Custom algorithms | Smart summarization |
| 🔒 **Security** | Google Cloud Storage, Encryption | Document protection |
| ☁️ **Cloud** | Google Cloud Platform | Scalable AI services |
| 🎨 **Frontend** | HTML, CSS, JavaScript | User interface |

</div>

---

## 📁 Project Structure

```
📦 Legal-Doc-Demystifier/
├── 🐍 app/
│   ├── 🔧 services/
│   │   ├── ocr.py              # 📄 Text extraction from PDFs/images
│   │   ├── segment.py          # ✂️ Clause segmentation
│   │   ├── summarize.py        # 📝 TextRank summarization
│   │   ├── risk.py             # ⚠️ Risk analysis heuristics
│   │   ├── embeddings.py       # 🧠 FAISS vector indexing
│   │   ├── rag_chat.py         # 💬 RAG chatbot
│   │   ├── storage.py          # 🔒 Encrypted storage
│   │   ├── gcp_config.py       # ☁️ Google Cloud configuration
│   │   ├── gcp_ocr.py          # 🔍 Enhanced OCR with Vision AI
│   │   ├── gcp_summarize.py    # 🤖 AI summarization with Gemini
│   │   ├── gcp_chat.py         # 💬 Enhanced chatbot with Gemini
│   │   └── gcp_storage.py      # ☁️ Cloud Storage integration
│   ├── 🎨 templates/           # HTML templates
│   ├── 🎨 static/             # CSS/JS assets
│   └── 🛣️ routes.py           # Flask routes
├── 📁 data/                   # Document storage (local fallback)
├── 🤖 models/                # AI model storage
├── 📋 requirements.txt       # Python dependencies
├── 🐳 Dockerfile             # Container configuration
├── ☁️ app.yaml               # Google Cloud App Engine config
└── 📖 gcp_setup.md           # Google Cloud setup guide
```

---

## 🚀 Deployment Options

### 🌐 **Render (Recommended)**
- **One-click deployment** from GitHub
- **Automatic builds** on code changes
- **Free tier available** with generous limits
- **Custom domain support**
- **Environment variables** for configuration

### ☁️ **Google Cloud Platform**
- **App Engine** for serverless deployment
- **Cloud Run** for containerized deployment
- **Full Google Cloud integration** available
- **Enterprise-grade security** and scalability

### 🐳 **Docker Deployment**
- **Containerized application** ready for any platform
- **Consistent environment** across deployments
- **Easy scaling** and management
- **Production-ready** configuration

### 📋 **Deployment Checklist**
- ✅ **Requirements installed** (`pip install -r requirements.txt`)
- ✅ **Environment variables** configured (optional)
- ✅ **Google Cloud APIs** enabled (optional)
- ✅ **Domain configured** (optional)
- ✅ **SSL certificate** (automatic on most platforms)

---

## ☁️ Google Cloud Integration

### 🚀 Enhanced AI Features

Our application now integrates with Google Cloud Platform for advanced AI capabilities:

- **🤖 Gemini AI**: Enhanced chatbot with natural language understanding
- **🔍 Vision AI**: Superior OCR for scanned documents and images
- **📝 Document AI**: Advanced document parsing and structure analysis
- **☁️ Cloud Storage**: Secure, scalable document storage
- **🧠 Vertex AI**: Enterprise-grade AI processing

### 🛠️ Setup Google Cloud Services

1. **Follow the setup guide**: See [gcp_setup.md](gcp_setup.md) for detailed instructions
2. **Configure environment variables**: Set up your Google Cloud credentials
3. **Enable APIs**: Activate required Google Cloud APIs
4. **Deploy**: Use Google Cloud Run or App Engine for production

### 💡 Benefits of Google Cloud Integration

- **🎯 Better Accuracy**: AI-powered text extraction and analysis
- **⚡ Faster Processing**: Cloud-based parallel processing
- **🔒 Enhanced Security**: Enterprise-grade data protection
- **📈 Scalability**: Automatic scaling based on demand
- **💰 Cost-Effective**: Pay only for what you use

### 🔄 Fallback Mode

The application gracefully falls back to local processing when Google Cloud services are not available, ensuring it works in any environment.

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. 🍴 **Fork** the repository
2. 🌿 **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. 💾 **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. 📤 **Push** to the branch (`git push origin feature/amazing-feature`)
5. 🔄 **Open** a Pull Request

### 🐛 Found a Bug?
- Open an issue with the `bug` label
- Provide steps to reproduce
- Include system information

### 💡 Have an Idea?
- Open an issue with the `enhancement` label
- Describe your feature idea
- Explain the use case

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🆘 Support & Contact

<div align="center">

### 💬 Need Help?

[![GitHub Issues](https://img.shields.io/github/issues/Athul-S-369/Legal-Doc-Demystifier?style=for-the-badge&logo=github)](https://github.com/Athul-S-369/Legal-Doc-Demystifier/issues)
[![GitHub Stars](https://img.shields.io/github/stars/Athul-S-369/Legal-Doc-Demystifier?style=for-the-badge&logo=github)](https://github.com/Athul-S-369/Legal-Doc-Demystifier/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/Athul-S-369/Legal-Doc-Demystifier?style=for-the-badge&logo=github)](https://github.com/Athul-S-369/Legal-Doc-Demystifier/network)

**For questions, issues, or feature requests, please open an issue on GitHub.**

---

## 👥 Made with ❤️ by Team Atomic

<div align="center">

### 🚀 **Team Atomic** - Building the Future of Legal Tech

**Lead Developer:** [Athul S](https://github.com/Athul-S-369)

*"Democratizing legal knowledge through AI"*

### 🎯 **Project Highlights**
- ✅ **Fully Functional** - Ready for production use
- ✅ **Live Demo** - Available at [legal-doc-demystifier-oeul.onrender.com](https://legal-doc-demystifier-oeul.onrender.com)
- ✅ **Google Cloud Integration** - Optional AI enhancements
- ✅ **Professional Branding** - Team Atomic attribution throughout
- ✅ **Robust Deployment** - Works on multiple platforms

### 🏆 **Achievements**
- 🥇 **Hackathon Winner** - Legal Document Demystifier
- 🚀 **Production Ready** - Deployed and accessible worldwide
- 🤖 **AI-Powered** - Advanced document analysis capabilities
- 🔒 **Secure** - Privacy-focused design with encryption
- 📱 **Responsive** - Works on all devices and platforms

---

![Footer](https://img.shields.io/badge/Made%20with-❤️-red?style=for-the-badge)
![Footer](https://img.shields.io/badge/Powered%20by-AI-blue?style=for-the-badge)
![Footer](https://img.shields.io/badge/Team-Atomic-orange?style=for-the-badge)
![Footer](https://img.shields.io/badge/Live%20Demo-Available-green?style=for-the-badge)

</div>
