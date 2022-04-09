import sys

import slugify

import transifex_api
import trivia_api_getter


def get_key(original_string: str) -> str:
    return slugify.slugify(original_string)


if __name__ == "__main__":
    categories = trivia_api_getter.get_categories()
    if len(sys.argv) < 2:
        print("Usage: python3 main.py 'Category1' 'Category2'...'CategoryN'")
        print(
            f"Possible categories: {', '.join([category for category in categories])}"
        )
        exit(1)

    selected_categories = []
    has_invalid = False
    for arg in sys.argv[1:]:
        if arg.strip() not in categories:
            print(f"Invalid category {arg}")
            has_invalid = True
        else:
            print()
            selected_categories.append(
                {"id": categories[arg.strip()], "name": arg.strip()}
            )
    if has_invalid:
        print(
            f"Possible categories: {', '.join([category for category in categories])}"
        )
        exit(1)
    token = trivia_api_getter.get_token()
    for category_id in selected_categories:
        resource_slug = transifex_api.generate_resource_slug(
            category_id=category_id["id"], category_name=category_id["name"]
        )
        if not transifex_api.get_resource(resource_slug):
            print(f"Creating resource for {resource_slug}")
            transifex_api.create_resource(resource_slug)
        cat_data = trivia_api_getter.get_category_data(
            category=category_id["id"], token=token
        )
        generated_json = {}
        for question in cat_data:
            generated_json[get_key(question["question"])] = question["question"]
            generated_json[get_key(question["correct_answer"])] = question[
                "correct_answer"
            ]
            for incorrect in question["incorrect_answers"]:
                generated_json[get_key(incorrect)] = incorrect

        existing_strings = transifex_api.get_resource_strings(resource_slug)
        existing_strings.update(generated_json)
        transifex_api.upload_file(content=existing_strings, resource_slug=resource_slug)
