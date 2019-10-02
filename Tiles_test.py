import unittest
import random
from Tiles import Tile, Deck
from Tiles import SQUARESET

class TestTile(unittest.TestCase):
    def test_get(self):
        """Testiing the get methods for Tile Class"""
        t = Tile("0wheat","1forest")
        self.assertEqual(t.get_square2(),"0wheat")
        self.assertEqual(t.get_square1(),"1forest")
        self.assertEqual(t.get_suit2(),"wheat")
        self.assertEqual(t.get_suit1(),"forest")
        self.assertEqual(t.get_crowns2(),0)
        self.assertEqual(t.get_crowns1(),1)

    def test_create_invalid(self):
        """Testing that Tile class cannot accept invalid tile inputs"""
        self.assertRaises(AssertionError, Tile, "wheat", "0grass")
        self.assertRaises(AssertionError, Tile, "1wheat", "3grass")
        self.assertRaises(ValueError, Tile, "1wheat")

    def test_print(self):
        """Testing that the print statement works"""
        t1 = Tile("0wheat","0forest")
        self.assertEqual(str(t1), "[0wheat|0forest]")
        t2 = Tile("2swamp","0mine")
        self.assertEqual(str(t2),"[2swamp|0mine]")

    def test_sort_squares(self):
        t1 = Tile("0wheat", "1grass")
        self.assertEqual(str(t1), "[1grass|0wheat]", "Crowns should be t1")
        t2 = Tile("0forest","0wheat")
        self.assertEqual(str(t2), "[0wheat|0forest]", "wheat is before forest")

    def test_calculate_value(self):
        #mono-suit tiles, no crowns
        t1 = Tile("0grass","0grass")
        t2 = Tile("0wheat","0water")
        self.assertGreater(t2.get_value(), t1.get_value(), "Mono-tiles are lowest")
        t3 = Tile("0forest","0forest")
        self.assertGreater(t1.get_value(), t3.get_value(), "Mono-tiles are ordered")

        #crowns
        t4 = Tile("1wheat", "0forest")
        self.assertGreater(t4.get_value(), t1.get_value(), "Crowns are greater")
        t5 = Tile("2swamp","0forest")
        t6 = Tile("3mine","0water")
        self.assertGreater(t6.get_value(), t4.get_value(), "More growns are greater")
        self.assertGreater(t6.get_value(), t5.get_value(), "More crowns are greater")
        t7 = Tile("2swamp","0water")
        t8 = Tile("2grass","0swamp")
        self.assertGreater(t7.get_value(), t5.get_value(), "Order within crowns works")
        self.assertGreater(t7.get_value(), t8.get_value(), "Order within crowns works")

        #same tile, same value
        t9 = Tile("0grass","0grass")
        self.assertEqual(t1.get_value(), t9.get_value(), "Identical tile has same value")

        #random_check on standard tiles
        d = Deck(False)
        d.shuffle()
        for n in range(10):
            t1, t2 = d.deal_card(), d.deal_card()
            v1, v2 =  t1.get_value(), t2.get_value()
            if v1 >= v2:
                bigger, smaller = t1, t2
            else:
                bigger, smaller = t2, t1
            self.assertGreaterEqual(bigger.calculate_value(),
                                    smaller.calculate_value(),
                                    ("Random check number " + str(n) +
                                    "\ninputs:" + str(t1) + str(t2) + "\n"))


class TestDeck(unittest.TestCase):
    def test_test_deck(self):
        t4 = Tile("0wheat","0forest")
        t5 = Tile("2swamp","0mine")
        d = Deck(deck = [t4, t5])
        t6 = Tile("2swamp","0mine")
        t7 = Tile("2swamp","1mine")
        self.assertTrue(d.contains(t5), "Passing a Deck (for testing purpose) to Deck")
        self.assertTrue(d.contains(t6), "Passing a Deck (for testing purpose) to Deck")
        self.assertFalse(d.contains(t7), "Passing a Deck (for testing purpose) to Deck")
    
    def test_standard_deck(self):
        d = Deck(False)
        t1 = Tile("0wheat","0wheat",1)
        self.assertTrue(d.contains(t1), "Deck contains standard Tile #1")
        t2 = Tile("1wheat","0grass",21)
        self.assertTrue(d.contains(t2), "Deck contains standard Tile #21")
        t3 = Tile("0wheat","3mine",48)
        self.assertTrue(d.contains(t3), "Deck contains standard Tile #48")
        
#suite = unittest.TestLoader().loadTestsFromTestCase(TestStringMethods)
#unittest.TextTestRunner(verbosity=2).run(suite)
