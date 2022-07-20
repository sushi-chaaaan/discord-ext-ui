from __future__ import annotations

from discord import ui
import discord

from typing import List, Callable, Any
from .utils import _call_any


class Modal(ui.Modal):
    def __init__(self, title: str, components: List[ui.TextInput]):
        super().__init__(title=title)
        for component in components:
            self.add_item(component)

        self._hook = None
        self._components = components

    def hook(self, func: Callable[[discord.Interaction], Any]) -> Modal:
        self._hook = func
        return self

    async def on_submit(self, interaction: discord.Interaction) -> None:
        inputted_values = []
        for raw_component in interaction.data.get("components", []): # type: ignore
            for component in self._components:
                if raw_component.get("custom_id") == component.custom_id:
                    inputted_values.append({f"{component.label}" : raw_component.get("value")})
        if self._hook is not None:
            await _call_any(self._hook, interaction, inputted_values)
        if not interaction.response.is_done():
            await interaction.response.defer()
