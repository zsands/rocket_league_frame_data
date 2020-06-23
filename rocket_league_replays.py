# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 20:27:13 2020

@author: Zach
"""
import json

f = open('D:/75C26A43424A1EAE39CF18BDCE105827.json') 

f = json.load(f)

first_frame = f['Frames'][0]['ActorUpdates']

object_dict = {}

position_dict = {}

def actor_parse(actor,object_dict):
    actor_id = actor['Id']
    parent = None
    if 'ClassName' not in actor.keys():
         return object_dict
    class_name = actor['ClassName']

    if class_name not in ['TAGame.GameEvent_Soccar_TA','TAGame.CameraSettingsActor_TA','TAGame.GRI_TA'
                          ,'ProjectX.NetModeReplicator_X','TAGame.Team_Soccar_TA','TAGame.CrowdActor_TA','TAGame.CrowdManager_TA']:
        if class_name == 'TAGame.Ball_TA':
            parent = 'Ball'
            
        elif class_name == 'TAGame.PRI_TA':
            parent =  actor['Engine.PlayerReplicationInfo:PlayerName']
            
        elif 'Engine.Pawn:PlayerReplicationInfo' in actor.keys():
            parent = actor['Engine.Pawn:PlayerReplicationInfo']['ActorId']
            
        elif 'TAGame.CarComponent_TA:Vehicle' in actor.keys():
            parent = actor['TAGame.CarComponent_TA:Vehicle']['ActorId']
        
        if parent in object_dict.keys():        
            while object_dict[parent] in object_dict.keys():
                parent = object_dict[parent]
                
        for key in object_dict.keys():
            if object_dict[key] == actor_id:
                if type(parent) == str:
                    object_dict[key] = actor_id
                else:
                    object_dict[key] = parent
                    
        object_dict[actor_id] = parent
    
    return object_dict

def position_parse(actor,object_dict,position_dict,time):
    actor_id = actor['Id']
    if 'TAGame.RBActor_TA:ReplicatedRBState' not in actor.keys():
        print('No Position Data : ',actor_id)
    else:
        position = [x for x in actor['TAGame.RBActor_TA:ReplicatedRBState']['Position'].values()]
        if actor_id in object_dict.keys():
            if type(object_dict[actor_id]) != str:
                actor = object_dict[object_dict[actor_id]]
            else:
                actor = object_dict[actor_id]
            if time not in position_dict.keys():
                position_dict[time] = {actor_id : position}
            else:
                position_dict[time][actor_id] = position
    return position_dict
            
    
    

def frame_parse(frame,object_dict,position_dict):
    if any('ClassName' in x.keys() for x in frame['ActorUpdates']):
        for actor in frame['ActorUpdates']:
            object_dict = actor_parse(actor,object_dict)
    time = frame['Time']
    for actor in frame['ActorUpdates']:
        position_dict = position_parse(actor,object_dict,position_dict,time)
        
    return object_dict,position_dict


counter = 0
for frame in f['Frames']:
    print(counter)
    object_dict,position_dict = frame_parse(frame,object_dict,position_dict)
    counter += 1