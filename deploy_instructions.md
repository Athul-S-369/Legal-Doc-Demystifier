# 🚀 Deployment Instructions

## Option 1: Heroku (Recommended)

### Prerequisites:
1. Install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
2. Create a [Heroku account](https://heroku.com) (free)

### Steps:

1. **Login to Heroku:**
   ```bash
   heroku login
   ```

2. **Create Heroku app:**
   ```bash
   heroku create legal-doc-demystifier
   ```

3. **Set environment variables:**
   ```bash
   heroku config:set FLASK_APP=run.py
   heroku config:set FLASK_ENV=production
   ```

4. **Deploy:**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

5. **Open your app:**
   ```bash
   heroku open
   ```

## Option 2: Railway

1. Go to [Railway.app](https://railway.app)
2. Connect your GitHub repository
3. Deploy automatically!

## Option 3: Render

1. Go to [Render.com](https://render.com)
2. Connect GitHub repository
3. Select "Web Service"
4. Use these settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python run.py`

## Option 4: PythonAnywhere

1. Go to [PythonAnywhere.com](https://pythonanywhere.com)
2. Create free account
3. Upload your code via Git
4. Configure web app

## 🔧 Important Notes:

- **OCR Setup**: For production, you may need to install Tesseract on the server
- **File Storage**: Consider using cloud storage (AWS S3, etc.) for production
- **Database**: Add a proper database for production use
- **Environment Variables**: Store sensitive data in environment variables

## 📊 Monitoring:

- Check logs: `heroku logs --tail`
- Monitor performance in Heroku dashboard
- Set up error tracking (Sentry, etc.)

## 🎯 Your App Will Be Live At:
- Heroku: `https://legal-doc-demystifier.herokuapp.com`
- Railway: `https://your-app-name.railway.app`
- Render: `https://your-app-name.onrender.com`
