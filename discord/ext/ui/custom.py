from __future__ import annotations
from typing import Optional, Union, Callable

import discord
from discord import ui
from discord.utils import MISSING

from .utils import _call_any
from .modal import Modal


class CustomButton(ui.Button):
    def __init__(
            self,
            label: str = "",
            style: discord.ButtonStyle = discord.ButtonStyle.primary,
            disabled: bool = False,
            emoji: Optional[Union[str, discord.PartialEmoji]] = None,
            row: Optional[int] = None,
            custom_id: Optional[str] = None,
            modal_submit: Optional[Modal] = None
    ):
        super().__init__(
            label=label,
            style=style,
            disabled=disabled,
            emoji=emoji,
            custom_id=custom_id,
            row=row
        )
        self.callback_func: Optional[Callable] = None
        self.check_func: Optional[Callable[[discord.Interaction], bool]] = None
        self.modal_submit = modal_submit

    async def callback(self, interaction: discord.Interaction) -> None:
        if self.callback_func is None and self.modal_submit is None:
            return
        if self.check_func is not None:
            if not self.check_func(interaction):
                return
        if self.modal_submit is not None:
            await interaction.response.send_modal(self.modal_submit)
            return
        await _call_any(self.callback_func, interaction)


class CustomSelect(ui.Select):
    def __init__(
            self,
            *,
            custom_id: Optional[str],
            placeholder: Optional[str] = None,
            min_values: int = 1,
            max_values: int = 1,
            options: Optional[list[discord.SelectOption]],
            disabled: bool = False,
            row: Optional[int] = None,
            callback: Optional[Callable] = None,
            check_func: Optional[Callable[[discord.Interaction], bool]] = None
    ) -> None:
        custom_id = custom_id or MISSING
        options = options or MISSING
        super(CustomSelect, self).__init__(
            custom_id=custom_id,
            placeholder=placeholder,
            min_values=min_values,
            max_values=max_values,
            options=options,
            disabled=disabled,
            row=row
        )
        self.callback_func = callback
        self.check_func = check_func

    async def callback(self, interaction: discord.Interaction) -> None:
        if self.callback_func is None:
            return
        if self.check_func is not None:
            if not self.check_func(interaction):
                return
        selected_options = []
        for label in interaction.data.get("values", []):
            for option in self.options:
                if option.label == label:
                    selected_options.append(option)
                    continue
        await _call_any(self.callback_func, interaction, selected_options)


class CustomRoleSelect(ui.RoleSelect):
    def __init__(
            self,
            *,
            custom_id: Optional[str],
            placeholder: Optional[str] = None,
            min_values: int = 1,
            max_values: int = 1,
            disabled: bool = False,
            row: Optional[int] = None,
            callback: Optional[
                Callable[[discord.Interaction, list[discord.Role]], None]
            ] = None,
            check_func: Optional[Callable[[discord.Interaction], bool]] = None
    ) -> None:
        custom_id = custom_id or MISSING
        super(CustomRoleSelect, self).__init__(
            custom_id=custom_id,
            placeholder=placeholder,
            min_values=min_values,
            max_values=max_values,
            disabled=disabled,
            row=row
        )
        self.callback_func = callback
        self.check_func = check_func

    async def callback(self, interaction: discord.Interaction) -> None:
        if self.callback_func is None:
            return
        if self.check_func is not None:
            if not self.check_func(interaction):
                return
        await _call_any(self.callback_func, interaction, self.values)


class CustomUserSelect(ui.UserSelect):
    def __init__(
            self,
            *,
            custom_id: Optional[str],
            placeholder: Optional[str] = None,
            min_values: int = 1,
            max_values: int = 1,
            disabled: bool = False,
            row: Optional[int] = None,
            callback: Optional[
                Callable[
                    [discord.Interaction, list[Union[discord.Member, discord.User]]], None
                ]
            ] = None,
            check_func: Optional[Callable[[discord.Interaction], bool]] = None
    ) -> None:
        custom_id = custom_id or MISSING
        super(CustomUserSelect, self).__init__(
            custom_id=custom_id,
            placeholder=placeholder,
            min_values=min_values,
            max_values=max_values,
            disabled=disabled,
            row=row
        )
        self.callback_func = callback
        self.check_func = check_func

    async def callback(self, interaction: discord.Interaction) -> None:
        if self.callback_func is None:
            return
        if self.check_func is not None:
            if not self.check_func(interaction):
                return
        await _call_any(self.callback_func, interaction, self.values)


class CustomMentionableSelect(ui.MentionableSelect):
    def __init__(
            self,
            *,
            custom_id: Optional[str],
            placeholder: Optional[str] = None,
            min_values: int = 1,
            max_values: int = 1,
            disabled: bool = False,
            row: Optional[int] = None,
            callback: Optional[
                Callable[
                    [
                        discord.Interaction,
                        list[Union[discord.Role, discord.Member, discord.User]],
                    ],
                    None,
                ]
            ] = None,
            check_func: Optional[Callable[[discord.Interaction], bool]] = None
    ) -> None:
        custom_id = custom_id or MISSING
        super(CustomMentionableSelect, self).__init__(
            custom_id=custom_id,
            placeholder=placeholder,
            min_values=min_values,
            max_values=max_values,
            disabled=disabled,
            row=row
        )
        self.callback_func = callback
        self.check_func = check_func

    async def callback(self, interaction: discord.Interaction) -> None:
        if self.callback_func is None:
            return
        if self.check_func is not None:
            if not self.check_func(interaction):
                return
        await _call_any(self.callback_func, interaction, self.values)


class CustomChannelSelect(ui.ChannelSelect):
    def __init__(
            self,
            *,
            custom_id: Optional[str],
            channel_types: Optional[list[discord.ChannelType]],
            placeholder: Optional[str] = None,
            min_values: int = 1,
            max_values: int = 1,
            disabled: bool = False,
            row: Optional[int] = None,
            callback: Optional[
                Callable[
                    [
                        discord.Interaction,
                        list[Union[discord.abc.GuildChannel, discord.Thread]],
                    ],
                    None,
                ]
            ] = None,
            check_func: Optional[Callable[[discord.Interaction], bool]] = None
    ) -> None:
        custom_id = custom_id or MISSING
        channel_types = channel_types or MISSING
        super(CustomChannelSelect, self).__init__(
            custom_id=custom_id,
            placeholder=placeholder,
            min_values=min_values,
            max_values=max_values,
            channel_types=channel_types,
            disabled=disabled,
            row=row
        )
        self.callback_func = callback
        self.check_func = check_func

    async def callback(self, interaction: discord.Interaction) -> None:
        if self.callback_func is None:
            return
        if self.check_func is not None:
            if not self.check_func(interaction):
                return
        _resolved = [c.resolve() or await c.fetch() for c in self.values]
        await _call_any(self.callback_func, interaction, _resolved)
