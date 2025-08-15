import time
from playwright.sync_api import Page
from utils.apply_modal import handle_easy_apply_modal

def search_and_apply_jobs(page: Page, config: dict):
    print("🔍 Navigating to Jobs page...")
    page.goto("https://www.linkedin.com/jobs", timeout=35000)
    page.wait_for_load_state("domcontentloaded")

    # Fill in keyword and location
    page.fill('[id^="jobs-search-box-keyword-id-ember"]', config["keywords"])
    # page.fill('[id^="jobs-search-box-location-id-ember"]', config["location"])
    page.keyboard.press("Enter")

    print(f"🧠 Searching for: {config['keywords']} in {config['location']}")
    time.sleep(5)

    # Wait for job listings
    page.wait_for_selector(".job-card-job-posting-card-wrapper__entity-lockup")

    # Get all job cards using your selector
    job_cards = page.query_selector_all(".job-card-job-posting-card-wrapper__entity-lockup")
    print(f"📄 Found {len(job_cards)} job cards.")

    easy_apply_count = 0

    for idx, card in enumerate(job_cards):
        print(f"\n➡️ Opening job {idx + 1}/{len(job_cards)}")

        try:
            card.click()
            time.sleep(3)  # Give time for the right panel to load

            apply_btn = page.query_selector("#jobs-apply-button-id")
            if apply_btn and apply_btn.is_visible():
                print("✅ Easy Apply available. Clicking...")
                apply_btn.click()
                
                time.sleep(2)


                success = handle_easy_apply_modal(page)

                if success:
                    easy_apply_count += 1
                    print("🎯 Successfully applied to this job.")
                else:
                    print("❌ Could not complete the application.")
                # Close modal if it opens
                close_btn = page.query_selector("button[aria-label='Dismiss']")
                if close_btn:
                    close_btn.click()
                    time.sleep(1)
            else:
                print("🚫 Easy Apply not available.")

        except Exception as e:
            print(f"⚠️ Error on job {idx + 1}: {e}")

    print(f"\n✅ Done! Easy Apply clicked for {easy_apply_count} job(s).")
