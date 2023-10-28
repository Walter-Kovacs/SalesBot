import logging
from typing import (
    Dict,
    List,
)

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
    KitState,
    KitVariantState,
    MainState,
)

logger = logging.getLogger(f"bot.{__name__}")

MAIN_STATE = "MAIN_STATE"
KIT_STATE = "KIT_STATE"
KIT_VARIANT_STATE = "KIT_VARIANT_STATE"

main_state: MainState
kit_states: Dict[str, KitState]
kit_variant_states: Dict[str, KitVariantState]


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
            kit_variant_key,
            reply_markup=kit_variant_states[kit_variant_key].get_keyboard_markup(),
        )
    return KIT_VARIANT_STATE


async def go_back_to_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query is not None:
        await query.answer()
        await query.edit_message_text(
            "Main menu", reply_markup=main_state.get_keyboard_markup()
        )
    return MAIN_STATE


async def select_kit_variant(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query is not None:
        kit_variant_key = str(query.data)  # kit.name~kit_variant.variant_title
        await query.answer()
        await query.edit_message_text(
            kit_variant_key, reply_markup=main_state.get_keyboard_markup()
        )
    return MAIN_STATE


async def go_back_to_kit_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query is not None:
        kit_name = str(query.data)
        await query.answer()
        await query.edit_message_text(
            kit_name, reply_markup=kit_states[kit_name].get_keyboard_markup()
        )
    return KIT_STATE


class ConversationHandlerManager:
    @staticmethod
    def create_handler() -> ConversationHandler:
        ConversationHandlerManager._create_states()

        handler = ConversationHandler(
            entry_points=[CommandHandler("start", start)],
            states={
                MAIN_STATE: ConversationHandlerManager._create_main_state_handler(),
                KIT_STATE: ConversationHandlerManager._create_kit_state_handlers(),
                KIT_VARIANT_STATE: ConversationHandlerManager._create_kit_variant_state_handlers(),
            },
            fallbacks=[CommandHandler("start", start)],
        )
        ConversationHandlerManager._log_handler(handler)

        return handler

    @staticmethod
    def _create_states() -> None:
        global main_state, kit_states, kit_variant_states
        main_state = MainState()
        kit_states = {kit.name: KitState(kit) for kit in KITS.values()}
        kit_variant_states = {
            f"{kit.name}~{kit_variant.variant_title}": KitVariantState(kit_variant)
            for kit in KITS.values()
            for kit_variant in kit.variants.values()
        }

    @staticmethod
    def _create_main_state_handler() -> List[CallbackQueryHandler]:
        handlers = [
            CallbackQueryHandler(open_kit_menu, pattern=callback_data)
            for callback_data in main_state.list_of_callback_data_go_to_kit
        ]
        handlers.append(
            CallbackQueryHandler(
                show_current_selection,
                pattern=MainState.callback_data_show_current_selections,
            )
        )
        handlers.append(
            CallbackQueryHandler(
                confirm_selections, pattern=MainState.callback_data_confirm_selections
            )
        )
        return handlers

    @staticmethod
    def _create_kit_state_handlers() -> List[CallbackQueryHandler]:
        handlers = [
            CallbackQueryHandler(open_kit_variant_menu, pattern=callback_data)
            for state in kit_states.values()
            for callback_data in state.list_of_callback_data_go_to_kit_variant
        ]
        handlers.append(
            CallbackQueryHandler(
                go_back_to_main_menu,
                pattern=KitState.callback_data_go_back_to_main_menu,
            )
        )
        return handlers

    @staticmethod
    def _create_kit_variant_state_handlers() -> List[CallbackQueryHandler]:
        handlers = [
            CallbackQueryHandler(
                select_kit_variant, pattern=state.callback_data_select_kit
            )
            for state in kit_variant_states.values()
        ]
        handlers += [
            CallbackQueryHandler(go_back_to_kit_menu, pattern=pattern)
            for pattern in set(
                [
                    state.callback_data_go_back_to_kit
                    for state in kit_variant_states.values()
                ]
            )
        ]
        handlers.append(
            CallbackQueryHandler(
                go_back_to_main_menu,
                pattern=KitVariantState.callback_data_go_back_to_main_menu,
            )
        )
        return handlers

    @staticmethod
    def _log_handler(handler: ConversationHandler):
        callback_space = max(
            [
                len(h.callback.__name__)
                for state in handler.states
                for h in handler.states[state]
            ]
        )
        callback_space += 4

        debug_string = "Conversation states handlers (callback, pattern):"
        for state in handler.states:
            debug_string += f"\n{state}:\n    " + "\n    ".join(
                [
                    f"{h.callback.__name__.ljust(callback_space)}{h.pattern}"
                    if isinstance(h, CallbackQueryHandler)
                    else repr(h)
                    for h in handler.states[state]
                ]
            )
        logger.info(debug_string)
