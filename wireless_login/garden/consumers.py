# garden/consumers.py
from channels.generic.http import AsyncHttpConsumer
from channels.generic.websocket import AsyncWebsocketConsumer, SyncConsumer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Garden, Outlet, Picture
from login.models import WirelessUser
import json
from django.conf import settings
from django.core.serializers import serialize
from . import tasks
import os

class change_detect(SyncConsumer):

    wifi = WirelessUser.objects.get(pk=1)

    try:
        channel_layer = get_channel_layer()
#        async_to_sync(channel_layer.group_add)(settings.BOX_SERIAL,'change_detect')
        print("------------- I'm Alive! ------------------")




        def data_exchange(self, event):
            channel_layer=get_channel_layer()
    #        async_to_sync(channel_layer.group_add)(settings.BOX_SERIAL,'change_detect')
            garden = Garden.objects.get(pk=3)
            event['outlet_number']=int(event['outlet_number'])
            if event['outlet_number'] !=0:
                outlet = Outlet.objects.get(number=event['outlet_number'], garden = garden)
                setattr(outlet, event['variable'], event['new_value'])
                outlet.save()
        #Do stuff for PUMP
                if outlet.style == "PUMP":
                    outlet.pump_calculator()
                if outlet.style == "UVB":
                    outlet.uvb_calculator()
        # Just so we can see what we're changing
                new_variable = getattr(outlet,event['variable'])
                print(new_variable)
            else:
                setattr(garden, event['variable'], event['new_value'])
                garden.save()
                new_variable = getattr(garden,event['variable'])
                print(new_variable)
#        async_to_sync(channel_layer.group_add)(settings.BOX_SERIAL,'change_detect')

        def update_mode_for_real(self,event):
            print('trying to update')
            channel_layer=get_channel_layer()
#        async_to_sync(channel_layer.group_add)(settings.BOX_SERIAL,'change_detect')
            garden = Garden.objects.get(pk=3)
            new_git = event['new_git']
            file_name = event['file_name']
            os.system("wget "+new_git+" -O " + file_name)
#        async_to_sync(channel_layer.group_add)(settings.BOX_SERIAL,'change_detect')

        def toggle(self,event):
            channel_layer=get_channel_layer()
#        async_to_sync(channel_layer.group_add)(settings.BOX_SERIAL,'change_detect')
            garden = Garden.objects.get(pk=3)
            outlet = Outlet.objects.get(number=event['outlet'], garden = garden)
            if event['is_on']:outlet.on()
            else: outlet.off()
            print(outlet,"is on? ",outlet.is_on)
#        async_to_sync(channel_layer.group_add)(settings.BOX_SERIAL,'change_detect')

        def camera_load(self, event):
            print("Taking picture!")
            tasks.camera_check(now='yes')
            channel_layer=get_channel_layer()
            print("Picture done!")
#           json.loads allows the bullshit strings that look like lists to become lists, or something
            async_to_sync(channel_layer.group_send)(
                settings.BOX_SERIAL, #Send it the right way
                {'type' : 'camera_confirmation'},
            )

        def garden_load(self, event):
            print("Garden Load Activated!")
        #tasks.camera_check(now='yes')
            channel_layer=get_channel_layer()
            garden = Garden.objects.get(pk=3)
            data = {}
            data['type'] = 'load_data'
            garden = Garden.objects.get(pk=3)
            bombo = json.loads(serialize('json', [garden]))
            data['garden_stuff'] = bombo[0]
            for x in range(1,6):
                outlet = Outlet.objects.get(number=x, garden=garden)
                bombo = json.loads(serialize('json', [outlet]))
                data["outlet_"+str(x)+"_stuff"] = bombo[0]
            x=1
            for pic in Picture.objects.all():
                bombo = json.loads(serialize('json', [pic]))
                data['picture update '+ str(x)] = bombo[0]
                x = x+1
            Picture.objects.all().delete()
        
            
        
#       json.loads allows the bullshit strings that look like lists to become lists, or something
            async_to_sync(channel_layer.group_send)(
                settings.BOX_SERIAL, #Send it the right way
                data,
            )
        
        def toggler(num,is_on):
            channel_layer=get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                settings.BOX_SERIAL, #Send it the right way
                {
                    'outlet': num,
                    'type' : 'togglest',
                    'is_on' : is_on,
                },
            )
    
        def load_data(self,event):
            pass

        def togglest(self,event):
            pass
        def camera_confirmation(self,event):
            pass
    except:
        print("I AM DEAD :(")
