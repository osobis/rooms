from unittest import mock, TestCase
from rooms.main import RoomNumberCalculator


class ReservationValidatorTest(TestCase):

    def setUp(self):
        self.room_num_cal = RoomNumberCalculator()

    def test_success(self):
        reservation_list = [(1, 2), (3, 5), (0, 2), (10, 23)]
        result = self.room_num_cal.is_reservations_list_valid(reservation_list)
        self.assertTrue(result)

    def test_not_tuple(self):
        reservation_list = [(1, 2), [3, 5], (0, 2), (10, 23)]
        result = self.room_num_cal.is_reservations_list_valid(reservation_list)
        self.assertFalse(result)

    def test_not_int(self):
        reservation_list = [(1, 'a'), (3, 5), (0, 2), (10, 23)]
        result = self.room_num_cal.is_reservations_list_valid(reservation_list)
        self.assertFalse(result)

    def test_out_of_range(self):
        reservation_list = [(1, 2), (3, 5), (0, 24), (10, 23)]
        result = self.room_num_cal.is_reservations_list_valid(reservation_list)
        self.assertFalse(result)


class RoomNumberCalculatorTest(TestCase):

    def setUp(self):
        self.room_num_cal = RoomNumberCalculator()

    def test_unfold_reservations(self):
        result = self.room_num_cal._unfold_hours([(0,1), (1,3)])
        self.assertEqual([0, 1, 1, 2, 3], result)

        result = self.room_num_cal._unfold_hours([(0, 1)])
        self.assertEqual([0, 1], result)

        result = self.room_num_cal._unfold_hours([(3, 3)])
        self.assertEqual([3], result)

        result = self.room_num_cal._unfold_hours([(1,1), (3, 3)])
        self.assertEqual([1, 3], result)

        result = self.room_num_cal._unfold_hours([(1, 1), (1, 1), (1, 1)])
        self.assertEqual([1, 1, 1], result)

        result = self.room_num_cal._unfold_hours([(1, 1), (1, 6)])
        self.assertEqual([1, 1, 2, 3, 4, 5, 6], result)

    def test_get_rooms_num_from_exercise(self):
        reservations = [
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

        expected = 4  # as in the task
        result = self.room_num_cal.get_rooms_num(reservations)
        self.assertEqual(result, expected)

    def test_get_rooms_num_one_reservation_one_room(self):
        reservations = [
            (3, 5)
        ]
        result = self.room_num_cal.get_rooms_num(reservations)
        self.assertEqual(result, 1)

        reservations = [
            (8, 8)
        ]

        result = self.room_num_cal.get_rooms_num(reservations)
        self.assertEqual(result, 1)

    def test_get_rooms_num_two_reservations_one_room(self):
        reservations = [
            (3, 5),
            (6, 10)
        ]

        result = self.room_num_cal.get_rooms_num(reservations)
        self.assertEqual(result, 1)

        reservations = [
            (3, 3),
            (6, 6)
        ]
        result = self.room_num_cal.get_rooms_num(reservations)
        self.assertEqual(result, 1)

    def test_get_rooms_num_two_reservations_two_rooms(self):
        reservations = [
            (5, 10),
            (3, 5)
        ]

        result = self.room_num_cal.get_rooms_num(reservations)
        self.assertEqual(result, 2)

        reservations = [
            (7, 7),
            (7, 7)
        ]

        result = self.room_num_cal.get_rooms_num(reservations)
        self.assertEqual(result, 2)

    def test_get_rooms_no_reservations_no_rooms(self):
        reservations = [
        ]

        result = self.room_num_cal.get_rooms_num(reservations)
        self.assertEqual(result, 0)

    def test_get_rooms_all_day_reservation(self):
        reservations = [
            (0, 23),
            (0, 23)
        ]

        result = self.room_num_cal.get_rooms_num(reservations)
        self.assertEqual(result, 2)

        reservations = [
            (0, 23),
            (4, 10),
            (11, 23)
        ]

        result = self.room_num_cal.get_rooms_num(reservations)
        self.assertEqual(result, 2)

        reservations = [
            (0, 23),
            (4, 10),
            (10, 23)
        ]

        result = self.room_num_cal.get_rooms_num(reservations)
        self.assertEqual(result, 3)

    def test_get_rooms_edge_reservations(self):
        reservations = [
            (0, 0),
            (23, 23)
        ]

        result = self.room_num_cal.get_rooms_num(reservations)
        self.assertEqual(result, 1)

    def test_get_rooms_invalid_reservations(self):
        self.room_num_cal.is_reservations_list_valid.return_value = False

        with self.assertRaises(ValueError) as err:
            result = self.room_num_cal.get_rooms_num(['dummy invalid list'])
        self.assertTrue("Invalid reservation list" in str(err.exception))
