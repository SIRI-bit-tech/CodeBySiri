# CodeBySiri - Professional Web Development Portfolio

A professional portfolio website built with Django, HTMX, and Foundation CSS.

## Features

- Responsive design with Foundation CSS
- Real-time interactions with HTMX
- SEO optimized with meta tags and sitemap
- Cloudinary integration for image storage
- Production-ready email sending

## Local Development

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file based on `.env-example`
6. Run migrations: `python manage.py migrate`
7. Create a superuser: `python manage.py createsuperuser`
8. Run the development server: `python manage.py runserver`

## Deployment on Railway

### Prerequisites

1. Create a [Railway](https://railway.app/) account
2. Create a [Cloudinary](https://cloudinary.com/) account for media storage

### Steps to Deploy via Railway Web Interface

1. Fork this repository to your GitHub account
2. Log in to [Railway](https://railway.app/)
3. Click "New Project" > "Deploy from GitHub repo"
4. Select your forked repository
5. Add a PostgreSQL database service by clicking "New" > "Database" > "Add PostgreSQL"
6. Set up the following environment variables:

   \`\`\`
   SECRET_KEY=your-secure-secret-key
   DEBUG=False
   ALLOWED_HOSTS=your-app-name.up.railway.app
   CSRF_TRUSTED_ORIGINS=https://your-app-name.up.railway.app
   
   # Cloudinary settings
   CLOUDINARY_CLOUD_NAME=your-cloud-name
   CLOUDINARY_API_KEY=your-api-key
   CLOUDINARY_API_SECRET=your-api-secret
   
   # Email settings
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   DEFAULT_FROM_EMAIL=noreply@codebysiri.com
   CONTACT_EMAIL=your-email@gmail.com
   
   # Superuser settings (will be created automatically)
   DJANGO_SUPERUSER_USERNAME=admin
   DJANGO_SUPERUSER_EMAIL=admin@example.com
   DJANGO_SUPERUSER_PASSWORD=your-secure-password
   \`\`\`

7. Click "Deploy" and wait for the deployment to complete
8. Once deployed, you can access your site at the provided Railway URL
9. Log in to the admin panel at `https://your-app-name.up.railway.app/admin/` using the credentials you set in the environment variables

### Custom Domain Setup (Optional)

1. In the Railway dashboard, go to your project settings
2. Click on "Domains"
3. Add your custom domain
4. Update your DNS settings as instructed

## License

This project is licensed under the MIT License - see the LICENSE file for details.
