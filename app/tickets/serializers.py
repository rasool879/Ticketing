from  tickets.models import *
from rest_framework import serializers


class TicketSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketSubject
        fields = ['subject','id']


class TicketSerializer(serializers.ModelSerializer):
    subject = serializers.CharField(source='subject.subject')
    class Meta:
        model = Ticket
        fields = ['ref_no', 'title', 'subject', 'status', 'created_at'] 


class TicketMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketMessage
        fields = ['text','admin_name','created_at', 'attachment_url']
