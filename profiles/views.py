from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from models import UserProfile
from django.contrib.auth.models import User
from ads.models import HomeForSaleAd, HomeForSaleSearch
from moderation.models import ModeratedObject
from django.shortcuts import redirect

def profile_detail(request, username, template_name='userena/profile_detail.html', extra_context=None):
    """
    Detailed view of an user.

    :param username:
        String of the username of which the profile should be viewed.

    :param template_name:
        String representing the template name that should be used to display
        the profile.

    :param extra_context:
        Dictionary of variables which should be supplied to the template. The
        ``profile`` key is always the current profile.

    **Context**

    ``profile``
        Instance of the currently viewed ``Profile``.

    """
    user = get_object_or_404(User,
                             username__iexact=username)
    profile = user.get_profile()
    if not profile.can_view_profile(request.user):
        return HttpResponseForbidden(_("You don't have permission to view this profile."))
    if not extra_context: extra_context = dict()
    extra_context['profile'] = user.get_profile()
    return direct_to_template(request,
                              template_name,
                              extra_context=extra_context)


def detail(request, username):
    '''
    page_user = get_object_or_404(User, username = username)
    profile_class = get_profile_model()
    profile = get_object_or_404(profile_class, user = page_user)
    '''
    user = get_object_or_404(User,
                             username__iexact=username)
    profile = user.get_profile()
    if not profile.can_view_profile(request.user):
        return HttpResponseForbidden(_("You don't have permission to view this profile."))
    #profile = UserProfile.objects.get(user__username = username)
    ads = HomeForSaleAd.objects.exclude(delete_date__isnull = False).filter(user_profile = profile)
    all_user_ads = False
    searchs = False
    if profile.user == request.user:
        all_user_ads = HomeForSaleAd.unmoderated_objects.filter(user_profile = profile)
        searchs = HomeForSaleSearch.objects.filter(user_profile = profile)
    return render_to_response('profiles/profile.html', {'profile':profile, 'ads':ads, 'all_user_ads':all_user_ads, 'searchs':searchs}, context_instance = RequestContext(request))

def list(request):
    # sort of a hack to redirect to profil detail
    return redirect('profile_detail', username=request.user.username)
    #profiles = UserProfile.objects.all()
    #return render_to_response('profiles/profiles.html', {'profiles':profiles}, context_instance = RequestContext(request))