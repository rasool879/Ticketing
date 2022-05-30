from django.urls import path
from tickets.views import *

urlpatterns = [
    path('create_ticket', CreateTicket.as_view()),
    path('answer_ticket', AnswerTicket.as_view()),
    path('ticket_subjects', TicketSubjects.as_view()),
    path('user_tickets', UserTickets.as_view()),
    path('ticket_chats', TicketChats.as_view()),
]
