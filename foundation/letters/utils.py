def can_send(user, case):
    return user.is_superuser or user == case.created_by


def nl2br(text):
    return text.replace("\n", "\n<br>")
