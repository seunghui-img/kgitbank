from django.shortcuts import render
import googletrans
from googletrans import Translator

# Create your views here.
def index(request):
    context = {
        "language": googletrans.LANGUAGES,
    }

    if request.method == 'POST':
        before = request.POST.get('before', '')
        fromLang = request.POST.get('from', '')
        toLang = request.POST.get('to', '')

        translator = Translator()

        # detect: 문자열의 언어가 뭔지 확인
        # print(translator.detect(before))
        
        trans_str = translator.translate(before, src=fromLang, dest=toLang)

        # 딕셔너리에 튜플 추가
        context['before'] = before
        context['after'] = trans_str.text

        # 딕셔너리에 한번에 튜플 추가
        context.update({
            "from": fromLang,
            "to": toLang,
        })

    return render(request, 'trans/index.html', context)