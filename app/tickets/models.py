from django.db import models



class TicketSubject(models.Model):
    subject = models.CharField(max_length=100)
    is_active = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject


class Ticket(models.Model):
    ref_no = models.CharField(max_length=15)
    title = models.CharField(max_length=255)
    user  = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='tickets_as_user')
    subject  = models.ForeignKey(TicketSubject, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, default='WAITING', choices=(('ANSWERED','ANSWERED'), ('WAITING','WAITING'), ('CLOSED','CLOSED')))
    current_admin = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='tickets_as_admin', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class TicketMessage(models.Model):
    ticket  = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    text = models.TextField()
    attachment = models.FileField(upload_to='attachments', null=True, blank=True)
    admin = models.ForeignKey('account.User', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def admin_name(self):
        return f'{self.admin.first_name} {self.admin.last_name}' if self.admin else None

    def attachment_url(self):
        if self.attachment:
            return self.attachment.url
