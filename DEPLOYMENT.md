# 🚀 Free Deployment Guide

This guide will help you deploy your Numbers game for free using various platforms.

## Option 1: Vercel + Railway (Recommended)

### Frontend Deployment (Vercel)

1. **Install Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

2. **Deploy Frontend**:
   ```bash
   cd Numbers
   vercel
   ```

3. **Configure Environment**:
   - Set `VITE_API_URL` to your Railway backend URL
   - Example: `https://your-app.railway.app`

### Backend Deployment (Railway)

1. **Create Railway Account**:
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Deploy Backend**:
   ```bash
   # Install Railway CLI
   npm i -g @railway/cli

   # Login and deploy
   railway login
   railway init
   railway up
   ```

3. **Set Environment Variables**:
   - `SECRET_KEY`: Your secret key
   - `DATABASE_URL`: Railway will provide PostgreSQL URL

## Option 2: Netlify + Render

### Frontend (Netlify)

1. **Connect GitHub Repository**:
   - Go to [netlify.com](https://netlify.com)
   - Connect your GitHub repo

2. **Build Settings**:
   - Build command: `cd frontend && npm install && npm run build`
   - Publish directory: `frontend/dist`

### Backend (Render)

1. **Create Render Account**:
   - Go to [render.com](https://render.com)
   - Sign up with GitHub

2. **Deploy Web Service**:
   - Connect your repository
   - Build command: `pip install -r backend/requirements.txt`
   - Start command: `uvicorn backend.api.app:app --host 0.0.0.0 --port $PORT`

## Option 3: Fly.io (All-in-one)

1. **Install Fly CLI**:
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Deploy**:
   ```bash
   fly auth login
   fly launch
   fly deploy
   ```

## Option 4: Railway (All-in-one)

1. **Create Railway Project**:
   - Go to [railway.app](https://railway.app)
   - Create new project

2. **Add Services**:
   - Add backend service (Python)
   - Add frontend service (Node.js)

3. **Configure**:
   - Set environment variables
   - Configure build commands

## Environment Variables

Create a `.env` file with:

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=your-database-url
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Database Options

### Free Database Providers:
- **Railway PostgreSQL**: Free tier included
- **Supabase**: Free tier with PostgreSQL
- **PlanetScale**: Free MySQL database
- **Neon**: Free PostgreSQL

### Keep SQLite (Simplest):
- Works for small projects
- No additional setup required
- Data persists in Railway/Render storage

## Cost Breakdown

| Platform | Frontend | Backend | Database | Total Cost |
|----------|----------|---------|----------|------------|
| Vercel + Railway | Free | Free | Free | $0/month |
| Netlify + Render | Free | Free | Free | $0/month |
| Fly.io | Free | Free | Free | $0/month |
| Railway (All) | Free | Free | Free | $0/month |

## Troubleshooting

### Common Issues:
1. **CORS Errors**: Update backend CORS settings
2. **Build Failures**: Check Node.js/Python versions
3. **Database Connection**: Verify DATABASE_URL format

### Support:
- Check platform documentation
- Use platform-specific logs
- Join platform Discord communities

## Next Steps

1. Choose your preferred platform
2. Follow the deployment steps
3. Update your README with live URLs
4. Share your deployed game! 🎮 