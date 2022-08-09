from infoportal.settings import register


@register.filter
def nums_to_list(value):
    """Make list out of words"""
    num_list = [i for i in range(1, int(value)+1)]
    return num_list