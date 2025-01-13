import pika
import json
import csv

# Создаём функцию callback для обработки данных из очереди
def callback(ch, method, properties, body):
    data = json.loads(body)
    queue = method.routing_key

    if queue == 'y_true':
        y_true_data.append(data)
    elif queue == 'y_pred':
        y_pred_data.append(data)

    # Проверяем совпадение id и записываем результат в файл
    for true_item in y_true_data:
        for pred_item in y_pred_data:
            if true_item['id'] == pred_item['id']:
                answer_string = [true_item['id'], true_item['y'], pred_item['y_pred'], abs(true_item['y'] - pred_item['y_pred'])]
                with open('./logs/metric_log.csv', 'a', newline='') as csvfile:
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow(answer_string)
                # Удаляем обработанные элементы из списков
                y_true_data.remove(true_item)
                y_pred_data.remove(pred_item)
                break

try:
    # Создаём подключение к серверу на локальном хосте
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    # Объявляем очередь y_true
    channel.queue_declare(queue='y_true')
    # Объявляем очередь y_pred
    channel.queue_declare(queue='y_pred')

    y_true_data = []
    y_pred_data = []

    # Извлекаем сообщение из очереди y_true
    channel.basic_consume(
        queue='y_true',
        on_message_callback=callback,
        auto_ack=True
    )
    # Извлекаем сообщение из очереди y_pred
    channel.basic_consume(
        queue='y_pred',
        on_message_callback=callback,
        auto_ack=True
    )

    # Запускаем режим ожидания прихода сообщений
    print('...Ожидание сообщений, для выхода нажмите CTRL+C')
    channel.start_consuming()
except Exception as e:
    print(f'Не удалось подключиться к очереди: {e}')
