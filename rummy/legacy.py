import random as r

cards={
    "Spades":['A',*list(map(str,[i for i in range(2,10)])),'JACK','QUEEN','KING',"JOKER"],
    "Clubs":['A',*list(map(str,[i for i in range(2,10)])),'JACK','QUEEN','KING',"JOKER"],
    "Diamonds":['A',*list(map(str,[i for i in range(2,10)])),'JACK','QUEEN','KING',"JOKER"],
    "Hearts":['A',*list(map(str,[i for i in range(2,10)])),'JACK','QUEEN','KING',"JOKER"]
}
pile={
  "Spades":[],"Clubs":[],"Diamonds":[],"Hearts":[]
}


class RUMMY():
  
  
  def __init__(self):
    self.num_players,self.turn_count=0,0
    self.players,self.set_pile={},[]
    self.current_player,self.drawn_card,self.last_card_on_the_pile="","",""
    self.player_names=[]
    self.sequence_pile={"Spades":[],"Clubs":[],"Diamonds":[],"Hearts":[]}
    self.wild_joker=None
    self.winner=None
    self.choice_made=False
    self.standard_seq=['A','2','3','4','5','6','7','8','9','10','JACK','QUEEN','KING','JOKER']

  def check_Winner(self):
     """This Function is designed to check for the Winner at the end of each round"""
     win=[False for i in range(len(self.player_names))]
     player_count=0
     for player in self.player_names:
        for suit in self.players[player]:
           if len(self.players[player][suit]==0):
              win[player_count]=True
           else:
              win[player_count]=False
        player_count+=1
     for i in range(len(win)):
        return i if win[i] else None

  def get_player_names(self):
    """This Function just obtains the player count and Player names from the User and
    sets their initial decks up"""
    while(self.num_players==0):
       self.num_players=int(input("Minimum 2 and Maximum 6 players allowed, Enter the Number?\n>> "))
       if self.num_players > 6 or self.num_players<2:
          self.num_players=0   
          print("Not more than 6 players allowed!")
       else:
          break

    for i in range(self.num_players):
        player_name=input("Enter Player "+str(i)+" name\n>> ")#Accepting Player Names
        player_cards={"Spades":[],"Clubs":[],"Hearts":[],"Diamonds":[],"Points":0}
        self.players.update({player_name:player_cards})
    self.player_names=list(self.players.keys())



  def __get_Suit(self,remove=True): #The double underscore makes sure it remains private and cannot be accessed
    while(True):                      #Outside the class
      Suit=list(cards.keys())[r.randint(0,3)]
      try:
        card_index=r.randint(0,13)
        card=cards[Suit][card_index]
        if(remove==True):
            cards[Suit].remove(card)
        break
      except:
        pass
    return (Suit,card)
  



  def distribute(self):
    card_count=1
    while(card_count<14):
      for i in range(len(self.players)):
        Suit,card=self.__get_Suit()
        self.players[list(self.players.keys())[i]][Suit].append(card)
      card_count+=1



  def show_cards(self):
    print("Showing Cards for player: ",self.current_player)
    if "y" in input("Are you Sure none of your Amigos are peeking over the shoulder?[y/n]\n>> ").lower():
      print(self.players[self.current_player])
    else:
      while("n" in input("GET RID OF THEM! I NEED TO SHOW YOU YOUR CARDS!!\n DONE??[y/n]\n>> ").lower()):
        pass
      print(self.players[self.current_player])



  def pile_empty(self):
    for i in list(pile.keys()):
      if len(pile[i])!=0:
        return False
    return True
  

  def set_joker(self):#Function to set the Wild Jokers Randomly
    self.wild_joker=self.__get_Suit(remove=False)
    print("Wild Joker Selected by the Dealer:",self.wild_joker)
    print("Now all the cards with the same Value, irrespective of their Suits, will be treated as WIlD JOKERS")

  
  
  def check_joker_rules(self,cards_avail,meld):
     print("Here's Some History about Jokers:\n\
           1. They can be used to complete a set/Sequence when you donot have enough cards\n\
           2. But the number of Jokers You can use should be less than the number of Natural\n\
              Cards\n\
           3. e.g. # If you only have one natural card, you can't use 2 Jokers to complete a\n\
                   # If you have 2 Nautural cards in a meld, you can put either 1 or 2 Jokers\n\
                   to complete the final meld\n\
                   # If you have 3 cards, then Jokers are not needed,though you can place one\n\
                   # If you have 4 cards in a set, Wild Jokers are not allowed")
     print("Your meld in hand:",meld," Jokers/Wild Cards in Hand:",cards_avail,"\n\
               You can only use at max 2 Jokers/Wild Cards!\n\
               Enter the Number of the cards to use...\n\
               1-for the first in the list of wild cards and so on\n\
               1 4- for the first and the fourth in the list of Wild Cards and so on")
     inp=input(">> ").split(" ")
     for i in inp:
        while True:
          try:
            i=int(i)-1
            key=list(cards_avail.keys())[i]
            #Whatever position the user has entered selecting the suit 
            #at that position to grab the card from
            if "JOKER" in cards_avail[key]:
              print("The Meld is in this type:",meld)
              meld.append((key,"JOKER"))
            else:
              meld.append(("Wild Card",cards_avail[key][0],cards_avail[key][1]))  
            return meld     
          except Exception as e:
            print("Error is :",e,"Ending the Game")
            exit(0)
            
        

     
  def card_lookup(self,card_value=None,Wild_card=None):
    cards_found={}
    for suit in cards.keys():
       current_player_suit=self.players[self.current_player][suit]
       if card_value in current_player_suit:
          cards_found.update({suit:[card_value]})  
       
       if Wild_card[1] in current_player_suit:
          if suit in cards_found.keys():
             cards_found[suit].append(Wild_card[1])
          else:
             cards_found.update({suit:Wild_card[1]})
    return cards_found  
  


          

  def display_rules(self):
    rules="~~ 10 cards are dealt with each player\n\
~~ The dealer selects 1 card randomly as the joker/wildcard.\n\
~~ The rest of the cards are kept on the table face down\n\
~~ The dealer also takes the top-most card from the rest of the cards \nand places it face-up on the table. \
   This becomes the discard pile.\n\
~~ During your turn, you can draw cards from the pile or pick up any card discarded by your opponent.\n\
~~ You have to discard 1 card as the number of cards in your hand remains constant.\n\
~~ In case you do not pick up/ discard you will lose 20 points (at the beginning of the game). During the game,\n\
this penalty goes up to 40 points. If you miss more than three turns, then you can lose 40 points.\n\
~~ You must form at least one pure sequence. A pure sequence is a combination of cards without any jokers. \n\
Example: A♠ 2♠ 3♠ or 2♦ 2♥ 2♣ 2♠\n\
~~ The other groups can be impure. Eg-  2♦ 2♥ Joker\n\
~~ If you have valid groups, you can declare “finish” or “rummy”,this is called declaring a hand\n\
~~ If your hand has valid combinations (called valid declaration), then you are the winner\n\
~~ Remember to be sure that your melding is valid. In case of an invalid declaration, you can lose 60 points" 





  def remove_meld_cards_from_player_deck(self,meld):
     for suit_value in meld:
        if(suit_value[0]!="Wild Card"):
            self.players[self.current_player][suit_value[0]].remove(suit_value[1])
        else:
            self.players[self.current_player][suit_value[1]].remove(suit_value[2])
     return meld
 




  def check_set_meld(self,value):
     """This Function is for creating a set"""
     meld={} #To Store the meld if the process is successful                      
     suit_card=[] #To store whatever cards are to be melded                
     
     for Suit in cards.keys():
        if value.upper() in self.players[self.current_player][Suit]:
          suit_card.append((Suit,value))
     
     if len(suit_card)==1:
        print("Can't Meld with only a Single Card!")
     
     
     elif len(suit_card)<3:
        print("You're trying to make a set but you don't have enough cards. \n\
Do you have a joker(WILD or PRINTED)??\nYour Collection:\n",self.players[self.current_player])
        
        if "y" in input("Got a WILD/PRINTED Joker??[y/n]\n>> ").lower():
           cards_avail=self.card_lookup("JOKER",self.wild_joker)
           if(len(cards_avail)<(3-len(suit_card))):
              print("You donot have enough Wild/Joker cards!!")
           else:
              meld=self.check_joker_rules(cards_avail,suit_card)
              print("SET CREATION SUCCESSFUL!!")#Because the set for that particular Turn has been created
              return self.remove_meld_cards_from_player_deck(meld) #What is left is to add that to the Set Pile     
              
     else:
        print("SET CREATION SUCCESSFUL!!")
        return self.remove_meld_cards_from_player_deck(suit_card)


  
  
  
  def create_seq_meld(self,value):
      seq=input("Please enter your sequence separated by spaces\n>> ").split(" ")
           
      if len(seq)<3:
        print("Not A valid Sequence, must have 3 or more Consecutive cards ")
      
      else:
        cards_to_add_to_sequence=[]
        for card in seq:
            
            if card in self.players[self.current_player][value]:
              cards_to_add_to_sequence.append(card)
              """The Reason We aren't directly adding the cards
              to the Sequence Pile is that if some card later 
              in the loop turns out to not exist with the User,
              then would have to put it back in their stacks,
              which would require more code :)"""
            
            else:
              cards_to_add_to_sequence=[]
              print("You don't have",(value,card),"Card with you!! Can't Meld")
              print("YOUR COLLECTION:",self.players[self.current_player]) #Displays the Collection
                                #To the user thus verifying the unavailability of the card
              return False
        for card in cards_to_add_to_sequence:
            self.sequence_pile[value].append(card)#Adding it to the Sequence
            self.players[self.current_player][value].remove(card)#Removing the Item from the Player's Collection
        return True    


  
  
  def merge_with_set(self):
     print("Existing Sets:\n",self.set_pile)
     print("Your Collection:\n",self.players[self.current_player])
     merge=input("Enter the Value of the Card that you want to merge:\n>> ").upper()
     cards_avail=self.card_lookup(merge)
     if not len(cards_avail)==0:
        print("Existing Sets:\n",self.set_pile)
        card_value=input("Enter the Position of the Set with which you want to merge...\n\
1. For the first set,2. For the second set and so on\n>> ")
        for card in cards_avail:
           if cards_avail[card]==self.set_pile[card_value-1][0][1]:
              self.set_pile[card_value-1].append((card,cards_avail[card]))
           elif cards_avail[card]=="JOKER":
              self.set_pile[card_value-1].append((card,cards_avail[card]))
           else:
              print("Card not Available in suit, MERGE ABORTED!!")
              return False
            #First try and make sure how the set pile looks like.
        return True
     return False


  
  
  
  
  def merge_with_seq(self):
     print("No matter where you merge, the Sequence should be ORDERED!")
     print("Order of cards in Rummy:\n",self.standard_seq)
     print("Existing Sequences:\n",self.sequence_pile)
     print("Your Collection:\n",self.players[self.current_player])
     suit=input("Enter the suit whose Sequence you want to merge with\n>> ").lower().capitalize()
     player_cards=input("Enter the SEQUENCE of cards to merge with that Seq(Separated By space)\n>> ").split(" ")
     for card in player_cards:
        if not(card==self.players[suit]):
           print("You donot have ",card," in that suit of your collection,aborting Merge")
           return False
     #After we know that all the cards are present, we need to make sure if they follow
     #the order
     seq_to_merge=self.sequence_pile[suit]
     if(player_cards[-1]<seq_to_merge):
        seq_to_merge=player_cards.append(seq_to_merge)
     elif(player_cards[0]>seq_to_merge):
        seq_to_merge=seq_to_merge.append(player_cards)
     else:
        print("Invalid Sequence Provided, Aborting Merge!")
        return False
     if "".join(seq_to_merge) in "".join(self.standard_seq):
        self.sequence_pile[suit]=seq_to_merge
        print("SEQUENCE MERGE SUCCESSFUL!")
        return True
     else:
        print("Incorrect ORDER of sequence provided, Aborting Merge")
        return False 
  
  
  
  
  
  
  def merge_with_existing_meld(self):
     print("Existing Sets:\n",self.set_pile)
     print("Exisiting Sequences:\n",self.sequence_pile)
     """Here we check first whether Existing Melds exist or not, if not, we simply return
     to the previous menu"""
     for i in self.sequence_pile.values():
        if len(i)==0 and len(self.set_pile)==0:
           print("No Existing Melds possible to Merge")
           return False
     while(True):
      meld_opt=input("Merge with Existing:\n1.Set\n2.Sequence\n3.Cancel Merge\n>> ").strip()
      if meld_opt=="1":
         return self.merge_with_set()
      elif meld_opt=="2":
         return self.merge_with_seq()
      elif meld_opt=="3":
         return False
      else:
         print("Please Enter a Valid choice")
     
      
  
  
  def meld(self):
     while(True):
        print("This is the list of Existing melds:\nExisting Sets:\n",self.set_pile,"\nExisting Sequences\n",self.sequence_pile)

        choice=input("Checking for possible melds : Enter your preference:\n\
'1': Set(3/4 Cards of the Same Value but different Suits)\n\
'2': Sequence(Consecutive Cards from the same Suit)\n\
'3': Merge with Existing Meld\n\
'4': Cancel Melding\n>> ")
        
        if('1' in choice):
           value=input("Enter the Value of the Card that you're trying to Meld\n>> ")
           try_meld=self.check_set_meld(value)

           if type(try_meld)==dict or type(try_meld)==list:
              self.set_pile.append(try_meld)
              return True
           
           else:
              print("SET CREATION UNSUCCESSFUL!!")
              return False
        
        
        elif('2' in choice):
           value=input("Enter the Suit that you have the sequence from\n>> ")
           seq_made=self.create_seq_meld(value)
           if(seq_made):
              print("SEQUENCE CREATION SUCCESSFULL!!")
           return seq_made
        
        elif("3" in choice):
            return self.merge_with_existing_meld()
        
        elif("4" in choice):
           return False
        
        else:
           print("Please Enter a Valid Choice")
     return True


  def draw_from_pile(self):
     if not self.pile_empty():
        print("Card available from the Discard Pile",self.last_card_on_the_pile)
        if "y" in input("Draw from the Pile??[y/n](Cannot be discarded in the same turn)\n>> "):
            pile[self.last_card_on_the_pile[0]].remove(self.last_card_on_the_pile[1])
            self.drawn_card=self.last_card_on_the_pile
        else:
            pile[self.last_card_on_the_pile[0]].append(self.last_card_on_the_pile[1])#Putting back the card data that was popped out 
            self.drawn_card=self.__get_Suit()
            print("The card drawn from deck is: ",self.drawn_card)
     else:
        self.drawn_card=self.__get_Suit()
        print("The Pile is empty, Card drawn from deck:",self.drawn_card)

  
  


  def trade_card(self):
     print("Trade a Card:\n Your Collection:",self.players[self.current_player])#Displaying the choices
                                                                                            #to the current player
     while(True):
        try:
            trade_card=input("Enter Suit and Card separated by space"+"\n0 to abort Trading\n>> ").split(" ")
            if(trade_card=="0"):
               return False
            print("Suit:",trade_card[0],"|| Card Recieved:",trade_card[1])
            self.players[self.current_player][trade_card[0]].remove(trade_card[1])
            pile[trade_card[0]].append(trade_card[1])
            self.last_card_on_the_pile=trade_card
            break
        except Exception as e:
           print("Please enter the Valid Suit and the Card separated by space")
     
     return True
     




  def play(self):
    if self.pile_empty():
            print("The Dealer places a card in the Middle.....\nAnd the Card is ",self.__get_Suit())
    while(self.winner is None):
        self.choice_made=False
        self.current_player=self.player_names[self.turn_count]
        print("It's Player "+self.current_player+"'s turn")
        self.show_cards()#Showing Cards to the Current Player
        self.draw_from_pile()
        #Whatever that drawn card is, adding that to the Player's Collection
        #As he can now also involve them in melding 
        self.players[self.current_player][self.drawn_card[0]].append(self.drawn_card[1])
        while(not self.choice_made):
            user_inp=input("1.Drop the Card\n2.Trade the Card\n3.Meld/Lay off\nYour Choice[1,2,3]??\n>> ")
            if "1" in user_inp:
                 # THE FUNCTIONALITY THAT THE CARD FROM THE PILE CANNOT BE RETURNED
                if(self.drawn_card==self.last_card_on_the_pile):
                  print("Cannot Reject a card drawn from the Pile!!")
                else:
                  print("Card rejected to the Pile")
                  pile[self.drawn_card[0]].append(self.drawn_card[1])#IF THE USER DOESN'T HOLD ON TO THE CARD, IT IS DISCARDED TO THE PILE AND 
                  self.players[self.current_player][self.drawn_card[0]].remove(self.drawn_card[1])
                  #Removing the card from the User's Collection
                  self.last_card_on_the_pile=self.drawn_card
                  self.choice_made=True        #NO EXCHANGE IS MADE
            
            elif "2" in user_inp:
                self.choice_made=self.trade_card()
                
            elif "3" in user_inp:
                self.choice_made=self.meld() #Depending upon whether the meld was
                 #cancelled/failed/successful, the choice would be completed
            else:
                print("Please enter a Valid Choice[1,2,3]")
        if(not self.current_player==self.player_names[-1]):
          self.turn_count+=1
        else:
          self.turn_count=0
        try:
          self.winner=self.player_names[self.check_Winner()]
        except:
          pass

     
          


  def draw(self,collection):
     picked_Card=""
     while(len(picked_Card)==0):
        try:
          print("Choices avail.",collection)
          picked_Card=input("Enter Suit and Card\n>> ").split(" ")
          print("Card Drawn:",picked_Card)
          collection[picked_Card[0]].append(picked_Card[1])

        except:
          print("Please enter the Valid Suit and the Card that exists in the Collection separated by a space")
                
  def game(self):
      print("LET THE ROMANCH OF RUMMY BEGIN!!")
      self.get_player_names()
      self.distribute()
      self.set_joker()
      self.play()
      

ok=RUMMY()
ok.game()
