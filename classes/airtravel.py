class Flight:
    #pass # pass is a noop
    def __init__(self, num, aircraft):
        if not num[:2].isalpha():
            raise ValueError("No airline code in '{}'".format(num))
        if not num[:2].isupper():
            raise ValueError("Invalid airline code in '{}'".format(num))
        if not (num[2:].isdigit() and int(num[2:]) <= 9999):
            raise ValueError("Invalid route number '{}'".format(num))
        self._num = num
        self._aircraft = aircraft

        rows, seats = self._aircraft.sPlan()
        self._seating = [None] + [{letter: None for letter in seats} for _ in rows]

    def number(self):
        return self._num
    # if we make f = Flight(), then the above method is callable as:
    # (1) f.number()
    # (2) Flight.number(f)
    def airline(self):
        return self._num[:2]

    def aircraft_mod(self):
        return self._aircraft.mod()

    def _parse_seat(self, seat):
        '''Parse a seat designator into a valid row and letter.

        Args:
            seat: A seat designator such as 12F

        Returns:
            A tuple containing an integer and a string for row and seat.
        '''
        rows, seat_letters = self._aircraft.sPlan()
        
        letter = seat[-1]
        if letter not in seat_letters:
            raise ValueError('Invalid seat letter {}'.format(letter))
        row_text = seat[:-1]
        try:
            row = int(row_text)
        except ValueError:
            raise ValueError('Invalid seat row {}'.format(row_text))
        
        if row not in rows:
            raise ValueError('Invalid row number {}'.format(row))

        return row, letter
    
    def allocate_seat(self, seat, passenger):
        '''Allocate a seat to a passenger.

        Args:
            seat: A seat designator such as '12C' or '21F'.
            passenger: The passenger name.
        
        Raises:
            ValueError: If the seat is unavailable.
        '''
        
        row, letter = self._parse_seat(seat)
        
        if self._seating[row][letter] is not None:
            raise ValueError('Seat {} is already occupied'.format(seat))

        self._seating[row][letter] = passenger
    
    def relocate_passenger(self, from_seat, to_seat):
        '''Relocate a passenger to a different seat.

        Args:
            from_seat: The existing seat designator for the passenger to be moved.

            to_seat: The new seat designator.
        '''
        from_row, from_letter = self._parse_seat(from_seat)
        if self._seating[from_row][from_letter] is None:
            raise ValueError("No passenger to relocate in seat {}".format(from_seat))
        to_row, to_letter = self._parse_seat(to_seat)
        if self._seating[to_row][to_letter] is not None:
            raise ValueError("Seat {} is already occupied".format(to_seat))
        
        self._seating[to_row][to_letter] = self._seating[from_row][from_letter]
        self._seating[from_row][from_letter] = None

    def num_available_seats(self):
        return sum(sum(1 for s in row.values() if s is None)
                    for row in self._seating
                    if row is not None)

class Aircraft:
    def __init__(self, reg, mod, rNum, SperR):
        self._reg = reg
        self._mod = mod
        self._rNum = rNum
        self._SperR = SperR
    
    def book(self):
        return self._reg
    
    def mod(self):
        return self._mod
    
    def sPlan(self):
        sCode = 'ABCDEFGHJKLM'
        return (range(1, self._rNum + 1), sCode[:self._SperR])

def make_flight():
    f = Flight('BA758', Aircraft('G-EUPT', 'Airbus A319', rNum=22, SperR=6))
    f.allocate_seat('12A', 'Guido van Rossum')
    f.allocate_seat('15F', 'Bjarne Stroustrup')
    f.allocate_seat('15E', 'Anders Heylsberg')
    f.allocate_seat('1C', 'John McCarthy')
    f.allocate_seat('1D', 'Richard Hickey')
    return f