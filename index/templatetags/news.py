from django.template import Library
from chat.models import Message
from datetime import datetime, timedelta
from auth_sys.models import Profile
from posts.models import Post, Comment
from django.urls import reverse


register = Library()


@register.filter(name="messages")
def messages(request):
    date = (datetime.now() - timedelta(days=7)).date()
    message_dict = dict()

    followers = Profile.objects.filter(followers__in=[request.user])
    for follower in followers:
        chat_messages = Message.objects.filter(created_at__gte=date,
                                               adresat=follower.user)
        for chat_message in chat_messages:
            url = reverse("message-list",
                          kwargs={"user_pk": chat_message.adresat.pk, })
            message = f"""<a href={url}>
                    {chat_message.adresat} has written the message.
                        </a>"""
            message_dict[chat_message.created_at] = message
        post_messages = Post.objects.filter(created_at__gte=date,
                                            author=follower.user)
        for post_message in post_messages:
            url = reverse("post-details",
                          kwargs={"pk": post_message.pk, })
            message = f"""<a href={url}>
                    {post_message.author} has posted something.
                        </a>"""
            message_dict[post_message.created_at] = message

    comments = Comment.objects.filter(author=request.user)
    for comment in comments:
        comment_messages = Comment.objects.filter(created_at__gte=date,
                                                  replied_comment=comment)
        for comment_message in comment_messages:
            url = reverse("post-details",
                          kwargs={"pk": comment_message.post.pk, })
            message = f"""<a href={url}>
                {comment_message.author} replied on your comment
                    </a>"""
            message_dict[comment_message.created_at] = message

    messag_list = list()
    for current_date in sorted(message_dict.keys(), reverse=True):
        messag_list.append(message_dict[current_date])

    return messag_list
