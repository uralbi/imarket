from django.db import models
from accounts.models import Account
from market.models import Item


class Chat(models.Model):
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="receiver")
    subject = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="product")
    content = models.TextField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        mess = f'Message {self.sender}>>{self.receiver}'
        return mess