from django import template


register = template.Library()


@register.filter(name="endswith")
def endswith(value, arg):
    if not isinstance(value, str):
        return False
    return value.lower().endswith(arg.lower())


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


@register.filter(name="is_audio")
def is_audio(value):
    if not isinstance(value, str):
        return False
    return value.lower().endswith(('.mp3', '.wav', '.ogg', '.aac'))
