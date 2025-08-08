def profile_image(request):
    if request.user.is_authenticated:
        try:
            return {
                'profile_image': request.user.userprofile.profile_image
            }
        except:
            return {}
    return {}