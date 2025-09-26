import requests
import os
import hashlib
import json


def calculate_hash(file_path: str) -> None:
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as file:
        while True:
            data = file.read(65536)
            if not data:
                break
            hasher.update(data)
    return hasher.hexdigest()


def send_discord_message(webhook_url: str, message: str) -> bool:
    """
    Send a message to Discord via webhook

    Args:
        webhook_url (str): The Discord webhook URL
        message (str): The message to send

    Returns:
        bool: True if message was sent successfully, False otherwise
    """
    payload = {
        "content": message,
        "username": "Exam Plan Checker"
    }

    try:
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 204:
            print("Discord message sent successfully!")
            return True
        else:
            print(f"Failed to send Discord message. Status code: {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"Error sending Discord message: {e}")
        return False


def checkExamPlanForUpdate(exam_plan_link: str, save_location: str) -> bool:
    base_file = "./{0}/exam_plan.pdf".format(save_location)
    compare_file = "./{0}/exam_plan_compare.pdf".format(save_location)

    response = requests.get(exam_plan_link)
    # TODO: Check if response is good.

    if os.path.isfile(base_file):
        open(compare_file, "wb").write(response.content)

        base_file_hash = calculate_hash(base_file)
        compare_file_hash = calculate_hash(compare_file)

        try:
            os.remove(compare_file)
        except FileNotFoundError:
            print("Error: compare file could not be found")

        if base_file_hash == compare_file_hash:
            return True

        return False

    # Creates a file to be compared in future events.
    open(base_file, "wb").write(response.content)
    return checkExamPlanForUpdate(exam_plan_link, save_location)


if __name__ == "__main__":
    exam_plan_link = "https://mitsdu.dk/-/media/files/om_sdu/fakulteterne/teknik/eksamensplaner/exam_tek_summer2025_odense-5.pdf"
    save_location = "Resources"

    # Discord webhook URL - set this as an environment variable for security
    discord_webhook_url = os.getenv('DISCORD_WEBHOOK_URL')

    if not discord_webhook_url:
        print("Warning: DISCORD_WEBHOOK_URL environment variable not set. Discord notifications disabled.")

    result = checkExamPlanForUpdate(exam_plan_link, save_location)

    if result:
        print("They are the same.")

    else:
        print("THEY ARE NOT THE SAME! New exam plan :O")

        # Send Discord notification if webhook URL is configured
        if discord_webhook_url:
            message = (
                "🚨 **Exam Plan Update Alert!** 🚨\n\n"
                "A new exam plan has been detected!\n"
                f"Link: https://mitsdu.dk/da/mit_studie/kandidat/civilingenioer_i_softwareengineering/eksamen/eksamensplan\n\n"
                "Please check the updated exam schedule."
            )
            send_discord_message(discord_webhook_url, message)
