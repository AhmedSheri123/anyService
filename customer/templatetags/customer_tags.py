from django import template
from django.template.defaultfilters import stringfilter
from messenger.models import MessagesModel, MessengerModel, BlockUserModel, FavoriteUserModel
from django.contrib.auth.models import User
from accounts.models import UserProfile, Review
import os

register = template.Library()

@register.simple_tag
@stringfilter
def get_request_service_review(ser_req_id, user_id):
    review = Review.objects.filter(service_request_id=ser_req_id, reviewer__user__id=user_id)
    if review:
        return review.first()
    
    return None


@register.simple_tag
@stringfilter
def get_service_review(service_id):
    review = Review.objects.filter(service_request__service__id=service_id)
    return review
    
