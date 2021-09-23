from datetime import datetime, timedelta
from re import T
from tools import LoadFile
typeOfCommands = ['pc','g','o','h']

last_cooldown = {} # Dictionary with server as keys and datetime as values  

def cooldown(channel,guild,ToC,Command):
    try:
        Cs = LoadFile('Cs')
        
    except EOFError:
        Cs = {}
        
    try:
      
        Cc = LoadFile('Cc')
    except EOFError:
        Cc = {}
    
    try:
       
        if Cc[f'{channel}_{Command}'] > 0:
            return cooldownF(guild,Cc[f'{channel}_{Command}'],Command)

    except KeyError:
        try:
           
            if Cc[f'{channel}_{ToC}'] > 0:
                return cooldownF(guild,Cc[f'{channel}_{ToC}'],ToC)

        except KeyError:
            try:
                       
                if Cs[f'{guild}_{Command}'] > 0:
                    return cooldownF(guild,Cs[f'{guild}_{Command}'],Command)
                    
            except KeyError:
                try:
                  
                    if Cs[f'{guild}_{ToC}'] > 0: 
                        return cooldownF(guild,Cs[f'{guild}_{ToC}'],ToC) 

                except KeyError:
                    
                    return("ok_send")
                        
    

def cooldownF(guild,cooldown,arg=None):
    try:
        # calculate the amount of time since the last (successful) use of the command
        time_elapsed = datetime.now() - last_cooldown[f'{guild}{arg}'] 
    except KeyError:
        # the key doesn't exist, the caller used the command for the first time
        # or the bot has been shut down since
        time_elapsed = None
        last_cooldown[f'{guild}{arg}'] = datetime.now()
        

    if time_elapsed is None or time_elapsed.seconds > cooldown:

        last_cooldown[f'{guild}{arg}'] = datetime.now() # the message was sent so we start the cooldown again
        
        return("ok_send")
        
    else:
        remain = cooldown - time_elapsed.seconds
        remain = round(remain / 60, 2)
        return(remain)



