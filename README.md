# Discord free game and UE assets notifier 
Утилита для оповещения в дискоде о:

- Steam играх (±dlc)

- Epic games раздачах

- Unreal Engine Assets

Оригинальный проект: https://github.com/TheLovinator1/discord-free-game-notifier

# Использование 
1. Установить python


2. В директории выполнить:
pip install -r requirements.txt

3. Создать канал в дискорде для оповещения, создать webhook, записать его в файл token.txt (требуется создать данный файл)

4. Сделать автоматический запуск main.py по расписанию (допустим раз в 30 мин). Я использую crontab c нужной записью.