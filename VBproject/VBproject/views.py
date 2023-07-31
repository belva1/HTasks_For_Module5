from django.http import HttpRequest, HttpResponse, Http404

def main_page_view(request: HttpRequest)-> HttpResponse:
    return HttpResponse('Blog 1, Blog2.')

def descp_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse('The site for first hw with Django.')

def create_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse('FORM.')

def article_view(request: HttpRequest, article: str) -> HttpResponse:
    return HttpResponse(f'Default article - {article}.')

def article_update_view(request: HttpRequest, article: str) -> HttpResponse:
	return HttpResponse(f'Updated article: {article}.') 

def article_delete_view(request: HttpRequest, article: str) -> HttpResponse:
	return HttpResponse(f'Deleted article: {article}.') 

def article_default_comment_view(request: HttpRequest, article: str) -> HttpResponse:
    return HttpResponse(f'Article - "{article}", comment by default.')

def article_comment_create_view(request: HttpRequest, article: str, comment: str) -> HttpResponse:
    return HttpResponse(f'Article - "{article}", new comment - "{comment}"".')

def topics_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse('Topics on the site.')

def topic_subscribe_view(request: HttpRequest, topic: str) -> HttpResponse:
    return HttpResponse(f'Subscribe for {topic}.')

def topic_unsubscribe_view(request: HttpRequest, topic: str) -> HttpResponse:
    return HttpResponse(f'Unsubscribe for {topic}.')

def profile_view(request: HttpRequest, username: str) -> HttpResponse:
    return HttpResponse(f'ProfileName - {username}.')

def set_user_data_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse('Set User Data.')

def set_password_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse('Set Password.')

def register_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse('Register Form.')

def deactivate_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse('Deactivate Form.')

def login_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse('Login.')

def logout_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse('Logout.')

def archive_view(request: HttpRequest, year: str, month: str) -> HttpResponse:
    return HttpResponse(f'Archive: year - {year}, month - {int(month)}.')
