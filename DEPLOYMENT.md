# Heroku Deployment Guide

This guide will walk you through deploying the Scrabble Word Solver to Heroku.

## Prerequisites

1. **Heroku Account**: Sign up at [heroku.com](https://heroku.com)
2. **Heroku CLI**: Install from [devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)
3. **Git**: Ensure you have Git installed and configured

## Step-by-Step Deployment

### 1. Prepare Your Local Environment

First, make sure your local Flask app is working:

```bash
# Install dependencies
pip install -r requirements.txt

# Test locally (runs on port 5001)
python app.py
```

Visit `http://localhost:5001` to verify the app works.

### 2. Initialize Git Repository (if not already done)

```bash
# Initialize git repository
git init

# Add all files
git add .

# Make initial commit
git commit -m "Initial commit: Scrabble Word Solver Flask app"
```

### 3. Login to Heroku

```bash
# Login to your Heroku account
heroku login
```

This will open your browser for authentication.

### 4. Create Heroku App

```bash
# Create a new Heroku app
heroku create your-scrabble-solver-app-name

# Replace 'your-scrabble-solver-app-name' with your desired app name
# If you don't specify a name, Heroku will generate one for you
```

### 5. Deploy to Heroku

```bash
# Add Heroku remote (if not already added)
git remote add heroku https://git.heroku.com/your-app-name.git

# Push to Heroku
git push heroku main

# If you're on the master branch instead of main:
git push heroku master
```

### 6. Verify Deployment

```bash
# Open your deployed app
heroku open

# Check the logs if there are any issues
heroku logs --tail
```

### 7. Test the Deployed App

1. Open your app in the browser
2. Enter some test letters (e.g., "aetrs")
3. Verify that words are generated correctly
4. Test the copy-to-clipboard functionality

## Troubleshooting

### Common Issues

#### 1. Build Failures

If the build fails, check the logs:
```bash
heroku logs --tail
```

Common causes:
- Missing dependencies in `requirements.txt`
- Python version mismatch in `runtime.txt`
- Syntax errors in the code

#### 2. App Not Starting

If the app doesn't start, check:
```bash
# Check if the app is running
heroku ps

# Restart the app
heroku restart

# Check logs for errors
heroku logs --tail
```

#### 3. Dictionary File Issues

If the dictionary file isn't found:
```bash
# Verify the file is in the repository
git ls-files | grep dictionary.txt

# If not, add it
git add dictionary.txt
git commit -m "Add dictionary file"
git push heroku main
```

#### 4. Port Issues

The app is configured to use Heroku's `PORT` environment variable automatically. If you see port-related errors, make sure your `app.py` doesn't hardcode a port number for production.

### Performance Optimization

#### 1. Enable Dyno Scaling (if needed)

For better performance with multiple users:
```bash
# Scale to 2 dynos (requires paid plan)
heroku ps:scale web=2
```

#### 2. Add Caching (Optional)

Consider adding Redis for caching if you expect high traffic:
```bash
# Add Redis addon (requires paid plan)
heroku addons:create heroku-redis:hobby-dev
```

## Monitoring and Maintenance

### 1. View Logs

```bash
# View recent logs
heroku logs

# Follow logs in real-time
heroku logs --tail
```

### 2. Monitor Performance

```bash
# Check dyno usage
heroku ps

# View app metrics
heroku addons:open scout
```

### 3. Update the App

To deploy updates:
```bash
# Make your changes
# Commit them
git add .
git commit -m "Update description"

# Deploy to Heroku
git push heroku main
```

## Environment Variables

The app doesn't require any environment variables for basic functionality. However, you can add them if needed:

```bash
# Set environment variables
heroku config:set VARIABLE_NAME=value

# View current environment variables
heroku config
```

## Custom Domain (Optional)

To use a custom domain:

```bash
# Add custom domain
heroku domains:add yourdomain.com

# Configure DNS as instructed by Heroku
```

## Cost Considerations

- **Free Tier**: No longer available on Heroku
- **Basic Dyno**: $7/month for basic dyno
- **Standard Dyno**: $25/month for better performance

## Security Considerations

1. **HTTPS**: Heroku automatically provides SSL certificates
2. **Input Validation**: The app validates all user input
3. **Rate Limiting**: Consider adding rate limiting for production use

## Backup and Recovery

### Backup Dictionary

```bash
# Download dictionary file from Heroku
heroku run cat dictionary.txt > dictionary_backup.txt
```

### Database Backup (if using database in future)

```bash
# If you add a database later
heroku pg:backups:capture
heroku pg:backups:download
```

## Support

If you encounter issues:

1. Check the Heroku logs: `heroku logs --tail`
2. Verify your local app works: `python app.py`
3. Check the Heroku documentation: [devcenter.heroku.com](https://devcenter.heroku.com)
4. Review the Flask documentation: [flask.palletsprojects.com](https://flask.palletsprojects.com)

## Next Steps

After successful deployment:

1. **Add Analytics**: Consider adding Google Analytics or similar
2. **Performance Monitoring**: Set up monitoring for response times
3. **Error Tracking**: Add error tracking with services like Sentry
4. **CI/CD**: Set up automatic deployment from GitHub
5. **Testing**: Add automated tests for the web interface 