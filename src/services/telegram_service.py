from aiogram import Bot
from aiogram.enums.parse_mode import ParseMode
from aiogram.types import BufferedInputFile
from pydantic import SecretStr
from tenacity import retry, stop_after_attempt, wait_exponential


class TelegramService:
    def __init__(self, bot_token: SecretStr, chat_id: str):
        self.bot = Bot(token=bot_token.get_secret_value())
        self.chat_id = chat_id

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=15), reraise=True)
    async def send_message(self, text: str) -> None:
        await self.bot.send_message(
            chat_id=self.chat_id,
            text=text,
            parse_mode=ParseMode.HTML,
        )

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=15), reraise=True)
    async def send_pdf(
        self, pdf_data: bytes, filename: str = 'meeting_report.pdf'
    ) -> None:
        file = BufferedInputFile(pdf_data, filename=filename)
        await self.bot.send_document(
            chat_id=self.chat_id,
            document=file,
            caption='📄 Отчёт по встрече',
        )

    async def close(self) -> None:
        await self.bot.session.close()
