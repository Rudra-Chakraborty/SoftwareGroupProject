from django.contrib.auth import login
from django.contrib.auth.models import User as DjangoUser


class GroupSessionToDjangoAuthMiddleware:
    """
    Bridges the uploaded group-project login session with Django auth.

    The uploaded login stores:
        request.session["user_email"]

    Student 1 pages can then use Django authentication safely.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        session_email = request.session.get("user_email")
        session_user_id = request.session.get("user_id")

        if (session_email or session_user_id) and not request.user.is_authenticated:
            try:
                email = session_email

                if not email and session_user_id:
                    try:
                        from main.models import User as GroupUser
                        group_user = GroupUser.objects.filter(user_Id=session_user_id).first()
                        if group_user:
                            email = group_user.email
                    except Exception:
                        email = None

                username = email or f"group_user_{session_user_id}"
                user, _ = DjangoUser.objects.get_or_create(
                    username=username,
                    defaults={"email": email or ""}
                )
                login(request, user)
            except Exception:
                pass

        return self.get_response(request)
