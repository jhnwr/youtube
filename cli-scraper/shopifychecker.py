import typer
import requests


app = typer.Typer()

@app.command()
def total_items(store: str):
    total = 0
    if store[-1] != "/":
        store = store + "/"
    for x in range(1,99):
        resp = requests.get(store + f"products.json?limit=250&page={x}")
        products = len(resp.json()['products'])
        total += products
        if products !=250:
            print(total)
            break

if __name__ == "__main__":
    app()   
