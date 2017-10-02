"""
Program to calculate the minimum number of rooms required to accommodate all possible reservations made
for a given day
Example:

Assuming we have the following list of reservations:
[
    (3, 5),    # reservation A
    (2, 9),    # reservation B
    (0, 4),    # reservation C
    (0, 2),    # reservation D
    (8, 8),    # reservation E
    (3, 7),    # reservation F
    (6, 9),    # reservation G
    (5, 6),    # reservation H
    (7, 9),    # reservation I
    (1, 2)     # reservation J
]

Then we could find a compact arrangement for these reservations in the following form

Hour of day  |  0  1  2  3  4  5  6  7  8  9
---------------------------------------------
Room #1      |  D  D  D  A  A  A  G  G  G  G
Room #2      |  C  C  C  C  C  H  H  I  I  I
Room #3      |     J  J  F  F  F  F  F  E
Room #4      |        B  B  B  B  B  B  B  B

were the letters A - J mark a time-slot occupied by the corresponding reservation in the input list.

With this arrangement we would be able to handle all reservations with only 4 meeting rooms.
"""
import logging

LOG_FORMAT = '%(asctime)s %(levelname)s [%(name)s] %(message)s'
logging.basicConfig(level=getattr(logging, 'DEBUG'), format=LOG_FORMAT, )


class RoomNumberCalculator(object):
    """
    Calculates the minimum number of rooms required to accommodate all possible reservations for a given day
    """
    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)

    @staticmethod
    def is_reservations_list_valid(reservations):
        """
        Validate reservations list
        :param reservations: (list of tuples)
        :return: True on success
        """
        for reservation in reservations:
            if not isinstance(reservation, tuple):
                return False
            if len(reservation) != 2:
                return False
            for item in reservation:
                if not isinstance(item, int) or item not in range(0, 24):
                    return False
        return True

    @staticmethod
    def _unfold_hours(reservations):
        """
        Unfold hours in each reservation so that we get a flat list of hours used by each reservations
        Example:
        [(0, 1), (1, 3)]  unfolds to [0, 1, 1, 2, 3]
        [(0, 1)] unfolds to [0, 1]
        [(1, 1), (3, 3)] unfolds to [1, 3]
        :param: (list of tuples) list of reservations
        :return: (list of lists) list of unfolded hours in the reservation list
        """
        unfolded_hours = []
        for reservation in reservations:
            unfolded_hours.extend(range(reservation[0], reservation[-1] + 1))

        return unfolded_hours

    def get_rooms_num(self, reservations):
        """
        Get min number of rooms
        Having unfolded hours in a list, multiple occurrence of the same digit indicates a need for a new room
        So, if we have [0, 1, 1, 2, 3] sequence, we would need 2 rooms, because 2 meetings both happen  at 1 o'clock
        If we have [0, 1, 1, 3, 4, 4, 4, 5] we would need 3 rooms, because at 4 we have 3 meetings at the same time
        :param reservations: (list of tuples), i.e.: [(3, 5), (2, 9), ...]
        :return: (int) number of rooms
        """
        if not self.is_reservations_list_valid(reservations):
            raise ValueError('Invalid reservation list')

        self.log.debug('Reservations: %r', reservations)
        unfolded_hours = self._unfold_hours(reservations)

        self.log.debug('Unfolded hours: %r', unfolded_hours)
        return max([unfolded_hours.count(i) for i in range(0, 24)])


def main():

    room_num_calculator = RoomNumberCalculator()

    reservation_list = [
        (3, 5),    # reservation A
        (2, 9),    # reservation B
        (0, 4),    # reservation C
        (0, 2),    # reservation D
        (8, 8),    # reservation E
        (3, 7),    # reservation F
        (6, 9),    # reservation G
        (5, 6),    # reservation H
        (7, 9),    # reservation I
        (1, 2)     # reservation J
    ]

    result = room_num_calculator.get_rooms_num(reservation_list)
    print ("Number of rooms needed: {}".format(result))

    print ('-'*40)
    reservation_list = [
        (3, 5),  # reservation A
        (2, 9),  # reservation B

    ]
    result = room_num_calculator.get_rooms_num(reservation_list)
    print("Number of rooms needed: {}".format(result))

    print('-' * 40)
    reservation_list = [
        (1, 4),  # reservation A
        (1, 5),  # reservation B

    ]
    result = room_num_calculator.get_rooms_num(reservation_list)
    print("Number of rooms needed: {}".format(result))

    print('-' * 40)
    reservation_list = [
        (1, 4),  # reservation A
        (5, 5),  # reservation B

    ]
    result = room_num_calculator.get_rooms_num(reservation_list)
    print("Number of rooms needed: {}".format(result))

    print('-' * 40)
    reservation_list = [
        (0, 0),  # reservation A

    ]
    result = room_num_calculator.get_rooms_num(reservation_list)
    print("Number of rooms needed: {}".format(result))

    print('-' * 40)
    reservation_list = [

    ]
    result = room_num_calculator.get_rooms_num(reservation_list)
    print("Number of rooms needed: {}".format(result))


# added main to be able to run the application from the command line
main()
