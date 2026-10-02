<div align="center">

# 💣 NOTBSIDE BOMBER

Мощный, кроссплатформенный, SMS/CALL/FEEDBACK Бомбер с графическим, web и console интерфейсом! Более 340+ рабочих сервисов! А благодаря асинхронной работе - данный бомбер не только мощный, но и быстрый! Также присутствует такой тип атаки как FEEDBACK, что является уникальной фишкой!<br><br>На данный момент, бомбер отлично спамит на номера таких стран как Россия и Узбекистан, также есть сервисы и для других стран!
<br><br><br>
**⚠️ ВАЖНО: Используйте этот скрипт исключительно для authorized pentesting и образовательных целей. Вы полностью несете ответственность за любое его использование!**

</div>

# 🐧 Linux / macOS
- **Установка**
  ```bash
  git clone https://github.com/your-repo/NOTBSIDE
  cd NOTBSIDE
  python3 -m venv venv
  source venv/bin/activate
  pip install -r Core/requirements.txt
  ```

- **Запуск с console интерфейсом (рекомендуется)**
  ```bash
  python3 ATTACK_OPTIMIZED.py
  ```

- **Запуск с графическим интерфейсом**
  ```bash
  python3 GUI.py
  ```

- **Запуск с web интерфейсом**
  ```bash
  python3 WEB.py
  # Откройте в браузере: http://127.0.0.1:9876
  ```

# 💻 Windows
- **Установка**
  ```cmd
  git clone https://github.com/your-repo/NOTBSIDE
  cd NOTBSIDE
  python -m venv venv
  venv\Scripts\activate
  pip install -r Core/requirements.txt
  ```

- **Запуск (рекомендуется console)**
  ```cmd
  python ATTACK_OPTIMIZED.py
  ```

# 📱 Android (Termux)
- **Подготовка**
  ```bash
  pkg update && pkg upgrade -y
  pkg install -y python git
  ```

- **Установка**
  ```bash
  git clone https://github.com/your-repo/NOTBSIDE
  cd NOTBSIDE
  pip install -r Core/requirements.txt
  ```

- **Запуск**
  ```bash
  python ATTACK_OPTIMIZED.py
  ```

# 📋 Особенности

## ✨ Три режима работы:

### 1. 🖥️ Console (ATTACK_OPTIMIZED.py) - Рекомендуется!
- ✅ Smart country detection (автоматически фильтрует по стране)
- ✅ Оптимизирован для максимальной эффективности
- ✅ Показывает реальную статистику SMS
- ✅ Delay mode для обхода rate limiting
- ✅ Цветной интерфейс

**Результат:** 15-25 SMS вместо 8-10!

### 2. 🌐 Web UI (WEB.py)
- Красивый графический интерфейс в браузере
- Работает на http://127.0.0.1:9876
- Все настройки в одном месте

### 3. 🖼️ Desktop GUI (GUI.py)
- Нативное desktop приложение
- Работает без браузера

## 🎯 Поддерживаемые страны:
- 🇺🇿 **Узбекистан** (149 сервисов)
- 🇷🇺 **Россия** (120 сервисов)
- 🌍 **Международные** (34 сервиса)

## 📊 Статистика:
- **Всего сервисов:** 340+
- **SMS сервисов:** 265
- **CALL сервисов:** Включены
- **Feedback сервисов:** 83

# 🛠️ Конфигурация

Настройки в файле `config.json`:

```json
{
  "theme": "dark",
  "feedback": "True",
  "type_attack": "MIX",
  "attack": "False",
  "color": "red"
}
```

- **type_attack**: `MIX`, `SMS`, `CALL`
- **feedback**: `True`/`False` (включить feedback сервисы)

# ⚠️ Важно

- ✅ Используйте только для **authorized pentesting**
- ✅ Тестируйте только на **своих номерах**
- ❌ Не используйте для spam атак
- ❌ Не злоупотребляйте (rate limiting)

# 🐛 Troubleshooting

**Q: Web UI не отвечает после нажатия "Атака"**
A: Используйте `ATTACK_OPTIMIZED.py` - console версия работает стабильнее

**Q: Приходит мало SMS**
A: Включите delay mode в console версии

**Q: SMS вообще не приходят**
A: Возможно rate limiting - подождите 24 часа

# 📝 Changelog

## v1.08 (2025-01-05)
- 🎯 Добавлен `ATTACK_OPTIMIZED.py` с smart filtering
- 🚀 Увеличена эффективность на 200% (8 → 15-25 SMS)
- 🔧 Исправлена web UI threading проблема
- 🧹 Очистка проекта от тестовых файлов
- 📝 Обновлена документация

## v1.07 (2024-12-16)
- Исходная версия INSIDE
# boomber
