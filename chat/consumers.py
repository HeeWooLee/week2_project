import json 
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

class PersonalChatConsumer(AsyncWebsocketConsumer):
    async def connet(self):
        pass
#         # get id of current user
#         my_id = self.scope['user'].id
#         # url route == 'ws/<int:id>' get id from url 
#         # kwargs : keyword arguments 
#         other_user_id = self.scope['url_route']['kwargs']['id']

#         # create room : people connected to same room can interact/ only 2 person can get to one room
#         # make sure same room name for both user
#         # ex) '2-1' 
#         if int(my_id) > int(other_user_id):
#             self.room_name = f'{my_id}-{other_user_id}'
#         else: 
#             self.room_name = f'{other_user_id}-{my_id}'

#         self.room_group_name = 'chat_%s'% self.room_name

#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name,
#         )

#         await self.accept