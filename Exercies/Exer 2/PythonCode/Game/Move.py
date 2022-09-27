from typing import List


from typing import List

class Move(object):
    def __init__(self, frm: int, to: int) -> None:
        super().__init__()
        self.o = frm 
        self.d = to
    
    def __eq__(self, o: object) -> bool:
        if isinstance(o, Move):
            return o.o == self.o and o.d == self.d
    
    def __repr__(self) -> str:
        return f'({self.o} -> {self.d})'
    
Moves = List[Move]