from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from utils.generals import get_ref_nom
from tickets.models import *
from tickets.serializers import *


def validate_data(data, required_data):
    for key in required_data:
        if key not in data:
            return False
    return True


class CreateTicket(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, req):
        data = req.POST
        if not validate_data(data, ['subject_id','title','text']):
            return Response({'code':104, 'data':{}, 'message':f"required_data: {['subject_id','title','text']}"}, status=400)
        subject = TicketSubject.objects.filter(id=data['subject_id'])
        if not subject:
            return Response({'code':105, 'data':{}, 'message':'invalid subject'}, status=422)
        if not data['title']:
            return Response({'code':106, 'data':{}, 'message':'blank title'}, status=422)
        ticket = Ticket.objects.create(subject=subject[0], user=req.user, title=data['title'], ref_no=get_ref_nom(Ticket))
        TicketMessage.objects.create(ticket=ticket, text=data['text'], attachment=req.FILES.get('attachment'))
        return Response({'code':100, 'data':{'ref_no':ticket.ref_no}, 'message':''})



class AnswerTicket(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, req):
        data = req.POST
        if not validate_data(data, ['ticket_ref_no','text']):
            return Response({'code':104, 'data':{}, 'message':f"required_data: {['ticket_ref_no','text']}"}, status=400)
        if not data['text'] and not req.FILES.get('attachment'):
            return Response({'code':106, 'data':{}, 'message':'blank title'}, status=422)
        ticket = Ticket.objects.filter(ref_no=data['ticket_ref_no'])
        if not ticket:
            return Response({'code':107, 'data':{}, 'message':'invalid ticket'}, status=422)     
        if ticket[0].user != req.user and not req.user.is_staff:
            return Response({'code':108, 'data':{}, 'message':'access denied'}, status=403)
        TicketMessage.objects.create(
            ticket = ticket[0],
            text = data['text'],
            attachment = req.FILES.get('attachment'),
            admin = req.user if req.user.is_staff else None
        )
        ticket[0].status = 'ANSWERED' if req.user.is_staff else 'WAITING'
        ticket[0].save()
        return Response({'code':100, 'data':{}, 'message':''})



class TicketSubjects(APIView):
    def get(self, req):
        subjects = TicketSubject.objects.filter(is_active=True)
        subjects = TicketSubjectSerializer(subjects, many=True)
        return Response({'code':100, 'data':subjects.data, 'message':''})


class UserTickets(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,req):
        tickets = req.user.tickets_as_user.all()
        tickets = TicketSerializer(tickets, many=True).data
        return Response({'code':100, 'data':tickets, 'message':''})
        

class TicketChats(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,req):
        data = req.GET
        if not validate_data(data, ['ref_no']):
            return Response({'code':104, 'data':{}, 'message':f"required_data: {['ref_no']}"},status=400)
        ticket = Ticket.objects.filter(ref_no=data['ref_no'])
        if not ticket:
            return Response({'code':107, 'data':{}, 'message':'invalid ticket'}, status=422)   
        if ticket[0].user != req.user and not req.user.is_staff:
            return Response({'code':108, 'data':{}, 'message':'access denied'}, status=403)
        chats = TicketMessage.objects.filter(ticket=ticket[0])
        chats = TicketMessageSerializer(chats, many=True).data
        return Response({'code':100, 'data':chats, 'message':''})

       