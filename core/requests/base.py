from ..objects.tg_objects import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, ForceReply

ReplyMarkupT = ReplyKeyboardMarkup | InlineKeyboardMarkup | ReplyKeyboardRemove | ForceReply
