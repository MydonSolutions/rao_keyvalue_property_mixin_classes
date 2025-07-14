from typing import List
from enum import Enum
import os

from .hpdaq import HpdaqProperties
from .guppi_raw import GuppiRawDatatype


class HpdaqAtaProperties(HpdaqProperties):
    telescope: str = property(
        fget=lambda self={}: self.get("TELESCOP", "ATA"),
        fset=lambda self, value=None: self.__setitem__("TELESCOP", "ATA"),
        doc="""The telescope name or code referencing the ATA. Static."""
    )

    observation_stem: str = property(
        fget=lambda self: self.__getitem__("OBSSTEM"),
        fset=None
    )

    observation_stempath: str = property(
        fget=lambda self: os.path.join(
            self.observation_output_directorypath,
            self.observation_stem,
        ),
        fset=None
    )

    nof_beams: int = property(
        fget=lambda self: self.get("NBEAM", 0),
        fset=lambda self, value: self.__setitem__("NBEAM", value)
    )

    nof_channels: int = property(
        fget=lambda self: self.get(
            "NCHAN",
            self.observed_nof_channels//self.nof_antennas
        ),
        fset=lambda self, value: self.__setitem__("NCHAN", value),
        doc="""Number of channels per aspect: `OBSNCHAN/NANTS`.
        """
    )

    channel_bandwidth: float = property(
        fget=lambda self: self.get(
            "CHAN_BW",
            1.0/self.spectra_timespan
        ),
        fset=lambda self, value: self.__setitem__("CHAN_BW", value),
        doc="""Bandwidth of a channel.
        """
    )

    sample_datatype: str = property(
        fget=lambda self: GuppiRawDatatype(self.get("DATATYPE")),
        fset=None,
        doc="""The binary encoding of the samples in the block-data.
        Beamformed data is stored in a floating-point GUPPI file as an
        interim solution.
        """
    )

    observation_id: str = property(
        fget=lambda self: self.get("OBSID"),
        fset=lambda self, value: self.__setitem__("OBSID", value)
    )

    antenna_names: List[str] = property(
        fget=lambda self: HpdaqAtaProperties._gather_antennaCsvEntries(
            "ANTNMS",
            self
        ),
        fset=lambda self, value: [
            self.__setitem__(key, value)
            for key, value in HpdaqAtaProperties._generate_antennaCsvEntries(
                "ANTNMS",
                self,
                value
            )
        ]
    )

    antenna_flags: List[bool] = property(
        fget=lambda self: HpdaqAtaProperties._gather_antennaCsvEntries(
            "ANTFLG",
            self
        ),
        fset=lambda self, value: [
            self.__setitem__(key, value)
            for key, value in HpdaqAtaProperties._generate_antennaCsvEntries(
                "ANTFLG",
                self,
                value
            )
        ]
    )

    @staticmethod
    def _gather_antennaCsvEntries(key_prefix, kvp, separator: str = ","):
        # manage limited entry length
        nants = kvp.nof_antennas or 1

        antval_list = []
        key_enum = 0

        while len(antval_list) < nants:
            antvals = kvp.__getitem__(f"{key_prefix}{key_enum:02d}")
            key_enum += 1
            antval_list += antvals.split(separator)

        return antval_list[0:kvp.nof_antennas]

    @staticmethod
    def _generate_antennaCsvEntries(
        key_prefix,
        ant_values,
        separator: str = ","
    ):
        assert len(key_prefix) <= 6
        # manage limited entry length
        keyvalues = {}
        if len(ant_values) == 0:
            return keyvalues

        key_enum = 0
        current_str = ant_values[0]

        for ant in ant_values[1:]:
            addition = f"{separator}{ant}"
            if len(addition) + len(current_str) > 68:
                keyvalues[f"{key_prefix}%02d" % key_enum] = current_str
                key_enum += 1
                current_str = ant
            else:
                current_str += addition

        keyvalues[f"{key_prefix}%02d" % key_enum] = current_str
        return keyvalues
