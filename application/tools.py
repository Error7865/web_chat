
            # Thoes are function and other instance that will help to maintain my code clean 


def select_instace_to_ls(instances:list)->list:
    '''This function will just convert this structure
    [(instance,),(instance,),...]
    to this structure
    [instance,instance, ....]'''

    ls=list()
    for set in instances:
        ls.append(set[0])
    return ls
            

def msginstance_to_ls(msg_ls, user_id)->list:
    '''This function take Messages instance and convert a list
    where each list item will be a dictionary which will contain
    message and owner if message was sent by user self then owner 
    will be True or False otherwise'''

    ls=list()
    for message in msg_ls:
        owner=False     #message received user from sender
        if message.sender==user_id:
            owner=True      #user sent message to receiver
        ls.append(dict(msg=message.msg, owner=owner))
    return ls


