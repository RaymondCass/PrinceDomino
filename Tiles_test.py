import unittest
import random
from Tiles import Tile, Deck, Square
from Tiles import SQUARESET

class TestTile(unittest.TestCase):
    def test_get(self):
        """Testing the get methods for Tile Class"""
        s1, s2 = Square("wheat", 0), Square("forest", 1)
        t = Tile(s1,s2)
        self.assertEqual(str(t.get_square2()),"0wheat")
        self.assertEqual(str(t.get_square1()),"1forest")
        self.assertEqual(t.square2.get_terrain(),"wheat")
        self.assertEqual(t.square1.get_terrain(),"forest")
        self.assertEqual(t.square2.get_crowns(),0)
        self.assertEqual(t.square1.get_crowns(),1)
        self.assertEqual(t.get_direction(),"left")

    def test_create_invalid(self):
        """Testing that Tile class cannot accept invalid tile inputs"""
        self.assertRaises(AssertionError, Square, "gras", 1)
        self.assertRaises(AssertionError, Square, "grass", 3)
        sq = Square("grass", 1)
        self.assertRaises(ValueError, Tile, sq)

    def test_rotate(self):
        s1, s2 = Square("wheat", 0), Square("forest", 1)
        t = Tile(s1,s2)
        self.assertEqual(t.get_direction(),"left")
        t.rotate("clockwise")
        self.assertEqual(t.get_direction(),"up")
        t.rotate("counterclockwise")
        t.rotate("counterclockwise")
        self.assertEqual(t.get_direction(),"down")
        t.rotate("counterclockwise")
        self.assertEqual(t.get_direction(),"right")

    def test_print(self):
        """Testing that the print statement works"""
        s1, s2 = Square("wheat", 0), Square("forest", 0)
        t1 = Tile(s1,s2)
        self.assertEqual(str(t1), "[0wheat|0forest]")
        s1, s2 = Square("swamp", 2), Square("mine", 0)
        t2 = Tile(s1,s2)
        self.assertEqual(str(t2),"[2swamp|0mine]")

    def test_sort_squares(self):
        s1, s2 = Square("wheat", 0), Square("grass", 1)
        t1 = Tile(s1, s2)
        self.assertEqual(str(t1), "[1grass|0wheat]", "Crowns should be t1")
        s1, s2 = Square("forest", 0), Square("wheat", 0)
        t2 = Tile(s1, s2)
        self.assertEqual(str(t2), "[0wheat|0forest]", "wheat is before forest")

    def test_calculate_value(self):
        #mono-suit tiles, no crowns
        s1, s2= Square("grass", 0), Square("grass", 0)
        t1 = Tile(s1, s2)
        s3, s4 = Square("wheat", 0), Square("water", 0)
        t2 = Tile(s3, s4)

        self.assertGreater(t2.get_value(), t1.get_value(), "Mono-tiles are lowest")
        s5, s6 = Square("forest", 0), Square("forest", 0)
        t3 = Tile(s5, s6)
        self.assertGreater(t1.get_value(), t3.get_value(), "Mono-tiles are ordered")

        #crowns
        s7, s8 = Square("wheat", 1), Square("forest", 0)
        t4 = Tile(s7, s8)
        self.assertGreater(t4.get_value(), t1.get_value(), "Crowns are greater")
        s9, s10 = Square("swamp", 2), Square("forest", 0)
        t5 = Tile(s9, s10)
        s11, s12 = Square("mine", 3), Square("water", 0)
        t6 = Tile(s11, s12)
        self.assertGreater(t6.get_value(), t4.get_value(), "More crowns are greater")
        self.assertGreater(t6.get_value(), t5.get_value(), "More crowns are greater")
        s13, s14 = Square("swamp", 2), Square("water", 0)
        t7 = Tile(s13, s14)
        s15, s16 = Square("grass", 2), Square("swamp", 0)
        t8 = Tile(s15, s16)
        self.assertGreater(t7.get_value(), t5.get_value(), "Order within crowns works")
        self.assertGreater(t7.get_value(), t8.get_value(), "Order within crowns works")

        #same tile, same value
        s17, s18 = Square("grass", 0), Square("grass", 0)
        t9 = Tile(s17, s18)
        self.assertEqual(t1.get_value(), t9.get_value(), "Identical tile has same value")

        #random_check on standard tiles
        d = Deck(True)
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
        s13, s14 = Square("swamp", 2), Square("water", 0)
        t7 = Tile(s13, s14)
        s15, s16 = Square("grass", 2), Square("swamp", 0)
        t8 = Tile(s15, s16)
        d = Deck(deck = [t7, t8])
        s15, s16 = Square("grass", 2), Square("swamp", 0)
        t9 = Tile(s15, s16)
        s15, s16 = Square("grass", 2), Square("swamp", 1)
        t10 = Tile(s15, s16)

        self.assertTrue(d.contains(t7), "Passing a Deck (for testing purpose) to Deck")
        self.assertTrue(d.contains(t9), "Passing a Deck (for testing purpose) to Deck")
        self.assertFalse(d.contains(t10), "Passing a Deck (for testing purpose) to Deck")
    
    def test_standard_deck(self):
        d = Deck(True)
        s13, s14 = Square("wheat", 0), Square("wheat", 0)
        t7 = Tile(s13, s14, 1)
        s15, s16 = Square("wheat", 1), Square("grass", 0)
        t8 = Tile(s15, s16, 21)

        self.assertTrue(d.contains(t7), "Deck contains standard Tile #1")
        self.assertTrue(d.contains(t8), "Deck contains standard Tile #21")

    def test_random_deck(self):
        try:
            d = Deck(False)
        except:
            self.fail("Failed to create a random deck")
        #Test that there are 48 numbered cards (with no repeat numbers)
        self.assertEqual(sorted([c.get_value() for c in d.deck]), [n+1 for n in range(48)])

#suite = unittest.TestLoader().loadTestsFromTestCase(TestStringMethods)
#unittest.TextTestRunner(verbosity=2).run(suite)
