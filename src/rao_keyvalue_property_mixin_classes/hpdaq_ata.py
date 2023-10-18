from typing import List
from enum import Enum
import os

from .hpdaq import HpdaqProperties


class HpdaqAtaDatatype(str, Enum):
    integer = "INTEGER"
    floating_point = "FLOAT"


class HpdaqAtaProperties(HpdaqProperties):
    telescope: str = property(
        fget=lambda self=None: "ATA",
        fset=None,
        doc="""The telescope name or code referencing the ATA. Static, read-only."""
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
        fset=lambda self, value: self.set("NBEAM", value)
    )

    nof_channels: int = property(
        fget=lambda self: self.get(
            "NCHAN",
            self.observed_nof_channels//self.nof_antennas
        ),
        fset=lambda self, value: self.set("NCHAN", value),
        doc="""Number of channels per aspect: `OBSNCHAN/NANTS`.
        """
    )

    channel_bandwidth: float = property(
        fget=lambda self: self.get(
            "CHAN_BW",
            1.0/self.channel_timespan
        ),
        fset=lambda self, value: self.set("CHAN_BW", value),
        doc="""Bandwidth of a channel.
        """
    )

    sample_datatype: str = property(
        fget=lambda self: HpdaqAtaDatatype(self.get("DATATYPE")),
        fset=None
    )

    observation_id: str = property(
        fget=lambda self: self.get("OBSID"),
        fset=lambda self, value: self.set("OBSID", value)
    )

    antenna_names: List[str] = property(
        fget=lambda self: HpdaqAtaProperties._gather_antennaCsvEntries(
            "ANTNMS",
            self
        ),
        fset=lambda self, value: [
            self.set(key, value)
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
            self.set(key, value)
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

        antname_list = []
        key_enum = 0

        while len(antname_list) < nants:
            antnames = kvp.get(f"{key_prefix}{key_enum:02d}")
            key_enum += 1
            antname_list += antnames.split(separator)

        return antname_list[0:kvp.nof_antennas]

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
