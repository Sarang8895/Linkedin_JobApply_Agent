# linkedin/apply_modal.py

import time
from utils.llm_answer import get_llm_answer

def handle_easy_apply_modal(page):
    print("🧾 Handling Easy Apply modal...")

    try:
        while True:
            time.sleep(2)

            # 1. Detect labels with actual questions (contain '?')
            labels = page.query_selector_all(".artdeco-text-input--label")
            if not labels:
                print("❗ No labels found on modal.")
            else:
                for label in labels:
                    try:
                        label_text = label.inner_text().strip()
                        if "?" not in label_text:
                            print(f"ℹ️ Skipping non-question label: {label_text}")
                            continue

                        print(f"🧠 Question detected: {label_text}")

                        # Get answer from LLM
                        answer = get_llm_answer(label_text)
                        print(f"✍️ Answer: {answer}")

                        # 2. Find the associated input/textarea/select
                        input_elem = label.evaluate_handle(
                            """label => 
                                label.parentElement.querySelector('input, textarea, select')"""
                        )

                        if input_elem:
                            tag_name = input_elem.evaluate("el => el.tagName.toLowerCase()")
                            if tag_name == "select":
                                page.select_option(f"#{input_elem.get_attribute('id')}", answer)
                            else:
                                input_elem.fill(answer)
                        else:
                            print("⚠️ Input element not found for this question.")

                    except Exception as e:
                        print(f"⚠️ Error answering question '{label_text}': {e}")

            # 3. Navigation buttons
            next_button = page.query_selector("button[aria-label*='Continue'], button[aria-label*='Next']")
            review_button = page.query_selector("button[aria-label*='Review']")
            submit_button = page.query_selector("button[aria-label*='Submit application'], button[aria-label='Submit']")

            if next_button and next_button.is_enabled():
                print("➡️ Clicking Next/Continue...")
                next_button.click()
                time.sleep(1)

                # Validation error check
                error_msg = page.query_selector(".artdeco-inline-feedback--error")
                if error_msg:
                    error_text = error_msg.inner_text().strip()
                    print(f"❗ Validation error: {error_text}")
                    # TODO: re-answer the problematic field using LLM
                    continue

            elif review_button and review_button.is_enabled():
                print("✅ Reached Review step.")
                review_button.click()
                time.sleep(1)

            elif submit_button and submit_button.is_enabled():
                print("🚀 Submitting final application...")
                submit_button.click()
                time.sleep(2)

                # Click "Done" if available
                done_button = page.query_selector("button[aria-label='Done']")
                if done_button:
                    done_button.click()
                return True

            else:
                print("🔚 No more steps.")
                break

    except Exception as e:
        print(f"❌ Error in modal flow: {e}")
        return False

    return False
