from django.shortcuts import render, redirect
from django.core.mail import send_mail, EmailMultiAlternatives
from django.contrib import messages
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

            # HTML email with a cleaner, more compact format
            html_message = f"""
            <html>
                <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <div style="padding: 20px; background: #fff; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.07); text-align: left;">
                        <h2 style="color: #333; border-bottom: 1px solid #eee; padding-bottom: 10px; text-align: left !important;">
                            New Contact Form Submission
                        </h2>
                        <table style="width:100%; border-collapse:collapse; text-align: left !important;">
                            <tr>
                                <td style="padding:4px 0; width:90px; text-align: left !important;"><strong>Name:</strong></td>
                                <td style="padding:4px 0; text-align: left !important;">{name}</td>
                            </tr>
                            <tr>
                                <td style="padding:4px 0; text-align: left !important;"><strong>Email:</strong></td>
                                <td style="padding:4px 0; text-align: left !important;">{email}</td>
                            </tr>
                            <tr>
                                <td style="padding:4px 0; text-align: left !important;"><strong>Subject:</strong></td>
                                <td style="padding:4px 0; text-align: left !important;">{subject}</td>
                            </tr>
                        </table>
                        <div style="background: #f8f9fa; padding: 15px; border-radius: 4px; margin-top: 20px; text-align: left !important;">
                            {message.replace('\n', '<br>')}
                        </div>
                        <div style="margin-top: 20px; text-align: left !important;">
                            <p style="text-align: left !important; margin: 10px 0;">Best regards,<br>{name}</p>
                        </div>
                    </div>
                </body>
            </html>
            """

            # Plain text fallback
            text_message = f"Message from {name} ({email}):\n\n{message}"

            # Send email
            msg = EmailMultiAlternatives(
                subject=f"Contact Form: {subject}",
                body=text_message,
                from_email='georgerubinga@gmail.com',
                to=['georgerubinga@gmail.com'],
                reply_to=[email]
            )
            msg.attach_alternative(html_message, "text/html")
            msg.send()

            # Send confirmation (improved auto-responder)
            confirmation_subject = "Thank you for contacting us"
            confirmation_html = f"""
            <html>
                <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <div style="padding: 20px; background: #fff; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.07);">
                        <h2 style="color: #333;">Thank you, {name}!</h2>
                        <p>We have received your message and will respond as soon as possible.</p>
                        <h4 style="margin-top: 20px;">Your Submission:</h4>
                        <ul>
                            <li><strong>Name:</strong> {name}</li>
                            <li><strong>Email:</strong> {email}</li>
                            <li><strong>Subject:</strong> {subject}</li>
                        </ul>
                        <div style="background: #f8f9fa; padding: 15px; border-radius: 4px; margin-top: 10px;">
                            {message.replace('\n', '<br>')}
                        </div>
                        <p style="margin-top: 20px;">In the meantime, feel free to visit my <a href="https://my-portfolio-blush-delta-44.vercel.app/"
   style="display:inline-block; margin-top:20px; background:#1976d2; color:#fff; padding:10px 20px; border-radius:4px; text-decoration:none;">
   website
</a> or reply to this email if you have more information to add.</p>
                        <p style="margin-top: 20px;">Best regards,<br>George</p>
                    </div>
                </body>
            </html>
            """
            confirmation_text = (
                f"Dear {name},\n\n"
                "Thank you for your message. We'll respond soon.\n\n"
                "Your submission:\n"
                f"Name: {name}\nEmail: {email}\nSubject: {subject}\n\n"
                f"{message}\n\n"
                "Best regards,\nGeorge"
            )

            confirmation_msg = EmailMultiAlternatives(
                subject=confirmation_subject,
                body=confirmation_text,
                from_email='georgerubinga@gmail.com',
                to=[email]
            )
            confirmation_msg.attach_alternative(confirmation_html, "text/html")
            confirmation_msg.send()

            messages.success(request, "Your message was sent successfully! Thank you for reaching out.")
            return redirect('contact')
        else:
            messages.error(request, "There was an error sending your message. Please check the form and try again.")
    else:
        form = ContactForm()

    return render(request, 'portfolio/contact.html', {'form': form})

def chat_view(request):
    return render(request, 'portfolio/chat.html')


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

@csrf_exempt
def chatbot_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message")

        headers = {
            "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://openrouter.ai",
            "X-Title": "DjangoWebChatbot"
        }

        payload = {
            "model": "openai/gpt-3.5-turbo",  # You can change this to GPT-4 or Claude
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        }

        try:
            response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
            result = response.json()
            reply = result["choices"][0]["message"]["content"]
            return JsonResponse({"reply": reply})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)
