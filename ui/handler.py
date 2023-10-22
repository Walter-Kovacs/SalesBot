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
    BUTTON_TITLE_SHOW_CURRENT_SELECTIONS,
    KitState,
    MainState,
)

MAIN_STATE, KIT_STATE = range(2)
main_state: MainState = MainState()
kit_states: Dict[str, KitState] = {kit.name: KitState(kit) for kit in KITS.values()}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if msg is not None:
        await msg.reply_text("Main:", reply_markup=main_state.get_keyboard_markup())
    return MAIN_STATE


async def kit_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query is not None:
        kit_name: str = str(query.data)
        await query.answer()
        await query.edit_message_text(
            str(query.data), reply_markup=kit_states[kit_name].get_keyboard_markup()
        )
    return KIT_STATE


async def kit_variant_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass


async def show_current_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass


async def confirm_selections(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass


conversation_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        MAIN_STATE: [
            CallbackQueryHandler(kit_callback, pattern=kit.name)
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
                kit_variant_callback, pattern=f"{kit.name}~{kit_variant.variant_title}"
            )
            for kit in KITS.values()
            for kit_variant in kit.variants.values()
        ],
    },
    fallbacks=[CommandHandler("start", start)],
)
