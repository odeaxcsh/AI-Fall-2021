from typing import List, Tuple

class Card(object):
    def __init__(self, color, number) -> None:
        super().__init__()
        self.color = color
        self.number = number
    
    def __repr__(self) -> str:
        return f'{self.color}{self.number}'
    
    def __eq__(self, o: object) -> bool:
        if isinstance(o, Card):
            return self.color == o.color and self.number == o.number
        else: raise Exception(f'cannot compare object of type {type(o)} and Card')

    def __ge__(self, o: object):
        if isinstance(o, Card):
            return self.number <= o.number
        else: raise Exception(f'cannot compare object of type {type(o)} and Card')

    def __hash__(self) -> int:
        return super().__hash__()

Section = List[Card]
State = Tuple[Card]
States = List[State]
