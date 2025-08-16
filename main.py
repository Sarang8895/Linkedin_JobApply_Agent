from utils.browser import launch_browser
from utils.auth import linkedin_login
from utils.jobs import search_and_apply_jobs
import yaml


def load_config():
    with open("config file path.yaml", "r") as f:
        config = yaml.safe_load(f)
        print("✅ Loaded Config:", config)  # <-- Add this line
        return config


def run():
    config = load_config()
    browser, context, page = launch_browser(headless=False)

    linkedin_login(page, config["linkedin"])
    search_and_apply_jobs(page, config["linkedin"])

    print("✅ Script execution complete.")
    context.close()
    browser.close()


if __name__ == "__main__":
    run()
