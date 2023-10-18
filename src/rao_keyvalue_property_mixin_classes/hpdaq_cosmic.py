from .hpdaq_ata import HpdaqAtaProperties


class HpdaqCosmicProperties(HpdaqAtaProperties):
    telescope: str = property(
        fget=lambda self=None: "COSMIC",
        fset=None,
        doc="""The telescope name or code referencing the COSMIC. Static, read-only."""
    )
