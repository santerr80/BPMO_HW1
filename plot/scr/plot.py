import pika
import pandas as pd
import matplotlib.pyplot as plt

# Укажите путь к вашему CSV-файлу
file_path = './logs/metric_log.csv'

# Импортируйте CSV-файл в DataFrame
df = pd.read_csv(file_path)

# Выведите первые несколько строк DataFrame для проверки
plt.figure(figsize=(10, 6))
plt.hist(df['absolute_error'], bins=10, edgecolor='black')
plt.title('Histogram of Absolute Error')
plt.xlabel('Absolute Error')
plt.ylabel('Count')
plt.grid(True)

# Сохранение графика в файл
output_file = './logs/error_distribution.png'
plt.savefig(output_file)


plt.close()
