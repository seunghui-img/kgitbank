from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from .models import User
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'acc/index.html')

def login_user(request):
    if request.method == 'POST':
        iUsername = request.POST.get('username')
        iPassword = request.POST.get('password')

        user = authenticate(username=iUsername, password=iPassword)
        print(user)
        
        if user:
            login(request, user)
            messages.success(request, f"{user.username}님 환영합니다.")
            return redirect('acc:index')
        else:
            messages.error(request, '계정정보가 일치하지 않습니다.')
        
    return render(request, 'acc/login.html')

def logout_user(request):
    logout(request)
    return redirect('acc:index')

def join(request):
    if request.method == 'POST':
        iUsername = request.POST.get('username')
        iPassword = request.POST.get('password')
        iAge = request.POST.get('age')
        iComment = request.POST.get('comment')
        iPic = request.FILES.get('pic')

        print(iUsername, iPassword, iAge, iComment, iPic)

        # if User.objects.get(username=iUsername):
        #     print('사용 중인 아이디입니다')
        #     context={
        #         'success' : 'false',
        #         'username' : iUsername
        #     }
        #     return redirect('acc:joinus')

        try:
            User.objects.create_user(
                username=iUsername,
                password=iPassword,
                age=iAge,
                comment=iComment,
                pic=iPic,
            )
            return redirect('acc:login')
        except:
            messages.error(request, "이미 사용중인 USERNAME 입니다.")
    return render(request, 'acc/join.html')

def profile(request):
    return render(request, 'acc/profile.html')

def update(request):
    if request.method == 'POST':
        iPassword = request.POST.get('password')
        iComment = request.POST.get('comment')
        iPic = request.FILES.get('pic')

        print(iPassword, iComment, iPic)

        user = request.user

        if iPassword:
            user.set_password(iPassword)    # 패스워드 암호화
        user.comment = iComment
        if iPic:
            user.pic.delete()   # 기존 사진 삭제
            user.pic = iPic
        user.save()

        login(request, user)
        return redirect('acc:profile')

    return render(request, 'acc/update.html')

def delete(request):
    request.user.delete()
    return redirect('acc:index')