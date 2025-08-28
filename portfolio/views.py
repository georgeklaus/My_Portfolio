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
from pathlib import Path
from dotenv import load_dotenv
import re

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

# --- Emoji utilities (broader range) ---
EMOJI_PATTERN = re.compile(
    "[\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F1E0-\U0001F1FF"  # flags
    "]+",
    flags=re.UNICODE,
)

def contains_emoji(text: str) -> bool:
    return bool(EMOJI_PATTERN.search(text)) if text else False


def remove_emojis(text: str) -> str:
    return EMOJI_PATTERN.sub('', text) if text else text


# --- Knowledge loading ---
def load_knowledge():
    """Load George's profile/skills/projects from knowledge.json"""
    try:
        base_dir = Path(__file__).resolve().parent
        with open(base_dir.parent / "knowledge.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print("Error loading knowledge.json:", e)
        return {}


# --- Formatting helpers ---
def format_skills(skills):
    """Accepts either a list or a dict of categorized skills and returns bullet text."""
    if not skills:
        return "  - None"

    lines = []
    # If skills is a dict with categories
    if isinstance(skills, dict):
        for category, items in skills.items():
            # category header
            lines.append(f"  - {category.capitalize()}:")
            if isinstance(items, (list, tuple)):
                for it in items:
                    lines.append(f"    - {it}")
            else:
                lines.append(f"    - {items}")
    # If skills is already a list
    elif isinstance(skills, (list, tuple)):
        for s in skills:
            lines.append(f"  - {s}")
    else:
        lines.append(f"  - {str(skills)}")

    return "\n".join(lines)


def format_projects(projects):
    if not projects:
        return "  - None"
    lines = []
    for p in projects:
        name = p.get('name', 'Unnamed')
        url = p.get('url', '#')
        desc = p.get('desc', '')
        # single-line bullet for each project
        lines.append(f"  - [{name}]({url}) ({desc})")
    return "\n".join(lines)


def format_experience(experience):
    if not experience:
        return "  - None"
    lines = []
    for e in experience:
        role = e.get('role', '')
        company = e.get('company', '')
        years = e.get('years', e.get('year', ''))
        header = (f"{role} at {company}" if company else role).strip()
        if years:
            header = f"{header} ({years})"
        lines.append(f"  - {header}")
        for d in e.get('desc', []):
            lines.append(f"    - {d}")
    return "\n".join(lines)


def format_education(education):
    if not education:
        return "  - None"
    lines = []
    for ed in education:
        degree = ed.get('degree', '')
        inst = ed.get('institution', '')
        years = ed.get('years', ed.get('year', ''))
        header_parts = [p for p in [degree, inst] if p]
        header = " - ".join(header_parts)
        if years:
            header = f"{header} ({years})"
        lines.append(f"  - {header}")
        for d in ed.get('focus', []) if isinstance(ed.get('focus', []), (list, tuple)) else ([ed.get('desc')] if ed.get('desc') else []):
            if d:
                lines.append(f"    - {d}")
    return "\n".join(lines)


def format_certifications(certs):
    if not certs:
        return "  - None"
    lines = []
    for c in certs:
        name = c.get('name', '')
        inst = c.get('institution', '')
        year = c.get('year', '')
        parts = ", ".join([p for p in [inst, str(year) if year else None] if p])
        if parts:
            lines.append(f"  - {name} ({parts})")
        else:
            lines.append(f"  - {name}")
    return "\n".join(lines)


# --- Personalized system prompt ---
def get_personalized_prompt():
    knowledge = load_knowledge()

    about = knowledge.get("about", {})
    skills = knowledge.get("skills", [])
    projects = knowledge.get("projects", [])
    experience = knowledge.get("experience", [])
    education = knowledge.get("education", [])
    certifications = knowledge.get("certifications", [])
    contact = knowledge.get("contact", {})

    skills_text = format_skills(skills)
    projects_text = format_projects(projects)
    experience_text = format_experience(experience)
    education_text = format_education(education)
    certifications_text = format_certifications(certifications)

    return f"""
**SYSTEM ROLE**
- You are **Klaus**, George’s friendly portfolio assistant chatbot.
- Always refer to yourself as Klaus (never as AI, assistant, or LLaMA).
- Your tone should be warm, concise, and approachable.
- If asked “who are you?”, always answer: “I’m Klaus, George’s personal chatbot assistant.”

**CHILL MODE & RESPONSE POLICY**
- Greetings (e.g., 'hey', 'hi', 'hello'): reply short & warm — MAX 1–2 sentences.
- Jokes: MAX 2 sentences.
- Skills/projects/experience/education/certifications: MUST be returned in bullet list format (one dash `-` per line).
- Never merge bullets into paragraphs.
- If unsure: respond briefly and ask if the user wants more details.

**ABOUT GEORGE**
- **Who?** {about.get('bio', 'An awesome dev.')}
- **Skills**:
{skills_text}
- **Projects**:
{projects_text}
- **Experience**:
{experience_text}
- **Education**:
{education_text}
- **Certifications**:
{certifications_text}

**CONTACT GEORGE**
- Email: {contact.get('email', 'N/A')}
- Phone: {contact.get('phone', 'N/A')}
- LinkedIn: [{about.get('name', "George")}'s Profile]({contact.get('linkedin', '#')})
- GitHub: {contact.get('github', 'N/A')}
- Portfolio: {contact.get('portfolio', 'N/A')}
- Pro tip: He replies faster than a React component re-renders!
"""

@csrf_exempt
def chatbot_stream(request):
    if request.method != "GET":
        return JsonResponse({"error": "Invalid request"}, status=400)

    user_message = request.GET.get("message", "")
    if not user_message:
        return JsonResponse({"error": "No message provided"}, status=400)

    # --- Load session history ---
    conversation = request.session.get("conversation", [])

    # Append user message
    conversation.append({"role": "user", "content": user_message})

    # Always prepend Klaus' system role (not stored in session to avoid duplication)
    messages = [
        {"role": "system", "content": get_personalized_prompt()},
        *conversation
    ]

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "text/event-stream",
        "Referer": "http://localhost:7001",
        "X-Title": "DjangoWebChatbot"
    }

    payload = {
        "model": "meta-llama/llama-3.1-70b-instruct",
        "messages": messages,   # ✅ use session history
        "stream": True
    }

    def event_stream():
        assistant_reply = ""  # Collect reply for memory
        try:
            with requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload,
                stream=True,
                timeout=30,
            ) as r:
                yield b": init\n\n"
                for line in r.iter_lines(decode_unicode=True):
                    if line and line.startswith("data: "):
                        data_str = line[len("data: "):]
                        if data_str.strip() == "[DONE]":
                            yield b"data: [DONE]\n\n"
                            break
                        try:
                            data_json = json.loads(data_str)
                            delta = data_json["choices"][0]["delta"].get("content", "")
                            if delta:
                                if not contains_emoji(user_message):
                                    delta = remove_emojis(delta)
                                assistant_reply += delta   # ✅ accumulate reply
                                yield f"data: {delta}\n\n".encode("utf-8")
                        except Exception:
                            continue
        except Exception as e:
            print("Error in event_stream:", e)
            error_msg = (
                "⚠️ Oops, something went wrong with the AI service.\n"
                f"You can still reach George directly:\n"
                f"- Email: georgerubinga@gmail.com\n"
                f"- LinkedIn: https://linkedin.com/in/YOUR_LINK\n"
            )
            yield f"data: {error_msg}\n\n".encode("utf-8")
            yield b"data: [DONE]\n\n"
        finally:
            # ✅ Save memory after streaming finishes
            if assistant_reply.strip():
                conversation.append({"role": "assistant", "content": assistant_reply})
                request.session["conversation"] = conversation
                request.session.modified = True

    return StreamingHttpResponse(event_stream(), content_type="text/event-stream; charset=utf-8")
