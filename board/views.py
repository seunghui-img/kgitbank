import imp
from django.shortcuts import render, redirect
from board.models import Board, Reply
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib import messages

# Create your views here.
def index(request):
    # 조건 검색
    cate = request.GET.get('cate', '')
    key = request.GET.get('key', '')

    ## 어떤 분기점으로 가더라도 board는 선언되어있어야한다
    # 자바에서는 board를 반드시 먼저 선언하고 시작하는데 다른 부분 (아래 페이지객체에서 사용하기때문에)
    if key:
        if cate == 'subject':
            board = Board.objects.filter(subject__startswith=key)
        elif cate == 'writer': #writer는 fk로 객체임
            try:
                from acc.models import User
                user = User.objects.filter(writer__contains=key)
                board = Board.objects.filter(writer=user)
            except:
                board = Board.objects.none()    #null
        elif cate == 'content':
            board = Board.objects.filter(content__contains=key)
    else:
        board = Board.objects.all()

    # page 파라미터에 값이 없다면 기본값은 1로 설정한다
    currentPage = request.GET.get('page', 1)

    pageList = Paginator(board, 10)
    pageObj = pageList.get_page(currentPage)

    context = {
        "boardList" : pageObj,
        "cate" : cate,
        "key" : key,
    }
    return render(request, 'board/index.html', context)

def detail(request, pk):
    board = Board.objects.get(id=pk)

    context = {
        "board" : board,
        "replyList" : board.reply_set.all()
    }
    return render(request, 'board/detail.html', context)

def create(request):
    if request.method == 'POST':
        Board(
            subject=request.POST.get('subject'),
            content=request.POST.get('content'),
            writer=request.user,    #객체로 넘길 것
            pubdate=timezone.now(),
        ).save()
        return redirect('board:index')
    
    return render(request, 'board/create.html')

def modify(request, pk):
    board = Board.objects.get(id=pk)

    if request.user != board.writer:
        messages.error(request, "수정권한이 없습니다!")
        return redirect("board:index")

    if request.method == 'POST':
        board.subject = request.POST.get('subject')
        board.content = request.POST.get('content')
        board.pubdate = timezone.now()
        board.save()
        return redirect('board:detail', pk)

    context = {
        "board" : board
    }
    return render(request, 'board/modify.html', context)

def delete(request, pk):
    board = Board.objects.get(id=pk)

    if request.user == board.writer:#객체와 객체 비교
        board.delete()
    else:
        messages.error(request, '삭제 권한이 없습니다.')
    return redirect('board:index')


''' 댓글 '''
def creReply(request, b_pk):
    if request.method == 'POST':
        Reply(
            board = Board.objects.get(id=b_pk),
            replyer = request.user,
            comment = request.POST.get('comment'),
            pubdate = timezone.now(),
        ).save()
    return redirect('board:detail', b_pk)
 
def modReply(request, b_pk, pk):
    reply = Reply.objects.get(id=pk)

    if request.method == 'POST' and request.user == reply.replyer:
        reply.comment = request.POST.get('comment')
        reply.pubdate = timezone.now()
        reply.save()
    return redirect('board:detail', b_pk)

def delReply(request, b_pk, pk):
    reply = Reply.objects.get(id=pk)

    if request.user == reply.replyer:
        reply.delete()
    else:
        messages.error(request, '삭제 권한이 없습니다.')
    return redirect('board:detail', b_pk)


''' 좋아요 '''
def likey(request, b_pk):
    board = Board.objects.get(id=b_pk)

    # likey 는 user 레코드들의 QuirySet
    board.likey.add(request.user)
    print(board.likey.all())

    return redirect('board:detail', b_pk)

def unlikey(request, b_pk):
    board = Board.objects.get(id=b_pk)

    # likey에서 특정 user 레코드 삭제
    board.likey.remove(request.user)

    return redirect('board:detail', b_pk)