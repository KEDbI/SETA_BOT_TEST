# SETA_BOT_TEST
Тестовое задание для ООО СЕТА

**Задачи:**
  **1. Создание бота и обработка команд**
  
      Создать Telegram-бота, который отвечает на команду /start сообщением "Добро пожаловать в наш бот!", и команду /help сообщением "Доступные команды: /start, /help, /echo, /photo".
      
      Критерии проверки:
          Корректное создание бота и настройка диспетчера
          Обработка команд /start и /help
          
  **2. Команда /echo**
  
      Добавить команду /echo, которая будет возвращать пользователю его собственное сообщение.
      
      Критерии проверки:
        Корректная обработка команды /echo
        Правильный возврат сообщения пользователя
        
  **3. Inline кнопки и обработка коллбеков**
  
      Создать inline-кнопки с опциями "Выбор 1" и "Выбор 2”. При нажатии на любую из них бот должен отвечать соответствующим сообщением "Вы выбрали Выбор 1" или "Вы выбрали Выбор 2".
      
      Критерии проверки:
        Корректная работа inline-кнопок
        Правильная обработка коллбеков и ответ на нажатие
  **4. Хранение данных пользователя с использованием FSM (Finite State Machine)**
  
      Реализовать бота, который запрашивает у пользователя его имя и возраст, сохраняя эти данные с использованием FSM и выводит их в конце.
      
      Критерии проверки:
        Корректная реализация FSM
        Правильное сохранение и отображение введенных данных
        
  **5. Загрузка и обработка изображений**
  
      Добавить возможность пользователю отправлять изображение, на которое бот будет отвечать размером изображения в пикселях (ширина x высота).
      
      Критерии проверки:
        Корректная загрузка изображений
        Правильное определение и вывод размеров изображения
        
  **6. Интеграция с базой данных SQLite**
  
      Создать таблицу пользователей в базе данных SQLite и сохранить в неё данные пользователя (ID, имя, возраст). Реализовать команду /users для вывода всех пользователей.
      
      Критерии проверки:
        Корректная работа с SQLite
        Правильное сохранение и извлечение данных
        Корректный вывод списка пользователей
        
  **7. Обработка данных с API**
  
      Реализовать команду /weather, которая будет запрашивать у пользователя название города и выводить текущую погоду, используя API (например, OpenWeatherMap).
      
      Критерии проверки:
        Корректная работа с API
        Правильная обработка и вывод данных о погоде
        
  **8. Периодические задачи (Scheduled Tasks)**
  
      Добавить функционал, который будет отправлять пользователям сообщение "Не забудьте проверить уведомления!" каждый день в 9:00 утра.
      
      Критерии проверки:
        Корректная реализация периодических задач
        Отправка сообщения в заданное время
  **9. Напоминание о необходимости ответа через 15 минут**
  
      Пользователю бот отправляет сообщение: «Привет, «имя пользователя»! Как ты сегодня?». Добавить функционал, при котором бот отправит пользователю сообщение «вы забыли ответить», если пользователь не ответил на вопрос в течение 15 минут. Например, если бот задаёт пользователю вопрос, и тот не отвечает, то через 15 минут бот должен отправить сообщение "Вы забыли ответить".
      
      Критерии проверки: 
        Корректная реализация отслеживания времени ожидания ответа.
        Отправка напоминания через 15 минут, если ответа нет.
        Отмена напоминания, если пользователь ответил до истечения 15 минут.
        Использовать флаги middleware в aiogram 

  **10. Обработка ошибок и исключений**
  
      Реализовать обработку исключений, чтобы бот отправлял сообщение "Произошла ошибка, попробуйте позже" в случае любой ошибки. Примеры ошибок: пользователь вместо фото для определения размеров загрузил файл. Или вместо возраста в виде цифр, ввел буквами и тд 
      
      Критерии проверки:
        Корректная обработка исключений
        Правильное уведомление пользователя об ошибке
        В случае возникновения ошибки отправлять пользователю сообщение "Произошла ошибка, попробуйте позже".
        Логировать ошибки для дальнейшего анализа и устранения.
      
