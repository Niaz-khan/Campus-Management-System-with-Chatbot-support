from rest_framework import serializers
from .models import Facility, GymMembership, Equipment, EquipmentIssue, Tournament, TournamentRegistration
from students.serializers import StudentProfileSerializer

class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = ['id','name','facility_type','location','capacity','is_active','created_at']

class GymMembershipSerializer(serializers.ModelSerializer):
    student_details = StudentProfileSerializer(source='student', read_only=True)
    facility_name = serializers.CharField(source='facility.name', read_only=True)
    issued_by_name = serializers.CharField(source='issued_by.get_full_name', read_only=True)

    class Meta:
        model = GymMembership
        fields = ['id','student','student_details','facility','facility_name','membership_type','start_date','end_date','price','is_active','issued_by','issued_by_name','created_at']
        read_only_fields = ['issued_by','created_at']

class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ['id','name','description','total_quantity','available_quantity','is_active','created_at']

class EquipmentIssueSerializer(serializers.ModelSerializer):
    equipment_name = serializers.CharField(source='equipment.name', read_only=True)
    student_roll_no = serializers.CharField(source='issued_to.roll_no', read_only=True)

    class Meta:
        model = EquipmentIssue
        fields = ['id','equipment','equipment_name','issued_to','student_roll_no','issued_by','quantity','issue_date','due_date','returned','returned_at','overdue_fine','remarks']
        read_only_fields = ['issue_date','returned_at']

class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ['id','name','description','start_date','end_date','venue','capacity','is_active','created_by','created_at']

class TournamentRegistrationSerializer(serializers.ModelSerializer):
    student_details = StudentProfileSerializer(source='student', read_only=True)
    tournament_name = serializers.CharField(source='tournament.name', read_only=True)

    class Meta:
        model = TournamentRegistration
        fields = ['id','tournament','tournament_name','student','student_details','registered_at','attended','fee_paid']
        read_only_fields = ['registered_at','attended','fee_paid']
