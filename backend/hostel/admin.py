from django.contrib import admin
from .models import Hostel, Room, RoomAllocation, HostelViolation

@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'created_at')
    search_fields = ('name',)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('hostel', 'number', 'room_type', 'capacity', 'current_occupancy', 'monthly_fee', 'is_active')
    list_filter = ('hostel', 'room_type', 'is_active')
    search_fields = ('number',)

@admin.register(RoomAllocation)
class RoomAllocationAdmin(admin.ModelAdmin):
    list_display = ('student', 'room', 'start_date', 'end_date', 'is_active', 'allocated_by')
    list_filter = ('is_active', 'room__hostel')
    search_fields = ('student__roll_no', 'room__number')

@admin.register(HostelViolation)
class HostelViolationAdmin(admin.ModelAdmin):
    list_display = ('allocation', 'reported_by', 'date', 'fine_amount', 'is_resolved')
    list_filter = ('is_resolved',)
    search_fields = ('allocation__student__roll_no',)
