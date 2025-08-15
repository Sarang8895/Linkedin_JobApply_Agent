def linkedin_login(page, config):
    page.goto("https://www.linkedin.com/login", timeout=6000)
    page.fill("input#username", config["email"])
    page.fill("input#password", config["password"])
    page.click("button[type='submit']")
    
    page.wait_for_load_state("domcontentloaded")
    print("🔐 Logged into LinkedIn")
