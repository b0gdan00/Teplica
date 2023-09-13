import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
import pandas as pd
from config.DBEngine import SQLiteDB

def createPlot():
    db = SQLiteDB()
    try:
        data = db.get_last_hour()
        df = pd.DataFrame(data)
        df[1] = pd.to_datetime(df[1])
        fig = plt.figure(figsize=(18, 8))
        ax = fig.gca()
        ax.yaxis.set_major_locator(MultipleLocator(10))
        ax.yaxis.set_minor_locator(MultipleLocator(2))
        ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=5))
        ax.xaxis.set_minor_locator(mdates.MinuteLocator(interval=1))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        ax.grid(which='both')
        plt.plot(df[1], df[4],label='Освітленість', color = "orange", marker='.', linestyle='-')
        plt.plot(df[1], df[3], label='Температура', color = "blue", marker='.', linestyle='-')
        plt.plot(df[1], df[5], label='CO2', color = "red", marker='.', linestyle='-')
        plt.plot(df[1], df[2], label='green', color = "green", marker='.', linestyle='-')
        plt.xlabel('Час')
        plt.ylabel('Значення')
        plt.title('Зміна фізичних параметрів мікроклімату в залежності від часу')
        ax.grid(which='major', linestyle='--')
        ax.grid(which='minor', linestyle=':')
        ax.grid(which='minor', alpha=0.5)
        ax.grid(which='major', alpha=0.7)
        plt.ylim(top=100, bottom=0)
        plt.legend()
        plt.tight_layout()
        plt.savefig('Images/stat.png', dpi=100)
    except Exception as e: print(e)
    finally: db.close()
