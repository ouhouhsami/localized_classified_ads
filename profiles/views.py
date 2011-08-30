from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from models import UserProfile
from django.contrib.auth.models import User
from ads.models import HomeForSaleAd, AdSearch
from moderation.models import ModeratedObject
from django.shortcuts import redirect
from ads.decorators import site_decorator

@site_decorator
def detail(request, username, Ad=None, AdForm=None, AdFilterSet=None):
    '''
    page_user = get_object_or_404(User, username = username)
    profile_class = get_profile_model()
    profile = get_object_or_404(profile_class, user = page_user)
    '''
    user = get_object_or_404(User,
                             username__iexact=username)
    profile = user.get_profile()
    print profile
    #if not profile.can_view_profile(request.user):
    #    return HttpResponseForbidden(_("You don't have permission to view this profile."))
    # ads below are site specific :( because of decorators ...
    ads = Ad.objects.exclude(delete_date__isnull = False).filter(user_profile = profile)
    #.filter(_relation_object__moderation_status = 1)
    all_user_ads = False
    searchs = False
    if profile.user == request.user:
        all_user_ads = HomeForSaleAd.unmoderated_objects.filter(user_profile = profile).exclude(delete_date__isnull = False)
        searchs = AdSearch.objects.filter(user_profile = profile)
    return render_to_response('profiles/profile.html', {'profile':profile, 'ads':ads, 'all_user_ads':all_user_ads, 'searchs':searchs}, context_instance = RequestContext(request))

