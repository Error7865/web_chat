class Stack:
    '''This is stack which have some unique ability like
    *It hold only unique data 
    '''
    def __init__(self, *args, **kwargs) -> None:
        super(Stack, self).__init__(*args, **kwargs)
        self.stack=list()
    
    def push(self, data):
        '''This method same as append method of list'''
        if data in self.stack:
            raise ValueError('Data already exits in stack. ')
        return self.stack.append(data)            

    def pop(self, index=None):
        '''It is similar to pop method of list'''
        
        # if index is None:
        try:
            return self.stack.pop(index)
        except TypeError as e:
            return self.stack.pop()
    
    def is_empty(self):
        '''This method check if stack is empty or not and return
        boolean value base on it.'''
        if len(self.stack)==0:
            return True
        return False
    
    def get(self,index:int):
        '''This method take index number and return 
        value of that index'''

        return self.stack[index]
    
    def remove(self, data):
        '''This method remove provided data
        and return it'''

        return self.stack.remove(data)
    
    def __repr__(self)-> str:
        return f'{self.stack}'
    