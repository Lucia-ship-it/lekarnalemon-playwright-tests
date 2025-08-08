from playwright.sync_api import Page
from datetime import datetime
import pytest

@pytest.fixture
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=2000)
        # context = browser.new_context()
        # page = context.new_page()
        page = browser.new_page()
        yield page

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

    button.click()
    page.wait_for_timeout(2000)

    print("after click")

    cookies_square = page.locator("#cookiescript_injected")
     # overim, ze sa mi nezobrazuje
    assert cookies_square.is_visible() == False


def test_new_page(page: Page):
    page.goto("https://www.lekarnalemon.cz/?srsltid=AfmBOooEQ8c3jgvq-BJtH48oN3GY7-c4_KsYt6MVQ4JPhedXCQ4LGWCp")
    # na stranke najdi v menu leto a klikni nan
    button = page.locator("#desktop-a8ab5f3c-86fa-414f-999e-4601782baaec-dropdown")
    button.click()

# rozbali sa mi ponuka, screenshot  
    page.wait_for_selector("body > header > div.page-header__navigation > div > nav > div.menu-item.menu-item-dropdown.show > div > div", 5000)
    page.screenshot(path="ponuka menu.png")

    # klik na text s doplnkami stravy:
    h_text = page.locator("text=Doplňky stravy na opalování")
    h_text.click()
    print("po kliknuti na doplnky stravy")

    assert page.url == "https://www.lekarnalemon.cz/leto/doplnky-stravy-na-opalovani"


def test_cart(page: Page):
    page.goto("https://www.lekarnalemon.cz/leto/doplnky-stravy-na-opalovani")
    # otvor si produkt 
    produkt = page.locator("h3.box__product-title:has-text('Gs Betakaroten gold 15 mg 30 kapslí')")
    produkt.click()

    assert page.url ==  "https://www.lekarnalemon.cz/leto/doplnky-stravy-na-opalovani/gs-betakaroten-gold-15mg-cps-30-8595693300541"

    [print("pokracujeme na novej stranke")]
    page.wait_for_load_state("networkidle")

    buy_button = page.locator("#product-head div.js-buy-button > button") #snad ho najde
    # buy_button = page.locator("#product-head > div.container.mt-lg-4 > form > div > div:nth-child(2) > div > div > div > div.col-xl-7.col-lg-10.col-sm-9.col-md-6 > div > div.col-6.js-buy-button > button")
    buy_button.click()
    print("kliklo")
    page.wait_for_selector("#modal-template-content > div.modal__body", 5000)

    # presun do kosiku
    cart = page.locator("#modal-template-content div.cart-modal-buttons a")
    # stare - ("#modal-template-content > div.modal__body > div.row.cart-modal-buttons > div.col-sm-6.text-center.text-sm-right.order-sm-1.mb-3.mb-sm-0 > a")
    cart.click()
    print("kliklo na pokracovat do kosiku")
 
    page.wait_for_url("https://www.lekarnalemon.cz/kosik")
    print("sme v kosiku")

    # skontrolujem, ze sa mi tam nachadza produkt
    cart_items = page.locator("#cart-form")

    assert cart_items.filter(has_text="Betakaroten").first.is_visible()

#toto nie je dobre 
    # assert cart_content.filter(has_text="Betakaroten").is_visible()


 # chcem zistit jestli je videt text ri ikonke prihlasit sa
def test_log_icon(page : Page):
    page.goto("https://www.lekarnalemon.cz/")
    icon = page.locator("body > header > div.container > div > div.page-header__top-nav > a:nth-child(2) > span.page-header__top-link--icon")
    icon.hover(timeout=1000) 
    #kontrola na objavenie sa textu
    text = page.locator('span.page-header__top-link--text', has_text="Přihlásit")

    assert text.is_visible(), "Text 'Přihlásit' sa nezobrazil po hovernutí na ikonku"


def test_log_in_negative(page: Page):
    page.goto("https://www.lekarnalemon.cz/login")
    page.fill("#_username", "test@email.com")
    page.fill("#_password", "heslo")
    page.press("#_password", "Enter")

    error_message = page.locator("#cart-form > div.alert.alert-danger.mb-4")  
    error_message.wait_for(state="visible", timeout=3000)

    assert error_message.is_visible(), "Chybová hláška o zlých údajoch sa nezobrazila"


def test_new_page(page: Page):
    page.goto("https://www.lekarnalemon.cz/")

    with page.expect_popup() as popup:
        button = page.locator("footer .page-footer__menu a:nth-child(1) picture img")
        button.click()

        new_page = popup.value
        assert new_page == "https://prehledy.sukl.cz/prehledy.html#/lekarny/00215013336?verify=true"

