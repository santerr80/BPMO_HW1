import pika
import json
import pandas as pd
import matplotlib.pyplot as plt

columns = ["id", "y_true", "y_pred", "absolute_error"]
    
df = pd.DataFrame(columns=columns)

def callback(ch, method, properties, body):
    data = json.loads(body)
    
    df.loc[len(df)] = data
    
    # Создание и настройка гистрограммы
    plt.figure(figsize=(10, 6))
    plt.hist(df['absolute_error'], bins=10, edgecolor='black')
    plt.title('Histogram of Absolute Error')
    plt.xlabel('Absolute Error')
    plt.ylabel('Count')
    plt.grid(True)

    # Сохранение гистограммы в файл
    output_file = './logs/error_distribution.png'
    plt.savefig(output_file)
    plt.close()

# Работа с очередью plot
try:
    # Создаём подключение к серверу на локальном хосте
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()
    
    # Объявляем очередь plot
    channel.queue_declare(queue='plot')
    
    # Извлекаем сообщение из очереди plot
    channel.basic_consume(
        queue='plot',
        on_message_callback=callback,
        auto_ack=True)

