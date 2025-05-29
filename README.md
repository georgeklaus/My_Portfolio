# George Rubinga's Portfolio | Full-Stack Developer  

**Live Demo**: https://my-portfolio-blush-delta-44.vercel.app/
**GitHub**: https://github.com/georgeklaus/My_Portfolio 

##  Tech Stack  
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap  
- **Backend**: Django (Python)  
- **Deployment**: Vercel  
- **Other Tools**: Git 

##  Key Features  
1. **Functional Contact Form**  
   - Django backend handles form submissions ( uses Django's `send_mail` or SMTP).  
   - Validation: Client-side (JS) + server-side (Django forms).  
2. **Responsive Design**  
   - Mobile-first CSS with Bootstrap overrides.  
   - Custom animations  
3. **Deployment**  
   - Configured for Vercel, static file handling in Django  

##  Project Structure  
``
portfolio/  
├── core/                  # Django backend  
│   ├── views.py           # Contact form logic  
│   ├── forms.py           # Form validation  
│   └── models.py          # Database models (if any)  
├── static/                # Custom assets  
│   ├── css/               # Bootstrap overrides  
│   └── js/                # Interactive elements  
├── templates/             # HTML files  
├── vercel.json            # Deployment config  
└── requirements.txt       # Python dependencies

**Why This Code?**
Demonstrates Full-Stack Skills: Combines frontend (JS/CSS) + backend (Django).

Real-World Problem: Solves user engagement (contact form) and deployment.

MLH-Aligned: Uses Python (Django) + JavaScript — preferred languages.

**Challenges & Solutions**
Challenge: Django static files on Vercel.
Solution: Used whitenoise + Vercel config.

**Challenge: Cross-browser JS compatibility.**
Solution: Polyfills/Babel.

**For MLH Reviewers**
Focus Areas:

Django backend (core/views.py for form handling).

Custom JS (static/js/) for interactivity.
