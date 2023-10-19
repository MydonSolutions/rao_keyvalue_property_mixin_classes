from .hpdaq_ata import HpdaqAtaProperties


class HpdaqCosmicProperties(HpdaqAtaProperties):
    telescope: str = property(
        fget=lambda self={}: self.get("TELESCOP", "COSMIC"),
        fset=lambda self, value=None: self.__setitem__("TELESCOP", "COSMIC"),
        doc="""The telescope name or code referencing the COSMIC. Static."""
    )
