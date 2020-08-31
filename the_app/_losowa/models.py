

class The_game():
    # rnd_num=0
    # current_result=''
    # actual_turn=''
    # i=0
    # game_ending=False
    # result_pile=[]

    def __init__(self,rnd_num,current_result,actual_turn,i,result_pile,game_ending):
        
        self.rnd_num=rnd_num
        self.current_result=current_result
        self.actual_turn=actual_turn
        self.i=i
        self.result_pile=result_pile
        self.game_ending=game_ending

    def go_turn(self,number):
        if int (number)==4021:
            self.current_result='Błędny wpis!'
            self.i+=1
            self.actual_turn=f'Próba nr {self.i}'
            self.result_pile.insert(0,'error_')
        elif int(number)<self.rnd_num:
            self.actual_turn='To jest za mało1...Próbuj dalej!'
            self.i+=1
            self.actual_turn=f'Próba nr {self.i}'
            self.result_pile.insert(0,'to_little')
        elif int(number)>self.rnd_num:
            self.actual_turn='To jest za duzo... Próbuj dalej'
            self.i+=1
            self.actual_turn=f'Próba nr {self.i}'
            self.result_pile.insert(0,'to_much')
        elif int(number)==self.rnd_num:
            self.actual_turn='BRAWO!!! To jest właśnie ta liczba!'
            self.i+=1
            self.actual_turn=f'Za {self.i} razem'
            self.result_pile.insert(0,'win')
            self.game_ending=True
    
    def to_json(self):
        game_state = {}
        game_state['rnd_num']=self.rnd_num
        game_state['current_result']=self.current_result
        game_state['actual_turn']=self.actual_turn
        game_state['i']=self.i
        game_state['result_pile']=self.result_pile
        game_state['game_ending']=self.game_ending


        return game_state

    



