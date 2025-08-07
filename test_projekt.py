from playwright.sync_api import Page
from datetime import datetime

#pytest test_projekt.py
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

def test_title_lekarna(page: Page):
    page.goto("https://www.lekarnalemon.cz/?srsltid=AfmBOooEQ8c3jgvq-BJtH48oN3GY7-c4_KsYt6MVQ4JPhedXCQ4LGWCp")
    title = page.title()
    print("Page title is:", title)
    
    assert "Profesionální péče o Vaše zdraví a krásu" in title

# cookies
def test_cookies_click(page: Page):
    page.goto("https://www.lekarnalemon.cz/?srsltid=AfmBOooEQ8c3jgvq-BJtH48oN3GY7-c4_KsYt6MVQ4JPhedXCQ4LGWCp")
    button = page.locator("#cookiescript_accept") 
    print("before click")
    page.screenshot(path="before_click.png")

    button.click()
    page.wait_for_timeout(2000)

    print("after click")
    page.screenshot(path="after_click.png")

    # overim, ze sa mi nezobrazuje
    cookies_square = page.locator("#cookiescript_injected")
    
    assert cookies_square.is_visible() == False

def test_new_page(page: Page):
    page.goto("https://www.lekarnalemon.cz/?srsltid=AfmBOooEQ8c3jgvq-BJtH48oN3GY7-c4_KsYt6MVQ4JPhedXCQ4LGWCp")
    # na stranke najdi v menu leto a klikni nan
    button = page.locator("#desktop-a8ab5f3c-86fa-414f-999e-4601782baaec-dropdown")
    button.click()

# rozbali sa mi ponuka, screenshot  
    page.wait_for_timeout(2000)
    page.screenshot(path="ponuka menu.png")
    # page.locator("body > header > div.page-header__navigation > div > nav > div.menu-item.menu-item-dropdown.show > div > div").wait_for(state="visible")

# chcem kliknut na text s doplnkami stravy:
    h_text = page.locator("text=Doplňky stravy na opalování")
    h_text.click()
    print("po kliknuti na doplnky stravy")

    assert page.url == "https://www.lekarnalemon.cz/leto/doplnky-stravy-na-opalovani"


def test_cart(page: Page):
    page.goto("https://www.lekarnalemon.cz/leto/doplnky-stravy-na-opalovani")
    # otvor si produkt s nazvom:
    produkt = page.locator("h3.box__product-title:has-text('Gs Betakaroten gold 15 mg 30 kapslí')")
    produkt.click()

    assert page.url ==  "https://www.lekarnalemon.cz/leto/doplnky-stravy-na-opalovani/gs-betakaroten-gold-15mg-cps-30-8595693300541"

    [print("druha cast")]
    page.wait_for_timeout(1000)
    # najdem tlacitko koupit, kliknem
    buy_button = page.locator("#product-head > div.container.mt-lg-4 > form > div > div:nth-child(2) > div > div > div > div.col-xl-7.col-lg-10.col-sm-9.col-md-6 > div > div.col-6.js-buy-button > button")
    buy_button.click()
    print("kliklo")
    page.wait_for_timeout(1000)

    # klik na x kosik
    cart = page.locator("#modal-template-content > div.modal__body > div.row.cart-modal-buttons > div.col-sm-6.text-center.text-sm-right.order-sm-1.mb-3.mb-sm-0 > a")
    cart.click()
    print("kliklo na pokracovat do kosiku")
 
    page.wait_for_url("https://www.lekarnalemon.cz/kosik")
    print("sme v kosiku")

    # skontrolujem, ze sa mi tam nachadza produkt

    cart_items = page.locator(".order-list__product-text a")
    assert cart_items.filter(has_text="Betakaroten").first.is_visible()

#toto nie je dobre ani v jednom riadku 
    # cart_content = page.locator("#item-f9dfe36b-c11c-47c5-b387-a0ea45e71b68 > div.order-list__item-cell.order-list__item-cell--product > div > div.order-list__product-text > a")  # alebo iný selektor podľa layoutu košíka
    # assert cart_content.filter(has_text="Betakaroten").is_visible()




 
