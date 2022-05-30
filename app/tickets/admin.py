from django.contrib import admin
from tickets.models import *


admin.site.register(TicketSubject)
admin.site.register(Ticket)
admin.site.register(TicketMessage)