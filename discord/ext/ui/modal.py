from __future__ import annotations

import os

from discord import ui
import discord

from typing import List, Callable, Any
from .utils import _call_any


class Modal(ui.Modal):
    def __init__(self, title: str, components: List[ui.TextInput]):
        super().__init__(title=title)
        for component in components:
            component.custom_id = os.urandom(16).hex()
            self.add_item(component)

        self._hook = None
        self._components = components

    def hook(self, func: Callable[[discord.Interaction], Any]) -> Modal:
        self._hook = func
        return self

    async def on_submit(self, interaction: discord.Interaction) -> None:
        inputted_values = []
        modal_component = interaction.data.get("components",[]) # type: ignore
        if modal_component == []:
            pass
        
        else:
            text_inputs = modal_component[0].get("components",[]) # type: ignore
            for raw_input in text_inputs:
                for component in self._components:
                    if component.custom_id == raw_input.get("custom_id", ""):
                        inputted_values.append(f"{component.label}: {raw_input.get('value', '')}")
                        continue
        if self._hook is not None:
            await _call_any(self._hook, interaction, inputted_values)
        if not interaction.response.is_done():
            await interaction.response.defer()
