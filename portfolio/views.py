from django.shortcuts import render
from django.core.mail import send_mail
from .forms import ContactForm

# Add the index view for the homepage or portfolio page
def index(request):
    form = ContactForm()
    return render(request, 'portfolio/index.html', {'form': form})

# Contact form view
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # Send email
            send_mail(
                f"Contact Form: {subject}",
                f"Message from {name} ({email}):\n\n{message}",
                'your-email@example.com',  # From email
                ['recipient-email@example.com'],  # To email
            )
            return render(request, 'portfolio/success.html')
    else:
        form = ContactForm()

    return render(request, 'portfolio/contact.html', {'form': form})
