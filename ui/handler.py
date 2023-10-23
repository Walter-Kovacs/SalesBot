from typing import Dict

from telegram import (
    Update,
)
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
)

from kit import (
    KITS,
)
from ui.state import (
    BUTTON_TITLE_CONFIRM_SELECTIONS,
    BUTTON_TITLE_GO_BACK_TO_MAIN_MENU,
    BUTTON_TITLE_SHOW_CURRENT_SELECTIONS,
    KitState,
    KitVariantState,
    MainState,
)

MAIN_STATE, KIT_STATE, KIT_VARIANT_STATE = range(3)
main_state: MainState = MainState()
kit_states: Dict[str, KitState] = {kit.name: KitState(kit) for kit in KITS.values()}
kit_variant_states: Dict[str, KitVariantState] = {
    f"{kit.name}~{kit_variant.variant_title}": KitVariantState(kit_variant)
    for kit in KITS.values()
    for kit_variant in kit.variants.values()
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if msg is not None:
        await msg.reply_text("Main", reply_markup=main_state.get_keyboard_markup())
    return MAIN_STATE


async def open_kit_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query is not None:
        kit_name: str = str(query.data)
        await query.answer()
        await query.edit_message_text(
            str(query.data), reply_markup=kit_states[kit_name].get_keyboard_markup()
        )
    return KIT_STATE


async def show_current_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query is not None:
        await query.edit_message_text(
            str(query.data), reply_markup=main_state.get_keyboard_markup()
        )
    return MAIN_STATE


async def confirm_selections(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query is not None:
        await query.edit_message_text(
            str(query.data), reply_markup=main_state.get_keyboard_markup()
        )
    return MAIN_STATE


async def open_kit_variant_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query is not None:
        kit_variant_key = str(query.data)  # kit.name~kit_variant.variant_title
        await query.answer()
        await query.edit_message_text(
            str(query.data),
            reply_markup=kit_variant_states[kit_variant_key].get_keyboard_markup(),
        )
    return KIT_VARIANT_STATE


async def go_back_to_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query is not None:
        await query.edit_message_text(
            "Main menu", reply_markup=main_state.get_keyboard_markup()
        )
    return MAIN_STATE


conversation_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        MAIN_STATE: [
            CallbackQueryHandler(open_kit_menu, pattern=kit.name)
            for kit in KITS.values()
        ]
        + [
            CallbackQueryHandler(
                show_current_selection, pattern=BUTTON_TITLE_SHOW_CURRENT_SELECTIONS
            ),
            CallbackQueryHandler(
                confirm_selections, pattern=BUTTON_TITLE_CONFIRM_SELECTIONS
            ),
        ],
        KIT_STATE: [
            CallbackQueryHandler(
                open_kit_variant_menu, pattern=f"{kit.name}~{kit_variant.variant_title}"
            )
            for kit in KITS.values()
            for kit_variant in kit.variants.values()
        ]
        + [
            CallbackQueryHandler(
                go_back_to_main_menu, pattern=BUTTON_TITLE_GO_BACK_TO_MAIN_MENU
            ),
        ],
        KIT_VARIANT_STATE: [],
    },
    fallbacks=[CommandHandler("start", start)],
)
