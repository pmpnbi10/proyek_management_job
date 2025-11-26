from django import template

register = template.Library()

@register.filter(name='get')
def get(dictionary, key):
    """
    Memungkinkan kita memanggil dictionary.get(key) di template.
    Contoh: {{ data.dates|get:day }}
    
    Ini akan memperbaiki error 'Invalid filter: get'.
    """
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None


@register.filter(name='can_edit_job')
def can_edit_job(job, user):
    """
    Check apakah user bisa edit job ini.
    user bisa edit HANYA jika:
    - user adalah creator (pic)
    - user adalah assigned_to
    - user adalah supervisor dari assigned_to (bukan dari pic!)
    """
    if not user or not user.is_authenticated:
        return False
    
    # User adalah creator
    if job.pic == user:
        return True

    # User adalah yang di-assign
    if job.assigned_to == user:
        return True

    subordinate_ids = user.get_all_subordinates()

    # User adalah supervisor dari assigned_to
    if job.assigned_to is not None and job.assigned_to.id in subordinate_ids:
        return True

    # User adalah supervisor dari PIC (supervisor boleh juga edit job created by their subordinate)
    if job.pic is not None and job.pic.id in subordinate_ids:
        return True

    return False