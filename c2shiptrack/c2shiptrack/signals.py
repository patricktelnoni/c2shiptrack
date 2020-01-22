from c2shiptrack.models import Sessions
from django.db.models.signals import pre_save
from django.dispatch import receiver





def send_message(event):
    '''
    Call back function to send message to the browser
    '''


    # message = event['text']
    # channel_layer = channels.layers.get_channel_layer()
    # # Send message to WebSocket
    # async_to_sync(channel_layer.send)(text_data=json.dumps(
    #     message
    # ))

@receiver(pre_save, sender=Sessions)
def save_profile(sender, instance, **kwargs):
    print("Session inserted")
    # channel_layer = channels.layers.get_channel_layer()
    # async_to_sync(channel_layer.group_send)(
    #     'chat_queen',
    #     {
    #         "type": "chat_message",
    #         "message": "Session inserted"
    #     }
    # )
    # async_to_sync(channel_layer.group_send)(
    #     {"type": "chat_message", "message": "data"}
    # )

