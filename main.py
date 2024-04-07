import requests
import os
import hashlib


def calculate_hash(file_path: str) -> None:
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as file:
        while True:
            data = file.read(65536)
            if not data:
                break
            hasher.update(data)
    return hasher.hexdigest()


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
    exam_plan_link = "https://mitsdu.dk/-/media/files/om_sdu/fakulteterne/teknik/eksamensplaner/bachelor/bsc-softwareengineering-v23-2.pdf"
    save_location = "Resources"

    result = checkExamPlanForUpdate(exam_plan_link, save_location)

    if result:
        print("They are the same.")

    else:
        print("THEY ARE NOT THE SAME! New exam plan :O")
