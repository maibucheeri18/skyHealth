# Co-authored: Student_A_Annie_Moradians, Student_B_Aathika_Ajmal_Basha, Student_C_Mai_Bucheeri, Student_D_Diego_Santos_de_Freitas

from skyHealth.utils import get_user_level_context

# this adds the navbar across all templates
def navbar_context(request):
    return get_user_level_context(request)
