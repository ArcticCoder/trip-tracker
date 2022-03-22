import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()
        self.kortti = Maksukortti(1000)

    # ALUSTUS
    def test_luokka_alustettu_oikein(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    # KATEISOSTO
    def test_edullinen_kateinen_riittava_maksu(self):
        vaihto = self.kassapaate.syo_edullisesti_kateisella(250)
        self.assertEqual(vaihto, 10)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100240)
        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_edullinen_kateinen_riittamaton_maksu(self):
        vaihto = self.kassapaate.syo_edullisesti_kateisella(230)
        self.assertEqual(vaihto, 230)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_maukas_kateinen_riittava_maksu(self):
        vaihto = self.kassapaate.syo_maukkaasti_kateisella(410)
        self.assertEqual(vaihto, 10)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100400)
        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_maukas_kateinen_riittamaton_maksu(self):
        vaihto = self.kassapaate.syo_maukkaasti_kateisella(390)
        self.assertEqual(vaihto, 390)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    # KORTTIOSTO
    def test_edullinen_kortti_riittava_saldo(self):
        onnistui = self.kassapaate.syo_edullisesti_kortilla(self.kortti)
        self.assertTrue(onnistui)
        self.assertEqual(str(self.kortti), "saldo: 7.6")
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_edullinen_kortti_riittamaton_saldo(self):
        self.kortti.ota_rahaa(800)
        onnistui = self.kassapaate.syo_edullisesti_kortilla(self.kortti)
        self.assertFalse(onnistui)
        self.assertEqual(str(self.kortti), "saldo: 2.0")
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_maukas_kortti_riittava_saldo(self):
        onnistui = self.kassapaate.syo_maukkaasti_kortilla(self.kortti)
        self.assertTrue(onnistui)
        self.assertEqual(str(self.kortti), "saldo: 6.0")
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_maukas_kortti_riittamaton_saldo(self):
        self.kortti.ota_rahaa(800)
        onnistui = self.kassapaate.syo_maukkaasti_kortilla(self.kortti)
        self.assertFalse(onnistui)
        self.assertEqual(str(self.kortti), "saldo: 2.0")
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    # RAHAN LATAAMINEN
    def test_rahan_lataaminen_onnistuneesti(self):
        self.kassapaate.lataa_rahaa_kortille(self.kortti, 1000)
        self.assertEqual(str(self.kortti), "saldo: 20.0")
        self.assertEqual(self.kassapaate.kassassa_rahaa, 101000)

    def test_rahan_lataaminen_negatiivisella_arvolla(self):
        self.kassapaate.lataa_rahaa_kortille(self.kortti, -1000)
        self.assertEqual(str(self.kortti), "saldo: 10.0")
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
