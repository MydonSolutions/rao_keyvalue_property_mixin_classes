from .guppi_raw import GuppiRawProperties
from .hpdaq_ata import HpdaqAtaProperties


class HpdaqCosmicProperties(HpdaqAtaProperties):
    telescope: str = property(
        fget=lambda self={}: self.get("TELESCOP", "COSMIC"),
        fset=lambda self, value=None: self.__setitem__("TELESCOP", "COSMIC"),
        doc="""The telescope name or code referencing the COSMIC. Static."""
    )

    phasecenter_rightascension_hours: float = property(
        fget=lambda self: GuppiRawProperties.from_sexagesimal_str(
            self.__getitem__("RA_PHAS")
        ),
        fset=lambda self, value: self.__setitem__(
            "RA_PHAS",
            GuppiRawProperties.to_sexagesimal_str(value)
        ),
        doc="""The right-ascension phase-center coordinate of the block-data.
        """
    )

    phasecenter_declination_degrees: float = property(
        fget=lambda self: GuppiRawProperties.from_sexagesimal_str(
            self.__getitem__("DEC_PHAS")
        ),
        fset=lambda self, value: self.__setitem__(
            "DEC_PHAS",
            GuppiRawProperties.to_sexagesimal_str(value)
        ),
        doc="""The declination phase-center coordinate of the block-data.
        """
    )
