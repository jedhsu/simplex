"""
Thinking
========

Collects all world states visited during a lifetime.

"""

from dataclasses import dataclass

from typing import Sequence


@dataclass
class Thinking(
    WorldState,
):
    states: Sequence[WorldState]
    demons: Sequence[Demon]
    thermodynamics: Sequence[Energy]