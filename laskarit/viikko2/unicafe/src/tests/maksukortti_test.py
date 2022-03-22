import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(1000)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)

    def test_saldo_alussa_oikein(self):
        self.assertEqual(str(self.maksukortti), "saldo: 10.0")

    def test_rahan_lataaminen_kasvattaa_saldoa_oikein(self):
        self.maksukortti.lataa_rahaa(100)
        self.assertEqual(str(self.maksukortti), "saldo: 11.0")

    def test_rahan_ottaminen_kun_raha_riittaa(self):
        self.assertTrue(self.maksukortti.ota_rahaa(900))
        self.assertEqual(str(self.maksukortti), "saldo: 1.0")

    def test_rahan_ottaminen_kun_raha_ei_riita(self):
        self.assertFalse(self.maksukortti.ota_rahaa(1100))
        self.assertEqual(str(self.maksukortti), "saldo: 10.0")
