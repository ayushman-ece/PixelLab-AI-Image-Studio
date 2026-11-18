# ✦ PixelLab – AI Image Processing Studio

### Create. Enhance. Transform.

PixelLab is a professional AI-powered image processing and editing studio built using Python and Streamlit. It combines traditional image processing techniques with modern AI capabilities to help users enhance, analyze, and transform images through an intuitive web interface.

## 🚀 Live Demo

**Live Application:** Add your Streamlit deployment URL here.

## 📸 About the Project

PixelLab provides a creative workspace where users can upload images, apply image processing operations, download edited results, and access AI-powered image assistance.

The application combines Pillow for traditional image processing, Google Gemini for AI image editing and image analysis, and Groq for an interactive AI assistant.

## ✨ Features

### 🎨 Image Processing
- Grayscale conversion
- Black and white conversion
- Brightness adjustment
- Contrast adjustment
- Saturation adjustment
- Blur and sharpen effects
- Edge detection
- Vintage and sepia effects
- Image rotation
- Horizontal and vertical flipping

### ✦ AI Image Editor
- Edit images using natural-language prompts.
- Generate AI-modified images.
- Try predefined editing suggestions.
- Preview and download AI-generated results.

### ◈ Image Intelligence
- Image description and understanding.
- Lighting and image-quality analysis.
- Object and background identification.
- Color and composition analysis.
- Professional editing recommendations.

### ⚡ AI Assistant
- Interactive AI-powered assistant.
- Photography and editing suggestions.
- Image enhancement recommendations.
- Natural-language editing guidance.

### 📥 Image Export
- Download processed images.
- PNG export.
- JPEG export.
- Original and edited image previews.

### 🔐 Security
- API keys are stored in environment variables.
- Streamlit Secrets support for deployment.
- No API keys are displayed in the public interface.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Web application interface |
| Pillow (PIL) | Image processing |
| Google Gemini API | AI image editing and analysis |
| Groq API | AI assistant |
| python-dotenv | Environment variable management |
| GitHub | Source code management |
| Streamlit Community Cloud | Application hosting |

## 📂 Project Structure

```text
PixelLab/
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/PixelLab-AI-Image-Studio.git
```

### 2. Navigate to the project

```bash
cd PixelLab-AI-Image-Studio
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API keys

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
GROQ_API_KEY=your_groq_api_key
```

Get your API keys:

- Gemini: https://aistudio.google.com/apikey
- Groq: https://console.groq.com/keys

Never upload your `.env` file to GitHub.

### 5. Run the application

```bash
streamlit run app.py
```

Open the local application at:

```text
http://localhost:8501
```

## ☁️ Deployment

PixelLab can be deployed using Streamlit Community Cloud.

1. Push the project to a GitHub repository.
2. Sign in to Streamlit Community Cloud.
3. Connect your GitHub account.
4. Select the PixelLab repository.
5. Select `app.py` as the main application file.
6. Configure your API keys using Streamlit Secrets.
7. Deploy the application.

### Streamlit Secrets Configuration

```toml
GEMINI_API_KEY = "your_gemini_api_key"
GROQ_API_KEY = "your_groq_api_key"
```

## 🔑 API Usage

PixelLab uses external AI services for selected features:

- Google Gemini: Image editing and image understanding.
- Groq: Conversational AI assistance.

AI functionality depends on API availability, model access, usage limits, and applicable provider terms. Traditional image processing works independently of these AI services.

## ⚠️ Important Notes

- An internet connection is required for AI features.
- AI image generation may be subject to API quotas and billing.
- Uploaded images are processed locally for traditional editing. Images are sent to the relevant AI provider when an AI feature is used.
- Do not enter confidential images unless you are comfortable with the relevant provider's data-handling policies.

## 🎯 Project Objective

The objective of PixelLab is to combine traditional image processing and modern artificial intelligence into one accessible creative workspace.

It demonstrates the practical application of Python programming, image processing, API integration, AI-powered applications, and web development.

## 👨‍💻 Developer

**Developed as a Python Programming for Electronics Engineering mini project.**

GitHub: https://github.com/YOUR_USERNAME

---

### ✦ PixelLab

**Create. Enhance. Transform.**