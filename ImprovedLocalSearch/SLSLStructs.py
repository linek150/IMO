import copy 
IN=0
OUT=1
CORRECT=0
BOTH_REVERSED=1
ONE_REVERSED=2
NOT_EXIST=3


class Vertex:
    counter=0
    def __init__(self,cyc_no,abs_idx,cyc_idx):
        Vertex.counter+=1
        self.cyc_no=cyc_no
        self.__abs_idx=abs_idx
        self.cyc_idx=cyc_idx
        self.next=None
        self.prev=None
    def __str__(self):
        return "cyc_no "+str(self.cyc_no) +" MID: ("+str(self.cyc_idx)+", "+str(self.__abs_idx)+") PREV: ("+str(self.prev.cyc_idx)+","+str(self.prev.get_abs())\
            +") NEXT : ("+str(self.next.cyc_idx)+","+str(self.next.get_abs())+")"

    def set_next(self,vertex):
        self.next=vertex
    def set_prev(self,vertex):
        self.prev=vertex
    def get_abs(self):
        return self.__abs_idx
    def reverse_neigh(self):
        buff=self.next
        self.next=self.prev
        self.prev=buff
    def update_prev_rec(self,stop_v,cyc_len):
       #print(self)
        curr_prev=self.prev
        curr_prev.cyc_idx=(self.cyc_idx+1)%cyc_len
        if curr_prev is stop_v:
            #ja staje się poprzednikiem mojego poprzednika
            curr_prev.prev=self
            #mój poprzednik staje się moim następnikiem
            self.next=curr_prev
            return
        else:
            curr_prev.update_prev_rec(stop_v,cyc_len)
            #ja staje się poprzednikiem mojego poprzednika
            curr_prev.prev=self
            #mój poprzednik staje się moim następnikiem
            self.next=curr_prev
    def get_cyc_next(self,stop_v):
        if self.next is stop_v:
            return [self.get_abs()]
        else:
            ret_val=[self.get_abs()]
            ret_val.extend(self.next.get_cyc_next(stop_v))
            return ret_val
    def get_cyc_prev(self,stop_v,print_=False):
        if print_:print(self)
        if self.prev==stop_v:
            return [self.get_abs()]
        else:
            ret_val=self.prev.get_cyc_prev(stop_v,print_)
            ret_val.append(self.get_abs())
            return ret_val

    def get_cyc_idxs(self,stop_v):
        if self.next is stop_v:
            return [self.cyc_idx]
        else:
            ret_val=[self.cyc_idx]
            ret_val.extend(self.next.get_cyc_idxs(stop_v))
            return ret_val
    def update_neigh(self):
        self.next.prev=self
        self.prev.next=self
    @staticmethod
    def copy_atr_from_to(v_from,v_to):
        v_to.next=v_from.next
        v_to.prev=v_from.prev
        v_to.cyc_no=v_from.cyc_no
        v_to.cyc_idx=v_from.cyc_idx
    def __copy__(self):
        copy_ = type(self)(self.cyc_no,None,self.cyc_idx)
        copy_.__dict__.update(self.__dict__)
        copy_.set_next(self.next)
        copy_.set_prev(self.prev)
        return copy_

    def __del__(self):
        Vertex.counter-=1
class Cycle:
    def __init__(self,cyc,cyc_no):
        self.cyc_no=cyc_no
        self.vertecies=[]
        #create all vertecies add their predecesors
        for cyc_idx,abs_idx in enumerate(cyc):
            v=Vertex(cyc_no, abs_idx, cyc_idx)
            self.vertecies.append(v)
            if cyc_idx!=0:
                prev_v=self.vertecies[cyc_idx-1]
                self.vertecies[cyc_idx].set_prev(prev_v)
        last_v=self.vertecies[-1]
        self.vertecies[0].set_prev(last_v)
        #add successors
        for cyc_idx,abs_idx in enumerate(cyc):
            next_v=self.vertecies[(cyc_idx+1)%len(cyc)]
            self.vertecies[cyc_idx].set_next(next_v)
    def __len__(self):
        return len(self.vertecies)
class Move:
    def __init__(self,v1,v2,delta):
        #to ensure that v1 has lower idx in case of IN type 
        self.type=IN if v1.cyc_no==v2.cyc_no else OUT
        self.v1,self.v2=(v1,v2) if v1.cyc_idx<=v2.cyc_idx else (v2,v1)
        self.__frozen_v1=copy.copy(self.v1)
        self.__frozen_v2=copy.copy(self.v2)
        self.delta=delta
        self.reverse_neigh_when_apply=False
        self.mod_vertecies=None
    def __str__(self):
        return "Delta: "+str(self.delta)+" TYPE :"+self.typeelse +" \nv1: "+str(self.v1)+"\nv1_frozen "+str(self.__frozen_v1)\
            +"\nv2 :"+str(self.v2)+"\nv2_frozen "+str(self.__frozen_v2)

    def apply(self,cyc_len):
        v1=self.v1
        v2=self.v2
        self.mod_vertecies=[]
        self.mod_vertecies.extend([v1,v1.prev,v2,v2.prev])
        if self.type==IN:
            if v1.cyc_no != v2.cyc_no:print(self)
            assert v1.cyc_no==v2.cyc_no
            #if v1.next is v2 or v1.prev is v2: print("WYKONYWANO :",id(self))
            assert not(v1.next is v2) and not(v1.prev is v2)
            old_v1_prev=v1.prev
            old_v2_prev=v2.prev
            old_v1=v1
            old_v2=v2
            # print("Fragment od v1 do v2.prev na nextach:",v1.prev.get_cyc_next(v2.next))
            # print("Fragemtn od v1 do v2.prev na prev:   ",v2.get_cyc_prev(v1.prev.prev))
            # print("Indeksy: ", v1.prev.get_cyc_idxs(v1.prev))
            # print("\nv1.prev :", v1.prev)
            # print("v1 :",v1)
            # print("v2.prev:", v2.prev)
            # print("v2 :", v2)
            
            #print("REKURENCJA")
            v2.prev.cyc_idx=(v1.prev.cyc_idx+1)%cyc_len
            v2.prev.update_prev_rec(v1,cyc_len)
            old_v2_prev.prev=old_v1_prev
            old_v1_prev.next=old_v2_prev
            v1.next=v2
            v2.prev=v1
            # print("v1.prev :", v1.prev)
            # print("v1 :",v1)
            # print("v2.prev:", v2.prev)
            # print("v2 :", v2)
            # print("\n")
            # print("Indeksy: ", old_v1_prev.get_cyc_idxs(old_v1_prev))
            # print("Od old_v1_prev do v2 na prev:",v2.get_cyc_prev(old_v1_prev.prev))
            # print("Od old_v1_pre do v2  na next:",old_v1_prev.get_cyc_next(v2.next))
            assert len(v2.get_cyc_idxs(v2))==cyc_len
            assert v2.cyc_idx==(v1.cyc_idx+1)%cyc_len
        else:
            self.mod_vertecies.extend([v1.next,v2.next])
            v_buff=Vertex(cyc_no=None, abs_idx=None, cyc_idx=None)
            Vertex.copy_atr_from_to(v1, v_buff)
            Vertex.copy_atr_from_to(v2, v1)
            Vertex.copy_atr_from_to(v_buff, v2)
            v1.update_neigh()
            v2.update_neigh()
    def same_cyc_no(self):
        return self.v1.cyc_no == self.__frozen_v1.cyc_no\
             and self.v2.cyc_no == self.__frozen_v2.cyc_no


    def edges_state(self):
        v1=self.v1
        v2=self.v2
        
        frozen_v1=self.__frozen_v1
        frozen_v2=self.__frozen_v2
        if v1 is v2 or v1.next is v2 or v1.prev is v2 or\
             not(self.same_cyc_no()):
            return NOT_EXIST
        first_correct=v1.prev is frozen_v1.prev
        sec_correct=v2.prev is frozen_v2.prev
        if first_correct and sec_correct:
            state=CORRECT
        elif v1.next is frozen_v1.prev and v2.next is frozen_v2.prev:
            state=BOTH_REVERSED
        elif (first_correct and v2.next is frozen_v2.prev) or (sec_correct and v1.next is frozen_v1.prev):
            state=ONE_REVERSED
        else:
            state=NOT_EXIST
        return state
    def validate(self):
        if self.type==IN:
            assert not(self.v1.next is self.v2) and not(self.v1.prev is self.v2)
            if self.v1.cyc_idx<self.v2.cyc_idx:
                self.v1=self.v1.prev
                self.v2=self.v2.prev
            else:
                v1_buff=self.v1
                self.v1=self.v2.prev
                self.v2=v1_buff.prev
        elif self.type==OUT:
            pass
            #if self.__frozen_v1.next==self.v1.prev:
            #    self.__frozen_v1.reverse_neigh()
            #if self.__frozen_v2.next==self.v2.prev:
            #    self.__frozen_v2.reverse_neigh()
        else: raise NotImplementedError()

    def exact_same_neigh(self):
        v1=self.v1
        v2=self.v2
        frozen_v1=self.__frozen_v1
        frozen_v2=self.__frozen_v2
        if v1.cyc_no==v2.cyc_no:
            return NOT_EXIST
        v1_ex_next=v1.next is frozen_v1.next
        v1_ex_prev=v1.prev is frozen_v1.prev
        v2_ex_next=v2.next is frozen_v2.next
        v2_ex_prev=v2.prev is frozen_v2.prev
        state=None
        if v1_ex_next and v1_ex_prev and v2_ex_prev and v2_ex_next:# full match
            state=CORRECT
        elif v1_ex_next or v1_ex_prev or v2_ex_prev or v2_ex_next:# not exist because only partial match
            state=NOT_EXIST
        elif v1.next is frozen_v1.prev and v1.prev is frozen_v1.next and v2.next is frozen_v2.prev and v2.prev is frozen_v2.next:
            state=BOTH_REVERSED
        elif (v1.next is frozen_v1.prev and v1.prev is frozen_v1.next and v2_ex_prev and v2_ex_next) or (v2.next is frozen_v2.prev and v2.prev is frozen_v2.next and v1_ex_prev and v1_ex_next):
            state=ONE_REVERSED
        else:
            state=NOT_EXIST
        return state