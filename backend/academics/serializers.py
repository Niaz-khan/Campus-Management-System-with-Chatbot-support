from rest_framework import serializers
from .models import Batch, Program

class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = ['id', 'name', 'start_date', 'end_date', 'is_active']


class ProgramSerializer(serializers.ModelSerializer):
    batch_name = serializers.CharField(source='batch.name', read_only=True)  # for convenience

    class Meta:
        model = Program
        fields = ['id', 'name', 'batch', 'batch_name', 'duration_years', 'total_semesters', 'description']
