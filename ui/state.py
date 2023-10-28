from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    List,
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
    def _init_keyboard(self) -> None:
        ...


class MainState(UserInterfaceState):
    callback_data_show_current_selections = BUTTON_TITLE_SHOW_CURRENT_SELECTIONS
    callback_data_confirm_selections = BUTTON_TITLE_CONFIRM_SELECTIONS

    def __init__(self) -> None:
        self.list_of_callback_data_go_to_kit: List[str] = [
            kit.name for kit in KITS.values()
        ]

    def _init_keyboard(self) -> None:
        self._keyboard = []
        for kit_name in self.list_of_callback_data_go_to_kit:
            self._keyboard.append(
                [InlineKeyboardButton(kit_name, callback_data=kit_name)]
            )
        self._keyboard.append(
            [
                InlineKeyboardButton(
                    BUTTON_TITLE_SHOW_CURRENT_SELECTIONS,
                    callback_data=MainState.callback_data_show_current_selections,
                )
            ]
        )
        self._keyboard.append(
            [
                InlineKeyboardButton(
                    BUTTON_TITLE_CONFIRM_SELECTIONS,
                    callback_data=MainState.callback_data_confirm_selections,
                )
            ]
        )


class KitState(UserInterfaceState):
    _kit: Kit
    callback_data_go_back_to_main_menu = BUTTON_TITLE_GO_BACK_TO_MAIN_MENU

    def __init__(self, kit: Kit) -> None:
        self._kit = kit
        self.list_of_callback_data_go_to_kit_variant = [
            f"{self._kit.name}~{kit_variant.variant_title}"
            for kit_variant in self._kit.variants.values()
        ]

    def _init_keyboard(self) -> None:
        self._keyboard = []
        for kit_and_variant in self.list_of_callback_data_go_to_kit_variant:
            self._keyboard.append(
                [
                    InlineKeyboardButton(
                        kit_and_variant.partition("~")[-1],  # kit variant title
                        callback_data=kit_and_variant,
                    )
                ]
            )

        self._keyboard.append(
            [
                InlineKeyboardButton(
                    BUTTON_TITLE_GO_BACK_TO_MAIN_MENU,
                    callback_data=KitState.callback_data_go_back_to_main_menu,
                )
            ]
        )


class KitVariantState(UserInterfaceState):
    _kit_variant: KitVariant
    callback_data_go_back_to_main_menu = BUTTON_TITLE_GO_BACK_TO_MAIN_MENU

    def __init__(self, kit_variant: KitVariant) -> None:
        self._kit_variant = kit_variant
        self.callback_data_select_kit = (
            f"{self._kit_variant.kit.name}~{self._kit_variant.variant_title}"
        )
        self.callback_data_go_back_to_kit = self._kit_variant.kit.name

    def _init_keyboard(self) -> None:
        self._keyboard = [
            [
                InlineKeyboardButton(
                    BUTTON_TITLE_SELECT_KIT_VARIANT,
                    callback_data=self.callback_data_select_kit,
                )
            ],
            [
                InlineKeyboardButton(
                    BUTTON_TITLE_GO_BACK,
                    callback_data=self.callback_data_go_back_to_kit,
                )
            ],
            [
                InlineKeyboardButton(
                    BUTTON_TITLE_GO_BACK_TO_MAIN_MENU,
                    callback_data=KitVariantState.callback_data_go_back_to_main_menu,
                )
            ],
        ]
