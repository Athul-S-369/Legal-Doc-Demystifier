# Google Cloud Platform Setup Guide

This guide will help you set up Google Cloud services to enhance the Legal Document Demystifier with AI capabilities.

## Prerequisites

1. **Google Cloud Account**: Sign up at [Google Cloud Console](https://console.cloud.google.com/)
2. **Google Cloud CLI**: Install the [gcloud CLI](https://cloud.google.com/sdk/docs/install)
3. **Python 3.9+**: Ensure you have Python 3.9 or higher

## Step 1: Create a Google Cloud Project

```bash
# Create a new project
gcloud projects create legal-doc-demystifier --name="Legal Document Demystifier"

# Set the project as default
gcloud config set project legal-doc-demystifier

# Enable billing (required for AI services)
# Go to: https://console.cloud.google.com/billing
```

## Step 2: Enable Required APIs

```bash
# Enable Vertex AI API
gcloud services enable aiplatform.googleapis.com

# Enable Document AI API
gcloud services enable documentai.googleapis.com

# Enable Cloud Vision API
gcloud services enable vision.googleapis.com

# Enable Cloud Storage API
gcloud services enable storage.googleapis.com

# Enable Secret Manager API
gcloud services enable secretmanager.googleapis.com
```

## Step 3: Set Up Authentication

### Option A: Service Account (Recommended for Production)

```bash
# Create a service account
gcloud iam service-accounts create legal-doc-sa \
    --description="Service account for Legal Document Demystifier" \
    --display-name="Legal Doc Service Account"

# Grant necessary permissions
gcloud projects add-iam-policy-binding legal-doc-demystifier \
    --member="serviceAccount:legal-doc-sa@legal-doc-demystifier.iam.gserviceaccount.com" \
    --role="roles/aiplatform.user"

gcloud projects add-iam-policy-binding legal-doc-demystifier \
    --member="serviceAccount:legal-doc-sa@legal-doc-demystifier.iam.gserviceaccount.com" \
    --role="roles/documentai.apiUser"

gcloud projects add-iam-policy-binding legal-doc-demystifier \
    --member="serviceAccount:legal-doc-sa@legal-doc-demystifier.iam.gserviceaccount.com" \
    --role="roles/storage.admin"

# Create and download key
gcloud iam service-accounts keys create ./gcp-key.json \
    --iam-account=legal-doc-sa@legal-doc-demystifier.iam.gserviceaccount.com

# Set environment variable
export GOOGLE_APPLICATION_CREDENTIALS="./gcp-key.json"
```

### Option B: User Authentication (Development)

```bash
# Authenticate with your user account
gcloud auth login

# Set application default credentials
gcloud auth application-default login
```

## Step 4: Set Up Document AI Processor

```bash
# Create a Document AI processor (for enhanced OCR)
gcloud documentai processors create \
    --location=us-central1 \
    --processor-type=OCR_PROCESSOR \
    --display-name="Legal Document OCR"

# Note the processor ID from the output
# Set it as environment variable:
export DOCUMENT_AI_PROCESSOR_ID="your-processor-id"
```

## Step 5: Create Cloud Storage Bucket

```bash
# Create a bucket for document storage
gsutil mb gs://legal-doc-demystifier-documents

# Set environment variable
export GCS_BUCKET_NAME="legal-doc-demystifier-documents"
```

## Step 6: Get Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Set environment variable:

```bash
export GOOGLE_API_KEY="your-gemini-api-key"
```

## Step 7: Environment Variables

Create a `.env` file in your project root:

```bash
# Google Cloud Configuration
GOOGLE_CLOUD_PROJECT=legal-doc-demystifier
GOOGLE_APPLICATION_CREDENTIALS=./gcp-key.json
GOOGLE_API_KEY=your-gemini-api-key
GCS_BUCKET_NAME=legal-doc-demystifier-documents
DOCUMENT_AI_PROCESSOR_ID=your-processor-id

# Optional: Custom location
GOOGLE_CLOUD_LOCATION=us-central1
```

## Step 8: Install Dependencies

```bash
# Install Google Cloud dependencies
pip install -r requirements.txt

# Verify installation
python -c "from app.services.gcp_config import gcp_config; print('GCP Status:', gcp_config.is_gcp_enabled())"
```

## Step 9: Test the Setup

```bash
# Run the application
python run.py

# Check status at: http://localhost:5000/status
```

## Troubleshooting

### Common Issues

1. **Authentication Error**: Ensure `GOOGLE_APPLICATION_CREDENTIALS` points to valid key file
2. **API Not Enabled**: Run `gcloud services enable [API_NAME]` for required APIs
3. **Permission Denied**: Check IAM roles and permissions
4. **Quota Exceeded**: Check your billing account and quotas

### Cost Optimization

- **Free Tier**: Google Cloud offers free tier with limited usage
- **Monitoring**: Set up billing alerts in Google Cloud Console
- **Optimization**: Use local fallbacks when GCP services are not needed

## Security Best Practices

1. **Never commit API keys** to version control
2. **Use service accounts** for production deployments
3. **Rotate keys regularly**
4. **Monitor usage** and set up alerts
5. **Use least privilege** principle for IAM roles

## Deployment Considerations

### For Render/Heroku:
- Set environment variables in deployment platform
- Use service account key as environment variable (base64 encoded)
- Ensure all required APIs are enabled

### For Google Cloud Run:
- Use built-in authentication
- No need for service account keys
- Automatic scaling and billing

## Support

- [Google Cloud Documentation](https://cloud.google.com/docs)
- [Vertex AI Documentation](https://cloud.google.com/vertex-ai/docs)
- [Document AI Documentation](https://cloud.google.com/document-ai/docs)
- [Gemini API Documentation](https://ai.google.dev/docs)
