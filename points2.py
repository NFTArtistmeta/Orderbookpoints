import binance
import pandas as pd
import matplotlib.pyplot as plt


def get_symbol():
    symbol = input("Ingresa el símbolo de la moneda que deseas obtener: ")
    if not symbol:
        symbol = ''
    return symbol


def main():
    client = binance.Client()

    symbol = get_symbol()
    print(f'Obteniendo información para la moneda {symbol}...')

    order_book = client.futures_order_book(symbol=symbol, limit=1000)
    order_book = pd.DataFrame(order_book)
    bids = pd.DataFrame(order_book['bids'])
    asks = pd.DataFrame(order_book['asks'])

    price_now = client.futures_mark_price(symbol=symbol)
    price = float(price_now['markPrice'])

    ask_min = float(asks['asks'].iloc[0][0])
    bid_max = float(bids['bids'].iloc[-1][0])
    dif_pct = (ask_min - bid_max) / (price / 100)

    print(f'Precio actual: {price}')
    print(f'Diferencia: {ask_min - bid_max}')
    print(f'Diferencia (en %): {dif_pct:.2f}')

    prices_b = [float(x[0]) for x in order_book['bids']]
    quantities_b = [float(x[1]) for x in order_book['bids']]

    prices_a = [float(x[0]) for x in order_book['asks']]
    quantities_a = [float(x[1]) for x in order_book['asks']]

    # Obtener los últimos 10 puntos de entrada y salida para long
    long_points = pd.DataFrame({
        'Precio de Compra': prices_b[-10:],
        'Cantidad de Compra': quantities_b[-10:],
        'Precio de Venta': prices_a[-10:],
        'Cantidad de Venta': quantities_a[-10:]
    })

    print("Últimos 10 puntos de entrada y salida para Long:")
    print(long_points)

    # Obtener los últimos 10 puntos de entrada y salida para short
    short_points = pd.DataFrame({
        'Precio de Compra': prices_a[-10:],
        'Cantidad de Compra': quantities_a[-10:],
        'Precio de Venta': prices_b[-10:],
        'Cantidad de Venta': quantities_b[-10:]
    })

    print("Últimos 10 puntos de entrada y salida para Short:")
    print(short_points)


if __name__ == "__main__":
    main()
