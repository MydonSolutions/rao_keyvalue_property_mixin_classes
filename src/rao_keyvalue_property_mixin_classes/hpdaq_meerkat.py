from .hpdaq import HpdaqProperties


class HpdaqMeerkatProperties(HpdaqProperties):
    telescope: str = property(
        fget=lambda self=None: "MeerKAT",
        fset=None,
        doc="""The telescope name or code referencing the MeerKAT. Static, read-only."""
    )

    channel_bandwidth: float = property(
        fget=lambda self: self.__getitem__(
            "CHAN_BW"
        ),
        fset=lambda self, value: self.set("CHAN_BW", value)
    )

    nof_polarizations: int = property(
        fget=lambda self: (
            2 if self.__getitem__("NPOL") == 4
            else self.__getitem__("NPOL")
        ),
        fset=lambda self, value: self.set("NPOL", value),
        doc="""Number of polarizations in the data of the block.
            Critical to rawspec processing a file.

            Has a factor of 2 that, ostensibly, refers to the
            complexity of the data. Contemporarily, a value of 4
            is reinterpreted as 2 actual polarizations.
        """
    )
