from django.db import models
from acc.models import User

# Create your models here.
class Board(models.Model):
    subject = models.CharField(max_length=200)

    # ForeignKey - 1:N
    # related_name - user 객체의 별칭을 말함. likey 에서 호출되는 객체가 같기 때문에 별칭이 필요
    # board_set 함수 대신 writer으로 바로 호출가능
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="writer")
    content = models.TextField()

    # ManyToManyField - N:N
    likey = models.ManyToManyField(User, blank=True, related_name="likey")

    pubdate = models.DateTimeField()

    def __str__(self):
        return f"{self.writer}_{self.subject}"

    def getSummary(self):
        if len(self.content) > 30:
            return f"{self.content[:30]} ..."
        return self.content

class Reply(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    replyer = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    pubdate = models.DateTimeField()

    def __str__(self):
        return f"{self.board}({self.replyer})"