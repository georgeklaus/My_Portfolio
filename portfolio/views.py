from django.shortcuts import render
from django.core.mail import send_mail
from .forms import ContactForm

# Add the index view for the homepage or portfolio page
def index(request):
    form = ContactForm()
    return render(request, 'portfolio/index.html', {'form': form})

# Home view
def home_view(request):
    return render(request, 'portfolio/home.html')  # Render the home template

# Contact form view
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # Send email to the owner
            send_mail(
                f"Contact Form: {subject}",
                f"Message from {name} ({email}):\n\n{message}",
                'georgerubinga@gmail.com',  # From email
                ['georgerubinga@gmail.com'],  # To email (owner's email)
            )

            # Send confirmation email to the person who filled out the form
            send_mail(
                "Thank you for contacting us",
                f"Dear {name},\n\nThank you for reaching out. We have received your message and will get back to you shortly.\n\nBest regards,\nGeorge",
                'georgerubinga@gmail.com',  # From email
                [email],  # To email (person who filled out the form)
            )

            return render(request, 'portfolio/success.html')
    else:
        form = ContactForm()

    return render(request, 'portfolio/contact.html', {'form': form})
