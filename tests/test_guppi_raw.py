import unittest

from rao_keyvalue_property_mixin_classes.guppi_raw import GuppiRawProperties


class GuppiRawHeader(dict, GuppiRawProperties):
    pass


class TestGuppiRaw(unittest.TestCase):
    def test_blockshape(self):
        grh = GuppiRawHeader(
            NANTS=16,
            OBSNCHAN=16*32,
            NPOL=2,
            NBITS=8,
            BLOCSIZE=16*32*1024*2*2*8//8
        )

        blockshape = grh.blockshape
        assert blockshape[0] == grh["NANTS"]
        assert blockshape[1] == grh["OBSNCHAN"]//grh["NANTS"]
        assert blockshape[2] == 1024
        assert blockshape[3] == grh["NPOL"]

    def test_ant_chan_proxies(self):
        grh = GuppiRawHeader(
            NANTS=16,
            OBSNCHAN=16*32,
            OBSBW=32
        )

        assert grh.channel_bandwidth == 1
        grh.channel_bandwidth *= 2
        assert grh.channel_bandwidth == 2
        assert grh.observed_bandwidth == 64


    def test_ra_dec(self):
        ra = 8.34031194444
        dec = -3.1415926535
        grh = GuppiRawHeader(
            NANTS=16,
            OBSNCHAN=16*32,
            NPOL=2,
            NBITS=8,
            BLOCSIZE=16*32*1024*2*2*8//8,
            RA_STR=GuppiRawProperties.to_sexagesimal_str(ra),
            DEC_STR=GuppiRawProperties.to_sexagesimal_str(dec),
        )

        for i in range(3):
            # test str representation's accuracy to 14 characters
            assert str(grh.rightascension_hours)[0:14] == str(ra)[0:14], f"Iter #{i}: '{grh.rightascension_string}', {grh.rightascension_hours} != {ra}"
            assert str(grh.declination_degrees)[0:14] == str(dec)[0:14], f"Iter #{i}: '{grh.declination_string}', {grh.declination_degrees} != {dec}"

            ra *= -1.5
            dec *= -1.5

            grh.rightascension_hours = ra
            grh.declination_degrees = dec


if __name__ == '__main__':
    unittest.main()
