from django.shortcuts import render,redirect
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib import messages
import json
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
    return render(request,"index.html")
def succes(request):
    name = request.POST.get('name') 
    return render(request,"succes.html")
from django.core.mail import send_mail, BadHeaderError

from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from django.contrib import messages
from django.shortcuts import render, redirect

def contact_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        try:
            # Send email to admin
            send_mail(
                f"New Contact from {name}",
                f"Name: {name}\nEmail: {email}\nMessage:\n{message}",
                "vamshikrishnakannaji@gmail.com",
                ["vamshikrishnakannaji@gmail.com"],  # admin email
            )

            # Render HTML confirmation template for user
            html_content = render_to_string("email_templates/contact_response.html", {
                "name": name,
                "user_message": message,
            })

            # Send confirmation email to user
            email_message = EmailMessage(
                "Thanks for contacting me!",
                html_content,
                "vamshikrishnakannaji@gmail.com",
                [email],
            )
            email_message.content_subtype = "html"
            email_message.send()

            messages.success(request, "Your message was sent!")

        except Exception as e:
            print("EMAIL ERROR:", e)
            messages.error(request, "Something went wrong. Try again.")

        return redirect("index")

    return render(request, "index.html")



@csrf_exempt
def track_visit(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            time_spent = data.get('time_spent', 0)
            page_url = data.get('page_url', 'Unknown')

            send_mail(
                subject='New Portfolio Visit Alert',
                message=f"Someone visited your portfolio!\nPage: {page_url}\nTime Spent: {time_spent} seconds",
                from_email='vamshikrishnakannaji@gmail.com',
                recipient_list=['vamshikrishnakannaji@gmail.com'],
                fail_silently=False,
            )

            return HttpResponse("Tracked", status=200)
        except Exception as e:
            print("Tracking Error:", e)
            return HttpResponse("Error", status=500)

    return HttpResponse("Invalid request", status=400)