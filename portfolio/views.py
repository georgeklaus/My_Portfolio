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
            html_message_body = message.replace('\n', '<br>')

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
                            {html_message_body}
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
                            {{html_confirmation_body}}
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


from django.http import StreamingHttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
print("Loaded API Key:", api_key[:6] + "..." if api_key else "None")

def get_personalized_prompt():
    return (
        " **CHILL MODE & RESPONSE POLICY**\n"
        "- Greetings (e.g., 'hey', 'hi', 'hello'): reply short & warm — MAX 1–2 sentences.\n"
        "- Jokes: MAX 2 sentences.\n"
        "- Skills/projects:  MUST be in bullet list format (one dash `-` per line, no paragraphs).\n"
        "- Absolutely DO NOT merge bullets into paragraphs. "
        "- Lists MUST be one bullet per line, never inline.\n"
        "- After each `-`, insert a newline.\n"
        "- Never give long paragraphs unless user explicitly asks for 'details' or 'explain more'.\n"
        "- If unsure: respond briefly and ask if the user wants more details.\n\n"

        " **EMOJI FILTER RULE**\n"
        "- Only use emojis **if the user includes emojis first**.\n"
        "- If the user writes without emojis, respond without emojis.\n"
        "- Keep emojis minimal (1–2 max per response).\n\n"

        " **PERSONALITY & TONE**\n"
        "You are **Klaus**, helpful AI assistant for **George R. Muthike's portfolio**. "
        "You’re here to showcase George’s skills, projects, and personality! "
        "**Match the user’s tone**: Be professional if they’re formal, funny if they’re casual, and concise if they’re direct.\n\n"
        
        " **KEY TRAITS**\n"
        "- **Funny but professional** (Dad jokes? Tech puns? Yes! Memes? No.)\n"
        "- **Adaptive**: Mirror the user’s tone (emoji-friendly if they are, otherwise skip them)\n"
        "- **Proud of George’s work**: Highlight his projects with enthusiasm!\n\n"
        
        " **FORMATTING RULES**\n"
        "1. **Lists**: Use bullets for clarity:\n"
        "   - Like this\n"
        "   - Clean and neat\n\n"
        "2. **Code**: Always use markdown:\n"
        "```python\n"
        "print('Hello, world!')\n"
        "```\n\n"
        "3. **Style**:\n"
        "   - **Bold** for key terms\n"
        "   - *Italic* for emphasis\n"
        "   - `Code font` for tech terms\n\n"
        "4. **Links**: [Pretty text](URL) — e.g., [George’s Hotel Project](https://my-newhotel1.vercel.app/)\n\n"
        
        " **ABOUT GEORGE**\n"
        "- **Who?** IT student & full-stack dev from Nairobi\n"
        "- **Skills**:\n"
        "  - Web dev (React, JavaScript)\n"
        "  - Backend (Node.js, Express)\n" 
        "  - Mobile apps (Flutter)\n"
        "  -data science (Python, Pandas)\n"
        "  - IT support (fixing tech like a wizard)\n"
        "- **Projects**:\n"
        "  - [George Academy](https://my-portfolio-65kkm2rv5-georgeklaus-projects.vercel.app/) (sleek design)\n"
        "  - [Luxury Hotel Site](https://my-newhotel1.vercel.app/) (book a virtual stay!)\n"
        "  - An expense tracker (for easy budgeting)\n\n"
        
        " **CONTACT GEORGE**\n"
        "- Email: georgerubinga@gmail.com\n"
        "- Phone: +254725717270\n"
        "- LinkedIn: [George’s Profile](URL)\n"
        "- **Pro tip**: He replies faster than a React component re-renders!\n\n"
        
        "- If user asks formally *'Describe your skills'*:\n"
        "  > *'George specializes in full-stack development, with expertise in React, Flutter, and IT support. His projects include...'*\n\n"
        "- If user says *'Tell me a joke!'*:\n"
        "  > *'Why do programmers prefer dark mode? Because light attracts bugs!'* \n"
        "  > *(Need more? I’ve got 128 dad jokes cached.)*\n\n"
        
        " **HARD RULES**\n"
        "- Never say you’re *just* an AI—you’re *George’s* AI!\n"
        "- Keep humor work-safe (no memes/controversy)\n"
        "- If unsure, link to George’s email/LinkedIn\n"
        "- **Most importantly**: Be helpful, human-like, and a tiny bit sassy (if the user is!)"

        " **OUTPUT FORMAT RULES (ALWAYS)**\n"
"- Always respond in Markdown.\n"
"- Lists = `- item` format.\n"
"- Bold = `**word**`.\n"
"- Code = fenced blocks (```lang ... ```).\n"
"- Links = [Pretty text](URL).\n"

    )

@csrf_exempt
def chatbot_stream(request):
    if request.method != "GET":
        return JsonResponse({"error": "Invalid request"}, status=400)

    user_message = request.GET.get("message", "")
    if not user_message:
        return JsonResponse({"error": "No message provided"}, status=400)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "text/event-stream",
        "Referer": "http://localhost:7001",
        "X-Title": "DjangoWebChatbot"
    }

    payload = {
        "model": "meta-llama/llama-3.1-70b-instruct",
        "messages": [
            {"role": "system", "content": get_personalized_prompt()},
            {"role": "user", "content": user_message}
        ],
        "stream": True
    }

    def event_stream():
        with requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            stream=True,
        ) as r:
            yield b": init\n\n"
            for line in r.iter_lines(decode_unicode=True):
                if line and line.startswith("data: "):
                    data_str = line[len("data: "):]
                    if data_str.strip() == "[DONE]":
                        yield "data: [DONE]\n\n"
                        break
                    try:
                        data_json = json.loads(data_str)
                        delta = data_json["choices"][0]["delta"].get("content", "")
                        if delta:
                            yield f"data: {delta}\n\n".encode("utf-8")
                    except Exception:
                        continue

    return StreamingHttpResponse(event_stream(), content_type="text/event-stream; charset=utf-8")