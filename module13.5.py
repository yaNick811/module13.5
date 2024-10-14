from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

# Инициализация бота и диспетчера
API_TOKEN = ''
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# Определение состояний
class UserState(StatesGroup):
    growth = State()
    age = State()
    weight = State()

# Создание клавиатуры
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(KeyboardButton('Рассчитать'))
keyboard.add(KeyboardButton('Информация'))

# Обработчик для начала ввода данных
@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    print('Привет! Я бот помогающий твоему здоровью.')
    await message.answer('Привет! Я бот помогающий твоему здоровью. Для расчета калорий нажмите "Рассчитать".', reply_markup=keyboard)

# Обработчик для начала ввода возраста
@dp.message_handler(text='Рассчитать')
async def set_age(message: types.Message):
    await message.answer('Введите свой возраст:', reply_markup=types.ReplyKeyboardRemove())
    await UserState.age.set()

# Обработчик для ввода возраста
@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=int(message.text))
    data = await state.get_data()
    await message.answer(f"Возраст: {data['age']}")
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

# Обработчик для ввода роста
@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=int(message.text))
    data = await state.get_data()
    await message.answer(f"Рост: {data['growth']}")
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

# Обработчик для ввода веса и расчета калорий
@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=int(message.text))
    data = await state.get_data()
    await message.answer(f"Вес: {data['weight']}")

    age = data['age']
    growth = data['growth']
    weight = data['weight']

    # Формула Миффлина - Сан Жеора для женщин
    calories = 10 * weight + 6.25 * growth - 5 * age - 161

    await message.answer(f"Ваша норма калорий: {calories} ккал в день.")
    await state.finish()

# Обработчик для всех остальных сообщений
@dp.message_handler()
async def all_message(message: types.Message):
    print("Введите команду /start, чтобы начать общение.")
    await message.answer('Введите команду /start, чтобы начать общение.')

# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)