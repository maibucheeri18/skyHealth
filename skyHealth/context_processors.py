from skyHealth.utils import get_user_level_context

# this adds the navbar across all templates
def navbar_context(request):
    return get_user_level_context(request)
