class Flight:
    #pass # pass is a noop
    def __init__(self, flight_number, aircraft):
        if not flight_number[:2].isalpha():
            raise ValueError("No airline code in '{}'".format(flight_number))
        if not flight_number[:2].isupper():
            raise ValueError("Invalid airline code in '{}'".format(flight_number))
        if not (flight_number[2:].isdigit() and int(flight_number[2:]) <= 9999):
            raise ValueError("Invalid route number '{}'".format(flight_number))
        self._flight_number = flight_number
        self._aircraft = aircraft

        rows, seats = self._aircraft.seating_plan()
        self._seating = [None] + [{letter: None for letter in seats} for _ in rows]

    def number(self):
        return self._flight_number
    # if we make f = Flight(), then the above method is callable as:
    # (1) f.number()
    # (2) Flight.number(f)
    def airline(self):
        return self._flight_number[:2]

    def aircraft_mod(self):
        return self._aircraft.model()

    def _parse_seat(self, seat):
        '''Parse a seat designator into a valid row and letter.

        Args:
            seat: A seat designator such as 12F

        Returns:
            A tuple containing an integer and a string for row and seat.
        '''
        rows, seat_letters = self._aircraft.seating_plan()
        
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
    
    def locate_passenger(self, passenger):
        seat_counter = 0
        row_counter = 0
        for row in self._seating:
            if row is not None:
              seat_counter += len(row)
        for row in self._seating:
            row_counter += 1
            if row is not None:
              for key in row:
                if row[key] == passenger:
                    return str(row_counter) + key 
                else:
                    seat_counter-= 1
                    if seat_counter == 0:
                        raise ValueError('{} was not found on this plane'.format(passenger))

    def make_boarding_cards(self, card_printer):
        for passenger, seat in sorted(self._passenger_seats()):
            card_printer(passenger, seat, self.number(), self.aircraft_mod())
    
    def _passenger_seats(self):
        '''An iterable series of passenger seating allocations.'''
        rows, seat_letters = self._aircraft.seating_plan()
        for row in rows:
            for letter in seat_letters:
                passenger = self._seating[row][letter]
                if passenger is not None:
                    yield (passenger, '{}{}'.format(row, letter))
    
    def methods(self):
        print('(1) self.__init__(num, aircraft)')
        print('(2) self.number() ')
        print('(3) self.airline() ')
        print('(4) self.aircraft_mod() ')
        print('(5) self._parse_seat(seat) ')
        print('(6) self.allocate_seat(seat, passenger) ')
        print('(7) self.relocate_passenger(from_seat, to_seat) ')
        print('(8) self.num_available_seats() ')
        print('(8) self.locate_passenger(passenger) ')

class Aircraft:

    def __init__(self, registration):
        self._registration = registration
    
    def book(self):
        return self._registration
        
    def num_seats(self):
        rows, row_seats = self.seating_plan()
        return len(rows) * len(row_seats)


class AirbusA319(Aircraft):
    
    def model(self):
        return 'Airbus A319'
    
    def seating_plan(self):
        return range(1, 23), 'ABCDEF'
        

class Boeing777(Aircraft):
    
    def model(self):
        return 'Boeing 777'
    
    def seating_plan(self):
        return range(1, 56), 'ABCDEFGHJ'


def make_flight():
    f = Flight('BA758', Aircraft('G-EUPT', 'Airbus A319', row_number=22, SperR=6))
    f.allocate_seat('12A', 'Guido van Rossum')
    f.allocate_seat('15F', 'Bjarne Stroustrup')
    f.allocate_seat('15E', 'Anders Heylsberg')
    f.allocate_seat('1C', 'John McCarthy')
    f.allocate_seat('1D', 'Richard Hickey')
    return f

def console_card_printer(passenger, seat, flight_number, aircraft):
    output = "| Name: {0}"     \
             "  Flight: {1}"   \
             "  Seat: {2}"     \
             "  Aircraft: {3}" \
             " |".format(passenger, flight_number, seat, aircraft)
    banner = '+' + '-' * (len(output) - 2) + '+'
    border = '|' + ' ' * (len(output) - 2) + '|'
    lines = [banner, border, output, border, banner]
    card = '\n'.join(lines)
    print(card)
    print()