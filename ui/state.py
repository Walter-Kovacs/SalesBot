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

from products import (
    PRODUCTS,
    Product,
    ProductVariant,
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
    list_of_callback_data_go_to_product: List[str]
    callback_data_show_current_selections = BUTTON_TITLE_SHOW_CURRENT_SELECTIONS
    callback_data_confirm_selections = BUTTON_TITLE_CONFIRM_SELECTIONS

    def __init__(self) -> None:
        self.list_of_callback_data_go_to_product: List[str] = [
            product_name for product_name in PRODUCTS.names()
        ]

    def _init_keyboard(self) -> None:
        self._keyboard = []
        for product_name in self.list_of_callback_data_go_to_product:
            self._keyboard.append(
                [InlineKeyboardButton(product_name, callback_data=product_name)]
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


class ProductState(UserInterfaceState):
    _product: Product
    callback_data_go_back_to_main_menu = BUTTON_TITLE_GO_BACK_TO_MAIN_MENU

    def __init__(self, product: Product) -> None:
        self._product = product
        self.list_of_callback_data_go_to_product_variant = [
            f"{self._product.name}~{product_variant_name}" for product_variant_name in self._product.variants.names()
        ]

    def _init_keyboard(self) -> None:
        self._keyboard = []
        for product_and_variant in self.list_of_callback_data_go_to_product_variant:
            self._keyboard.append(
                [
                    InlineKeyboardButton(
                        product_and_variant.partition("~")[-1],  # product variant name
                        callback_data=product_and_variant,
                    )
                ]
            )

        self._keyboard.append(
            [
                InlineKeyboardButton(
                    BUTTON_TITLE_GO_BACK_TO_MAIN_MENU,
                    callback_data=ProductState.callback_data_go_back_to_main_menu,
                )
            ]
        )


class ProductVariantState(UserInterfaceState):
    _product_variant: ProductVariant
    callback_data_go_back_to_main_menu = BUTTON_TITLE_GO_BACK_TO_MAIN_MENU

    def __init__(self, product_variant: ProductVariant) -> None:
        self._product_variant = product_variant
        self.callback_data_select_this_variant = (
            f"{self._product_variant.product.name}~{self._product_variant.name}"
        )
        self.callback_data_go_back_to_product_menu = self._product_variant.product.name

    def _init_keyboard(self) -> None:
        self._keyboard = [
            [
                InlineKeyboardButton(
                    BUTTON_TITLE_SELECT_KIT_VARIANT,
                    callback_data=self.callback_data_select_this_variant,
                )
            ],
            [
                InlineKeyboardButton(
                    BUTTON_TITLE_GO_BACK,
                    callback_data=self.callback_data_go_back_to_product_menu,
                )
            ],
            [
                InlineKeyboardButton(
                    BUTTON_TITLE_GO_BACK_TO_MAIN_MENU,
                    callback_data=ProductVariantState.callback_data_go_back_to_main_menu,
                )
            ],
        ]
