from django_filters.rest_framework import FilterSet, CharFilter
from freelancer.project.models import Project
from django.contrib.postgres.fields import ArrayField



class ProjectFilter(FilterSet):
    
    class Meta:
        model = Project
        fields = {
            "category": ["exact"],
            "title": ["icontains"],
            "tags": ["exact"],
            "budget": ["gt", "lt"]
        }
        
        filter_overrides = {
            ArrayField: {
                'filter_class': CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
        }