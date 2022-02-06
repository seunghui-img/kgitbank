import googletrans
from googletrans import Translator

# googletrans.LANGUAGES : 지원되는 언어의 종류가 키값으로 
print(googletrans.LANGUAGES)
 
text1 = "Hello welcome to my website!"
 
translator = Translator()

# detect: 문자열의 언어가 뭔지 확인
print(translator.detect(text1))
 
trans1 = translator.translate(text1, src='en', dest='ja')
print("English to Japanese: ", trans1.text)
