# План Реализации Демо-Проекта

## Описание

Демонстрационный проект "Магазин на Микросервисах" для изучения RabbitMQ и FastStream.
Архитектура имитирует реальный flow заказа: User -> Bot -> API -> Broker -> Worker -> Broker -> Bot -> User.

## Архитектура

### 1. Cashier (API Service)

- **Технологии**: FastAPI, FastStream (RabbitBroker).
- **Порт**: 9010 (по умолчанию)
- **Задача**: Принимает заказ по HTTP, публикует событие `order.created`.

### 2. Kitchen (Worker Service)

- **Технологии**: FastAPI, FastStream.
- **Порт**: 9020 (по умолчанию)
- **Задача**: Слушает `order.created`, имитирует обработку (с задержкой), публикует события `order.started` (начало готовки) и `order.processed` (готовность).

### 3. Telegram Bot (Notification Service)

- **Технологии**: aiogram, FastStream.
- **Задача**: Интерфейс для пользователя (Меню, Корзина), отправка заказов в API и получение уведомлений о статусах (`started`, `processed`) через RabbitMQ.

## Инфраструктура

- **RabbitMQ**: Брокер сообщений (с плагином Management для удобного WebUI).
- **Docker Compose**: Оркестрация контейнеров.

## FAQ

**Почему RabbitMQ?**
Стандарт индустрии, строгая типизация очередей/обменников, надежность.

**Почему FastStream?**
Современный подход, Pydantic-валидация, удобные декораторы, документация AsyncAPI.
