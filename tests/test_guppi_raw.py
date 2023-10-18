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
        assert blockshape[3] == grh["NPOL"]
        assert blockshape[2] == 1024


if __name__ == '__main__':
    unittest.main()
