from django.contrib import admin
from .models import Facility, GymMembership, Equipment, EquipmentIssue, Tournament, TournamentRegistration

@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('name','facility_type','location','capacity','is_active','created_at')
    list_filter = ('facility_type','is_active')
    search_fields = ('name','location')

@admin.register(GymMembership)
class GymMembershipAdmin(admin.ModelAdmin):
    list_display = ('student','facility','membership_type','start_date','end_date','is_active','price')
    list_filter = ('membership_type','is_active')
    search_fields = ('student__roll_no',)

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name','total_quantity','available_quantity','is_active')
    search_fields = ('name',)

@admin.register(EquipmentIssue)
class EquipmentIssueAdmin(admin.ModelAdmin):
    list_display = ('equipment','issued_to','quantity','issue_date','due_date','returned')
    list_filter = ('returned',)

@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ('name','start_date','end_date','venue','capacity','is_active')
    search_fields = ('name',)

@admin.register(TournamentRegistration)
class TournamentRegistrationAdmin(admin.ModelAdmin):
    list_display = ('tournament','student','registered_at','fee_paid')
    list_filter = ('fee_paid',)
