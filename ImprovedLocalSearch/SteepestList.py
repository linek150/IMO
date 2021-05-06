from . SLSLStructs import * 
import numpy as np
NO=0
YES=1
MIGHT_BE=2
class Steepest_LS_List:
    def __init__(self,cycs_lists,dist_m):
        self.dist_m=dist_m
        self.cycs=[]
        for cyc_no,cyc in enumerate(cycs_lists):
            self.cycs.append(Cycle(cyc, cyc_no))
        self.move_list=None
        self.init_move_list()
        self.prev_move=None
    def get_poss_imp_moves(self,v,move_type=None):
        moves=[]
        if move_type==IN or move_type==None:
            for sec_v in self.cycs[v.cyc_no].vertecies:
                if sec_v is v.prev or sec_v is v.next: continue
                move=self.get_move(v,sec_v)
                if move.delta<0:
                    moves.append(move)
        if move_type==OUT or move_type==None:
            for cyc in self.cycs:
                if cyc.cyc_no!=v.cyc_no:
                    for sec_v in cyc.vertecies:
                        move = self.get_move(v,sec_v)
                        if move.delta<0:
                            moves.append(move)
        return moves       
    def dist_to_neigh(self,v1,v2=None):
        d_m=self.dist_m
        if v2==None:
            return d_m[v1.get_abs(),v1.next.get_abs()]+d_m[v1.get_abs(),v1.prev.get_abs()]
        else:
            return d_m[v1.get_abs(),v2.next.get_abs()]+d_m[v1.get_abs(),v2.prev.get_abs()]
    def dist_to_prev(self,v):
        d_m=self.dist_m
        return d_m[v.get_abs(),v.prev.get_abs()] 
    def get_delta(self,v1,v2):
        d_m=self.dist_m
        if v1.cyc_no!=v2.cyc_no:
            prev_dist=self.dist_to_neigh(v1)+self.dist_to_neigh(v2)
            new_dist=self.dist_to_neigh(v1,v2)+self.dist_to_neigh(v2,v1)
        else:
            if v1==v2 or (v1.cyc_idx+1)%len(self.cycs[v1.cyc_no])==v2.cyc_idx  or (v2.cyc_idx+1)%len(self.cycs[v2.cyc_no])==v1.cyc_idx:
                return 0
            prev_dist=self.dist_to_prev(v1)+self.dist_to_prev(v2)
            new_dist=d_m[v1.get_abs(),v2.get_abs()]+d_m[v1.prev.get_abs(),v2.prev.get_abs()]
        return new_dist-prev_dist
    def get_move(self,v1,v2):
        delta=self.get_delta(v1,v2)
        return Move(v1,v2,delta)
    def init_move_list(self):
        self.move_list=[]
        for cyc in self.cycs:
            for v in cyc.vertecies:
                moves=self.get_poss_imp_moves(v)
                self.move_list+=moves
    def update_moves_list(self): 
        if self.prev_move !=None:
            for v in self.prev_move.mod_vertecies:
                moves=self.get_poss_imp_moves(v)
                self.move_list+=moves
        return
    def is_valid(self,move):
        valid=None
        if move.type==IN:
            state=move.edges_state()
            if state==CORRECT:
                valid=YES
            elif state==BOTH_REVERSED:
                move.validate()
                valid=YES
            elif state==ONE_REVERSED:
                valid=MIGHT_BE
            elif state==NOT_EXIST:
                valid=NO
        elif move.type==OUT:
            state=move.exact_same_neigh()
            if state==CORRECT:
                valid=YES
            elif state==BOTH_REVERSED or state==ONE_REVERSED:
                move.validate()
                valid=YES
            elif state==NOT_EXIST:
                valid=NO
        assert valid!=None
        return valid
    def remove_moves(self,increasing_idxs):
        while increasing_idxs:
            idx=increasing_idxs.pop()
            #print("Dluigosc, idx: ",len(self.move_list),",",idx)
            self.move_list.pop(idx)
    def make_best_move(self):
        imp=False
        move_list=self.move_list
        move_list.sort(key=lambda x:x.delta)#the smaller the better
        idxs_to_remove=[]
        for idx,move in enumerate(move_list):
            valid=self.is_valid(move)
            if valid==YES:
                move.apply(len(self.cycs[move.v1.cyc_no]))
                self.prev_move=move
                idxs_to_remove.append(idx)
                imp=True
            elif valid==MIGHT_BE:
                continue
            elif valid==NO:
                idxs_to_remove.append(idx)
            if imp==True:
                break
        self.remove_moves(idxs_to_remove)
        return imp
    
    def get_cycs(self):
        cycs=[]
        found=[False,False]
        break_=False
        for cyc in self.cycs:
            for v in cyc.vertecies:
                if found[v.cyc_no]==False:
                    found[v.cyc_no]=True
                    cycs.append(v.get_cyc_next(v))
                if np.all(found):
                    break_=True
                    break
            if break_:break
        return cycs
    def get_cycs_idxs(self):
        cycs=[]
        found=[False,False]
        break_=False
        for cyc in self.cycs:
            for v in cyc.vertecies:
                if found[v.cyc_no]==False:
                    found[v.cyc_no]=True
                    cycs.append(v.get_cyc_idxs(v))
                if np.all(found):
                    break_=True
                    break
            if break_:break
        return cycs
    def try_to_improve(self):
        #cycs=self.get_cycs()
        #cycs_idxs=self.get_cycs_idxs()
        #print("CYKLE",cycs[0],cycs[1])
        #print("INDEKSY:",cycs_idxs[0],cycs_idxs[1],len(np.unique(cycs_idxs[0])),len(np.unique(cycs_idxs[1])))
        improved=False
        self.update_moves_list()
        improved=self.make_best_move()
        l1=len([a for a in self.cycs[0].vertecies if a.cyc_no==0])+len([a for a in self.cycs[1].vertecies if a.cyc_no==0])
        l2=len([a for a in self.cycs[0].vertecies if a.cyc_no==1])+len([a for a in self.cycs[1].vertecies if a.cyc_no==1])
        assert l1==l2
        #print("Liczba wierzchołków w cyklu 0:",wi)
        return improved
def ls_steepest_list(cyc1,cyc2,dist_m):
    lsl=Steepest_LS_List([cyc1,cyc2], dist_m)
    improved=True
    i=0
    while improved:
        improved=lsl.try_to_improve()
        i+=1
    return lsl.get_cycs()