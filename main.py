import tkinter as tk

from ebaysdk.finding import Connection
import matplotlib.animation as animation
import matplotlib.ticker as ticker
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import pandas as pd


LARGE_FONT = ('Verdana', 20)
MEDIUM_FONT = ('Verdana', 14)
NORMAL_FONT = ('Verdana', 10)
style.use('ggplot')

api_calls = 0
time_series = []
lego_prices = []
graph = Figure(figsize=(5, 5), dpi=100)
axis = graph.add_subplot(111)


def animate(i):
    global api_calls

    ebay = Ebay()
    lego_price = ebay.mean_buy_price('Lego 5 lbs') / 5

    time_series.append(api_calls)
    lego_prices.append(lego_price)

    axis.clear()
    axis.set_title('$LEGO-USD (1 lb.)')

    axis.set_xlabel('API Calls')
    axis.set_ylabel('Price')

    axis.set_xlim(0, len(lego_prices) * 1.2)
    axis.set_ylim(min(lego_prices) * 0.9, max(lego_prices) * 1.1)

    formatter = ticker.FormatStrFormatter('$%1.2f')
    axis.yaxis.set_major_formatter(formatter)

    axis.plot(time_series, lego_prices)

    api_calls += 1


def notify(msg):
    popup = tk.Tk()
    popup.wm_title('Notification')
    label = tk.Label(popup, text=msg, font=NORMAL_FONT)
    label.pack(side='top', fill='x', pady=10)
    okay_btn = tk.Button(popup, text='Okay', command=popup.destroy)
    okay_btn.pack()
    popup.mainloop()


class Ebay():

    def __init__(self):
        self.api = Connection(config_file='ebay.yaml', siteid='EBAY-US')

    def search(self, keywords):
        request = {
            'keywords': keywords,
            'itemFilter': [
                {'name': 'LocatedIn', 'value': 'US'}
            ],
            'paginationInput': {
                'entriesPerPage': 100,
                'pageNumber': 1
            },
            'sortOrder': 'BestMatch'
        }
        response = self.api.execute('findItemsByKeywords', request).dict()

        items = []
        for listing in response['searchResult']['item']:
            item = {}

            item['listingType'] = listing['listingInfo']['listingType']
            item['currentPrice'] = listing['sellingStatus']['currentPrice']['value']

            if listing['shippingInfo']['shippingType'] == 'Flat':
                shipping_price = float(listing['shippingInfo']['shippingServiceCost']['value'])
                item['totalPrice'] = float(item['currentPrice']) + shipping_price
            else:
                item['totalPrice'] = item['currentPrice']

            items.append(item)

        return pd.DataFrame(items).apply(pd.to_numeric, errors='ignore')

    def mean_buy_price(self, keywords):
        items = self.search(keywords)
        items = items[(items.listingType == 'StoreInventory') | (items.listingType == 'FixedPrice')]
        return items.totalPrice.mean()


class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, 'Realtime Lego Price')
        self.run()

    def run(self):
        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menu = tk.Menu(container)
        options = tk.Menu(menu, tearoff=0)

        options.add_command(label='Quit', command=quit)
        menu.add_cascade(label='Options', menu=options)

        tk.Tk.config(self, menu=menu)

        frame = HomePage(container, self)
        frame.grid(row=0, column=0, sticky='nsew')
        frame.tkraise()


class HomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.run()

    def run(self):
        canvas = FigureCanvasTkAgg(graph, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


if __name__ == '__main__':
    app = App()
    app.geometry('500x700')
    ani = animation.FuncAnimation(graph, animate, interval=2500)
    app.mainloop()
