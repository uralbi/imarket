from infoportal.settings import register


@register.filter
def words_to_list(value):
    """Make list out of words"""
    value = value.split(' ')
    return value