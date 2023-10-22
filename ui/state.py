from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    Sequence,
)

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from kit import (
    KITS,
    Kit,
    KitVariant,
)

BUTTON_TITLE_SHOW_CURRENT_SELECTIONS = "Show current selections"
BUTTON_TITLE_CONFIRM_SELECTIONS = "Confirm"
BUTTON_TITLE_SELECT_KIT_VARIANT = "Take"
BUTTON_TITLE_GO_BACK_TO_MAIN_MENU = "Go back to main menu"
BUTTON_TITLE_GO_BACK = "Go back"


class UserInterfaceState(ABC):
    _keyboard: list

    def get_keyboard_markup(self) -> InlineKeyboardMarkup:
        """
        Returns the InlineKeyboardMarkup of the user interface state.
        :return: InlineKeyboardMarkup
        """
        return InlineKeyboardMarkup(self.get_keyboard())

    def get_keyboard(self) -> Sequence[Sequence[InlineKeyboardButton]]:
        """
        Return the keyboard of the user interface state.
        :return: Sequence[Sequence[InlineKeyboardButton]]
        """
        if not hasattr(self, "_keyboard"):
            self._init_keyboard()
        return self._keyboard

    @abstractmethod
    def _init_keyboard(self):
        ...


class MainState(UserInterfaceState):
    def _init_keyboard(self):
        self._keyboard = []
        for kit in KITS.values():
            self._keyboard.append(
                [InlineKeyboardButton(kit.name, callback_data=kit.name)]
            )
        self._keyboard.append(
            [
                InlineKeyboardButton(
                    BUTTON_TITLE_SHOW_CURRENT_SELECTIONS,
                    callback_data=BUTTON_TITLE_SHOW_CURRENT_SELECTIONS,
                )
            ]
        )
        self._keyboard.append(
            [
                InlineKeyboardButton(
                    BUTTON_TITLE_CONFIRM_SELECTIONS,
                    callback_data=BUTTON_TITLE_CONFIRM_SELECTIONS,
                )
            ]
        )


class KitState(UserInterfaceState):
    _kit: Kit

    def __init__(self, kit: Kit):
        self._kit = kit

    def _init_keyboard(self):
        self._keyboard = []
        for kit_variant in self._kit.variants.values():
            title = kit_variant.variant_title
            self._keyboard.append([InlineKeyboardButton(title, callback_data=title)])

        self._keyboard.append(
            [
                InlineKeyboardButton(
                    BUTTON_TITLE_GO_BACK_TO_MAIN_MENU,
                    callback_data=BUTTON_TITLE_GO_BACK_TO_MAIN_MENU,
                )
            ]
        )


class KitVariantState(UserInterfaceState):
    _kit_variant: KitVariant

    def __init__(self, kit_variant: KitVariant):
        self._kit_variant = kit_variant

    def _init_keyboard(self):
        self._keyboard = [
            InlineKeyboardButton(
                BUTTON_TITLE_SELECT_KIT_VARIANT,
                callback_data=BUTTON_TITLE_SELECT_KIT_VARIANT,
            ),
            InlineKeyboardButton(
                BUTTON_TITLE_GO_BACK,
                callback_data=f"Go back {self._kit_variant.kit.name}",
            ),
            InlineKeyboardButton(
                BUTTON_TITLE_GO_BACK_TO_MAIN_MENU,
                callback_data=BUTTON_TITLE_GO_BACK_TO_MAIN_MENU,
            ),
        ]
