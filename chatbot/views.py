import json
import traceback

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages

from .models import FAQ, Navigation, AttachmentOpportunity, ChatLog
from google import genai

# Gemini client
client = genai.Client(api_key=settings.GEMINI_API_KEY)

# -----------------------------
# FORGOT PASSWORD
# -----------------------------


def forgot_password(request):
    return render(request, "chatbot/forgot_password.html")

# -----------------------------
# CHANGE PASSWORD
# -----------------------------


@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password changed successfully")
            return redirect("chat_page")
    else:
        form = PasswordChangeForm(request.user)

    return render(request, "chatbot/change_password.html", {"form": form})

# -----------------------------
# LOGIN
# -----------------------------


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("chat_page")

        return render(request, "chatbot/login.html", {
            "error": "Invalid username or password"
        })

    return render(request, "chatbot/login.html")

# -----------------------------
# LOGOUT
# -----------------------------


def logout_view(request):
    logout(request)
    return redirect("login")

# -----------------------------
# CHAT PAGE (LOGIN REQUIRED)
# -----------------------------


@login_required
def chat_page(request):
    return render(request, "chatbot/index.html")

# -----------------------------
# CHAT API
# -----------------------------


@csrf_exempt
@login_required
def chat_api(request):
    if request.method != "POST":
        return JsonResponse({"reply": "Invalid request.", "image": None})

    try:
        data = json.loads(request.body)
        message = data.get("message", "").strip()

        if not message:
            return JsonResponse({"reply": "Please type something.", "image": None})

        message_lower = message.lower()

        # FAQ SEARCH

        for faq in FAQ.objects.all():
            keywords = (faq.keywords or "").lower().split(",")
            if any(k.strip() in message_lower for k in keywords):
                ChatLog.objects.create(
                    user=request.user, message=message, response_type="faq")
                return JsonResponse({"reply": faq.answer, "image": None})

        # NAVIGATION SEARCH (BEST MATCH)

        best_match = None
        best_score = 0

        for nav in Navigation.objects.all():
            score = 0
            place_name = nav.place.lower()
            keywords = (nav.keywords or "").lower().split(",")

            # check place name
            if place_name in message_lower:
                score += 5

            # check keywords
            for k in keywords:
                k = k.strip()
                if k and k in message_lower:
                    score += 1

            # keep the best scoring match
            if score > best_score:
                best_score = score
                best_match = nav

        if best_match:
            image_url = None
            ChatLog.objects.create(
                user=request.user, message=message, response_type="navigation")
            return JsonResponse({"reply": best_match.description, "image": image_url})

        # ATTACHMENT SEARCH

        degrees = AttachmentOpportunity.objects.values_list(
            "degree_programme", flat=True).distinct()
        matched_degree = None

        for degree in degrees:
            if degree.lower() in message_lower:
                matched_degree = degree
                break

        if matched_degree:
            attachments = AttachmentOpportunity.objects.filter(
                degree_programme__iexact=matched_degree)
            if attachments.exists():
                table = """
                <div style="overflow-x:auto; max-height:300px; overflow-y:auto;">
                <table style="width:100%; border-collapse: collapse; background:white; color:black;">
                <tr style="background:#1a5f4a;color:white;">
                <th style="padding:8px;">Company</th>
                <th style="padding:8px;">Location</th>
                <th style="padding:8px;">Contact</th>
                </tr>
                """
                for a in attachments:
                    table += f"""
                    <tr>
                    <td style="padding:6px;">{a.company_name}</td>
                    <td style="padding:6px;">{a.location}</td>
                    <td style="padding:6px;">{a.contact}</td>
                    </tr>
                    """
                table += "</table></div>"

                ChatLog.objects.create(
                    user=request.user, message=message, response_type="attachment")
                return JsonResponse({"reply": table, "image": None})

        # DEGREE SUGGESTION

        if "attachment" in message_lower or "degree" in message_lower:
            if degrees:
                html = "<b>No results found.</b><br><br>Available degrees:<ul>"
                for d in degrees:
                    html += f"<li>{d}</li>"
                html += "</ul>"
                return JsonResponse({"reply": html, "image": None})

        # GEMINI AI FALLBACK

        try:
            response = client.models.generate_content(
                model="gemini-flash-latest",
                contents=f"You are a helpful university assistant.\nUser: {message}"
            )
            ai_reply = response.text
        except Exception as e:
            print("GEMINI ERROR:", e)
            ai_reply = "AI service unavailable."

        ChatLog.objects.create(
            user=request.user, message=message, response_type="ai")
        return JsonResponse({"reply": ai_reply, "image": None})

    except Exception as e:
        print("CHAT API ERROR:", e)
        traceback.print_exc()
        return JsonResponse({"reply": "Server error occurred.", "image": None})
