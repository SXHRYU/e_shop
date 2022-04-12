from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout


# This view here has all the logic inside of an html (filling out the form and
# checking if the user.is_authenticated and checking the correct credentials).
# This is a wrong way to do it, I know. It would be correct to make a Django
# form that has all the logic and display error messages (maybe via a 
# 'messages' default application. 
# The reason I've done authentication this way is purely experimental and
# educational purposes. I needed to understand different approaches in
# forms, authentication and logic. I'll leave the authentication system as-is
# and will redo it in future projects.
def auth_login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profiles-detail', pk=user.id)
        else:
            wrong_credentials = True
            return render(request, 'authentication/auth.html', {
                'wrong_credentials': wrong_credentials
            })
    else:
        return render(request, 'authentication/auth.html', {})

def auth_logout_view(request):
    logout(request)
    print('logged out successfully')
    return redirect('/login/')
