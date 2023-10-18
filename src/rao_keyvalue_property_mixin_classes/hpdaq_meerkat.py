from .hpdaq import HpdaqProperties


class HpdaqMeerkatProperties(HpdaqProperties):
    channel_bandwidth: float = property(
        fget=lambda self: self.__get_item__(
            "CHAN_BW"
        ),
        fset=lambda self, value: self.set("CHAN_BW", value)
    )

    nof_polarizations: int = property(
        fget=lambda self: self.__get_item__("NPOL"),
        fset=lambda self, value: self.set("NPOL", value),
        doc="""Number of polarizations in the data of the block.
            Critical to rawspec processing a file.

            Has a factor of 2 that, ostensibly, refers to the
            complexity of the data. Contemporarily, a value of 4
            is reinterpreted as 2 actual polarizations.
        """
    )
