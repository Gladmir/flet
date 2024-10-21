import flet as ft

async def homepage():
    return {"message": "Olá, Mundo!"}

def main(page: ft.Page):
    page.bgcolor=ft.colors.ORANGE_200
    page.title = "Aplicação Web"
    page.add(ft.Text("Olá, Mundo!", size=30))

ft.app(target=main, view=ft.AppView.WEB_BROWSER)