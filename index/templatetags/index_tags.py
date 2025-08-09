from django import template


register = template.Library()


@register.filter(name="is_image")
def is_image(value):
    if not isinstance(value, str):
        return False
    return value.lower().endswith(("jpg", "png", "svg",
                                   "gif", "ico", "jpeg", ))


@register.filter(name="is_video")
def is_video(value):
    if not isinstance(value, str):
        return False
    return value.lower().endswith(('.mp4', '.webm', ))
