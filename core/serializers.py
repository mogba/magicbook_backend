from django.db.models.query import QuerySet
from rest_framework import serializers

# class ModelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = None
#         fields = '__all__'
    
#     def __init__(self, *args, **kwargs):
#         model = kwargs.pop('model', None)
#         self.Meta.model = model
#         super(ModelSerializer, self).__init__(*args, **kwargs)

class ModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = None
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        if len(args) == 0:
            raise ValueError("ModelSerializer must be initialized with a model instance or a queryset.")
        
        instance = args[0]
        
        if instance is not None:
            if isinstance(instance, QuerySet):
                model = instance[0].__class__
            else:
                model = instance.__class__
            
            self.Meta.model = model
        
        super(ModelSerializer, self).__init__(*args, **kwargs)
